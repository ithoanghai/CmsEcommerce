import json

from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import FormView, ListView, TemplateView
from django.views.generic.edit import CreateView
from drf_yasg.utils import swagger_auto_schema

# from ..creme_core.common.custom_auth import JSONWebTokenAuthentication
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from creme.creme_core.accounts.decorators import login_required
from creme.creme_core.accounts.mixins import LoginRequiredMixin
from creme.creme_core.accounts.views import SignupView
from creme.userprofile.models import Org, Profile
from creme.utils.mail import send_email

from .decorators import manager_required, team_required
from .forms import TeamForm, TeamInviteUserForm, TeamSignupForm, TeamInvitationForm
from .hooks import hookset
from .models import Team, Teams, Membership
from . import swagger_params
from .serializer import TeamCreateSerializer, TeamsSerializer
from .tasks import remove_users, update_team_users


MESSAGE_STRINGS = hookset.get_message_strings()


class TeamSignupView(SignupView):

    template_name = "app_list/teams/signup.html"

    def get_form_class(self):
        if self.signup_code:
            return self.form_class
        return TeamSignupForm

    def after_signup(self, form):
        if not self.signup_code:
            self.created_user.teams_created.create(
                name=form.cleaned_data["team"]
            )
        super().after_signup(form)


class TeamCreateView(LoginRequiredMixin, CreateView):

    form_class = TeamForm
    model = Team
    template_name = "app_list/teams/team_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TeamListView(ListView):

    model = Team
    context_object_name = "teams"
    template_name = "app_list/teams/team_list.html"


class TeamsListView(APIView, LimitOffsetPagination):
    model = Teams
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_context_data(self, **kwargs):
        params = self.request.post_data
        queryset = self.model.objects.filter(org=self.request.org).order_by("-id")
        if params:
            if params.get("team_name"):
                queryset = queryset.filter(name__icontains=params.get("team_name"))
            if params.get("created_by"):
                queryset = queryset.filter(created_by=params.get("created_by"))
            if params.get("assigned_users"):
                queryset = queryset.filter(
                    users__id__in=json.loads(params.get("assigned_users"))
                )

        context = {}
        results_teams = self.paginate_queryset(
            queryset.distinct(), self.request, view=self
        )
        teams = TeamsSerializer(results_teams, many=True).data
        if results_teams:
            offset = queryset.filter(id__gte=results_teams[-1].id).count()
            if offset == queryset.count():
                offset = None
        else:
            offset = 0
        context["per_page"] = 10
        page_number = (int(self.offset / 10) + 1,)
        context["page_number"] = page_number
        context.update({"teams_count": self.count, "offset": offset})
        context["teams"] = teams
        return context

    @swagger_auto_schema(
        tags=["Teams"], manual_parameters=swagger_params.teams_list_get_params
    )
    def get(self, request, *args, **kwargs):
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            return Response(
                {
                    "error": True,
                    "errors": "You don't have permission to perform this action.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        context = self.get_context_data(**kwargs)
        return Response(context)

    @swagger_auto_schema(
        tags=["Teams"], manual_parameters=swagger_params.teams_create_post_params
    )
    def post(self, request, *args, **kwargs):
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            return Response(
                {
                    "error": True,
                    "errors": "You don't have permission to perform this action.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        params = request.post_data

        serializer = TeamCreateSerializer(data=params, request_obj=request)
        if serializer.is_valid():
            team_obj = serializer.save(created_by=request.profile, org=request.org)

            if params.get("assign_users"):
                assinged_to_list = json.loads(params.get("assign_users"))
                profiles = Profile.objects.filter(
                    id__in=assinged_to_list, org=request.org
                )
                if profiles:
                    team_obj.users.add(*profiles)
            return Response(
                {"error": False, "message": "Team Created Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": True, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class TeamsDetailView(APIView):
    model = Teams
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        return self.model.objects.get(pk=pk, org=self.request.org)

    @swagger_auto_schema(
        tags=["Teams"], manual_parameters=swagger_params.organization_params
    )
    def get(self, request, pk, **kwargs):
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            return Response(
                {
                    "error": True,
                    "errors": "You don't have permission to perform this action.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        self.team_obj = self.get_object(pk)
        context = {}
        context["team"] = TeamsSerializer(self.team_obj).data
        return Response(context)

    @swagger_auto_schema(
        tags=["Teams"], manual_parameters=swagger_params.teams_create_post_params
    )
    def put(self, request, pk, *args, **kwargs):
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            return Response(
                {
                    "error": True,
                    "errors": "You don't have permission to perform this action.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        params = request.post_data
        self.team = self.get_object(pk)
        actual_users = self.team.get_users()
        removed_users = []
        serializer = TeamCreateSerializer(
            data=params, instance=self.team, request_obj=request
        )
        if serializer.is_valid():
            team_obj = serializer.save()

            team_obj.users.clear()
            if params.get("assign_users"):
                assinged_to_list = json.loads(params.get("assign_users"))
                profiles = Profile.objects.filter(
                    id__in=assinged_to_list, org=request.org
                )
                if profiles:
                    team_obj.users.add(*profiles)
            update_team_users.delay(pk)
            latest_users = team_obj.get_users()
            for user in actual_users:
                if user not in latest_users:
                    removed_users.append(user)
            remove_users.delay(removed_users, pk)
            return Response(
                {"error": False, "message": "Team Updated Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": True, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        tags=["Teams"], manual_parameters=swagger_params.organization_params
    )
    def delete(self, request, pk, **kwargs):
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            return Response(
                {
                    "error": True,
                    "errors": "You don't have permission to perform this action.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        self.team_obj = self.get_object(pk)
        self.team_obj.delete()
        return Response(
            {"error": False, "message": "Team Deleted Successfully"},
            status=status.HTTP_200_OK,
        )


class TeamManageView(TemplateView):

    template_name = "app_list/teams/team_manage.html"

    @method_decorator(manager_required)
    def dispatch(self, *args, **kwargs):
        self.team = self.request.team
        self.role = self.team.role_for(self.request.user)
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            "team": self.team,
            "role": self.role,
            "invite_form": self.get_team_invite_form(),
            "can_join": self.team.can_join(self.request.user),
            "can_leave": self.team.can_leave(self.request.user),
            "can_apply": self.team.can_apply(self.request.user),
        })
        return ctx

    def get_team_invite_form(self):
        return TeamInviteUserForm(team=self.team)


class TeamInviteView(FormView):
    http_method_names = ["post"]
    form_class = TeamInviteUserForm

    @method_decorator(manager_required)
    def dispatch(self, *args, **kwargs):
        self.team = self.request.team
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({"team": self.team})
        return form_kwargs


@team_required
@login_required
def team_update(request):
    team = request.team
    if not team.is_owner_or_manager(request.user):
        return HttpResponseForbidden()
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect(team.get_absolute_url())
    else:
        form = TeamForm(instance=team)
    return render(request, "app_list/teams/team_form.html", {"form": form, "team": team})


@team_required
@login_required
def team_detail(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    role = team.role_for(request.user)
    if team.access == "invitation" and state is None and not request.user.is_staff:
        raise Http404()
    if team.member_access == Team.MEMBER_ACCESS_INVITATION and state is None:
        raise Http404()

    if can_invite(team, request.user):
        if request.method == "POST":
            form = TeamInvitationForm(request.POST, team=team)
            if form.is_valid():
                form.invite()
                send_email([form.user.email], "teams_user_invited", context={"team": team})
                messages.success(request, _("Invitation created."))
                return redirect("team_detail", slug=slug)
        else:
            form = TeamInvitationForm(team=team)
    else:
        form = None

    return render(request, "app_list/teams/team_detail.html", {
        "team": team,
        "state": state,
        "role": role,
        "invite_form": form,
        "can_join": can_join(team, request.user),
        "can_leave": can_leave(team, request.user),
        "can_apply": can_apply(team, request.user),
    })


@team_required
@login_required
def team_join(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    if team.access == "invitation" and state is None and not request.user.is_staff:
        raise Http404()

    if team.manager_access == Team.MEMBER_ACCESS_INVITATION and \
       state is None and not request.user.is_staff:
        raise Http404()

    if can_join(team, request.user) and request.method == "POST":
        membership, created = Membership.objects.get_or_create(team=team, user=request.user)
        membership.role = Membership.ROLE_MEMBER
        membership.state = Membership.STATE_MEMBER
        membership.save()
        messages.success(request, _("Joined team."))
        return redirect("team_detail", slug=slug)
    else:
        return redirect("team_detail", slug=slug)


@team_required
@login_required
def team_leave(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    if team.access == "invitation" and state is None and not request.user.is_staff:
        raise Http404()

    if team.manager_access == Team.MEMBER_ACCESS_INVITATION and \
       state is None and not request.user.is_staff:
        raise Http404()

    if can_leave(team, request.user) and request.method == "POST":
        membership = Membership.objects.get(team=team, user=request.user)
        membership.delete()
        messages.success(request, _("Left team."))
        return redirect("teams:dashboard")
    else:
        return redirect("teams:team_detail", slug=slug)


@team_required
@login_required
def team_apply(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)

    if team.access == "invitation" and state is None and not request.user.is_staff:
        raise Http404()
    if team.manager_access == Team.MEMBER_ACCESS_INVITATION and \
       state is None and not request.user.is_staff:
        raise Http404()

    if team.can_apply(team, request.user) and request.method == "POST":
        membership, created = Membership.objects.get_or_create(team=team, user=request.user)
        membership.state = Membership.STATE_APPLIED
        membership.save()
        managers = [m.user.email for m in team.managers()]
        send_email(managers, "teams_user_applied", context={
            "team": team,
            "user": request.user
        })
        messages.success(request, _("Applied to join team."))
        return redirect("teams:team_detail", slug=slug)
    else:
        return redirect("teams:team_detail", slug=slug)


@login_required
@require_POST
def team_accept(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    membership = get_object_or_404(Membership, pk=pk)
    state = membership.team.get_state_for_user(request.user)
    if membership.accept(by=request.user):
        messages.success(request, MESSAGE_STRINGS["accepted-application"])
    if request.user.is_staff or state == "manager":
        if membership.state == "applied":
            membership.state = "member"
            membership.save()
            messages.success(request, _("Accepted application."))
        if membership.accept(by=request.user):
            messages.success(request, MESSAGE_STRINGS["accepted-application"])

    return redirect("teams:team_detail", slug=membership.team.slug)


@login_required
@require_POST
def team_reject(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    membership = get_object_or_404(Membership, pk=pk)
    state = membership.team.get_state_for_user(request.user)
    if request.user.is_staff or state == "manager":
        if membership.state == "applied":
            membership.state = "rejected"
            membership.save()
            messages.success(request, _("Rejected application."))
    if membership.reject(by=request.user):
        messages.success(request, MESSAGE_STRINGS["rejected-application"])
    return redirect("teams:team_detail", slug=membership.team.slug)


@login_required
def team_promote(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    membership = get_object_or_404(Membership, pk=pk)
    state = membership.team.get_state_for_user(request.user)
    if request.user.is_staff or state == "manager":
        if membership.state == "member":
            membership.state = "manager"
            membership.save()
            messages.success(request, _("Promoted to manager."))
    return redirect("team_detail", slug=membership.team.slug)


@manager_required
@require_POST
def team_member_promote(request, pk):
    membership = get_object_or_404(request.team.memberships.all(), pk=pk)
    membership.promote(by=request.user)
    data = {
        "html": render_to_string(
            "app_list/teams/_membership.html",
            {
                "membership": membership,
                "team": request.team
            },
            request=request
        )
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def team_demote(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    membership = get_object_or_404(Membership, pk=pk)
    state = membership.team.get_state_for_user(request.user)
    if request.user.is_staff or state == "manager":
        if membership.state == "manager":
            membership.state = "member"
            membership.save()
            messages.success(request, _("Demoted from manager."))
    return redirect("team_detail", slug=membership.team.slug)


@manager_required
@require_POST
def team_member_demote(request, pk):
    membership = get_object_or_404(request.team.memberships.all(), pk=pk)
    membership.demote(by=request.user)
    data = {
        "html": render_to_string(
            "app_list/teams/_membership.html",
            {
                "membership": membership,
                "team": request.team
            },
            request=request
        )
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_unbound_form(self):
    """
    Overrides behavior of FormView.get_form_kwargs
    when method is POST or PUT
    """
    form_kwargs = self.get_form_kwargs()
    # @@@ remove fields that would cause the form to be bound
    # when instantiated
    bound_fields = ["data", "files"]
    for field in bound_fields:
        form_kwargs.pop(field, None)
    return self.get_form_class()(**form_kwargs)


def after_membership_added(self, form):
    """
    Allows the developer to customize actions that happen after a membership
    was added in form_valid
    """
    pass


@manager_required
@require_POST
def team_member_revoke_invite(request, pk):
    membership = get_object_or_404(request.team.memberships.all(), pk=pk)
    membership.remove(by=request.user)
    data = {
        "html": ""
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


@manager_required
@require_POST
def team_member_resend_invite(request, pk):
    membership = get_object_or_404(request.team.memberships.all(), pk=pk)
    membership.resend_invite(by=request.user)
    data = {
        "html": render_to_string(
            "app_list/teams/_membership.html",
            {
                "membership": membership,
                "team": request.team
            },
            request=request
        )
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


@manager_required
@require_POST
def team_member_remove(request, pk):
    membership = get_object_or_404(request.team.memberships.all(), pk=pk)
    membership.remove(by=request.user)
    data = {
        "html": ""
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


@team_required
@login_required
def autocomplete_users(request):
    team = request.team
    role = team.role_for(request.user)
    if role not in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
        raise Http404()
    User = get_user_model()
    users = User.objects.exclude(pk__in=[
        x.user.pk for x in team.memberships.exclude(user__isnull=True)
    ])
    q = request.GET.get("query")
    results = []
    if q:
        results.extend([
            hookset.get_autocomplete_result(x)
            for x in hookset.search_queryset(q, users)
        ])
    return HttpResponse(json.dumps(results), content_type="application/json")


def can_join(team, user):
    state = team.get_state_for_user(user)
    if team.access == "open" and state is None:
        return True
    elif state == "invited":
        return True
    elif user.is_staff and state is None:
        return True
    else:
        return False


def can_leave(team, user):
    state = team.get_state_for_user(user)
    if state == "member":  # managers can't leave at the moment
        return True
    else:
        return False


def can_apply(team, user):
    state = team.get_state_for_user(user)
    if team.access == "application" and state is None:
        return True
    else:
        return False


def can_invite(team, user):
    state = team.get_state_for_user(user)
    if team.access == "invitation":
        if state == "manager" or user.is_staff:
            return True
    return False


def get_form_success_data(self, form):
    """
    Allows customization of the JSON data returned when a valid form submission occurs.
    """
    data = {
        "html": render_to_string(
            "app_list/teams/_invite_form.html",
            {
                "invite_form": self.get_unbound_form(),
                "team": self.team
            },
            request=self.request
        )
    }

    membership = self.membership
    if membership is not None:
        if membership.state == Membership.STATE_APPLIED:
            fragment_class = ".applicants"
        elif membership.state == Membership.STATE_INVITED:
            fragment_class = ".invitees"
        elif membership.state in (Membership.STATE_AUTO_JOINED, Membership.STATE_ACCEPTED):
            fragment_class = {
                Membership.ROLE_OWNER: ".owners",
                Membership.ROLE_MANAGER: ".managers",
                Membership.ROLE_MEMBER: ".members"
            }[membership.role]
        data.update({
            "append-fragments": {
                fragment_class: render_to_string(
                    "app_list/teams/_membership.html",
                    {
                        "membership": membership,
                        "team": self.team
                    },
                    request=self.request
                )
            }
        })
    return data


def form_valid(self, form):
    user_or_email = form.cleaned_data["invitee"]
    role = form.cleaned_data["role"]
    if isinstance(user_or_email, str):
        self.membership = self.team.invite_user(self.request.user, user_or_email, role)
    else:
        self.membership = self.team.add_user(user_or_email, role, by=self.request.user)

    self.after_membership_added(form)

    data = self.get_form_success_data(form)
    return self.render_to_response(data)

def form_invalid(self, form):
    data = {
        "html": render_to_string("app_list/teams/_invite_form.html", {
            "invite_form": form,
            "team": self.team
        }, request=self.request)
    }
    return self.render_to_response(data)

def render_to_response(self, context, **response_kwargs):
    return JsonResponse(context)


