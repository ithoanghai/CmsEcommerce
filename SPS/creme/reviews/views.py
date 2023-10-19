from __future__ import unicode_literals
import hashlib
import random

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mass_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context, Template
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import static
from django.views.decorators.http import require_POST
from django.views.generic import (
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
    CreateView, View
)

from .hooks import hookset
from .utils import CanReviewMixin, LoggedInMixin, reviews_generator
from .forms import ReviewForm, SpeakerCommentForm, BulkPresentationForm, SubmitterCommentForm
from .models import (
    ReviewAssignment, Review, LatestVote, ProposalResult, NotificationTemplate,
    ResultNotification, ProposalMessage,
    ProposalKind, SupportingDocument, AdditionalSpeaker,
    ProposalBase, ProposalSection
)
from .signals import review_added
from .forms import (AddSpeakerForm, SupportingDocumentCreateForm)

# @@@ switch to pinax-teams
from ..creme_core.models.auth import User, EmailAddress
from ..creme_core.accounts.decorators import login_required
from ..speakers.models import Speaker
from ..teams.models import Team
from ..conf import settings
from ..utils.mail import send_email
from ..creme_core.core.loading import get_classes, get_model, get_form
from ..creme_core.core.utils import redirect_to_referrer


ProductReviewForm, VoteForm, SortReviewsForm = get_classes(
    'reviews.forms',
    ['ProductReviewForm', 'VoteForm', 'SortReviewsForm'])

Vote = get_model('reviews', 'vote')
ProductReview = get_model('reviews', 'ProductReview')
Product = get_model('catalogue', 'product')


def access_not_permitted(request):
    return render(request, "app_list/reviews/access_not_permitted.html")


def proposals_generator(request, queryset, user_pk=None, check_speaker=True):

    for obj in queryset:
        # @@@ this sucks; we can do better
        if check_speaker:
            if request.user in [s.user for s in obj.speakers()]:
                continue

        try:
            obj.result
        except ProposalResult.DoesNotExist:
            ProposalResult.objects.get_or_create(proposal=obj)

        obj.comment_count = obj.result.comment_count
        obj.total_votes = obj.result.vote_count
        obj.plus_one = obj.result.plus_one
        obj.plus_zero = obj.result.plus_zero
        obj.minus_zero = obj.result.minus_zero
        obj.minus_one = obj.result.minus_one
        lookup_params = dict(proposal=obj)

        if user_pk:
            lookup_params["user__pk"] = user_pk
        else:
            lookup_params["user"] = request.user

        try:
            obj.user_vote = LatestVote.objects.get(**lookup_params).vote
            obj.user_vote_css = LatestVote.objects.get(**lookup_params).css_class()
        except LatestVote.DoesNotExist:
            obj.user_vote = None
            obj.user_vote_css = "no-vote"

        yield obj


def proposal_submit(request):
    if not request.user.is_authenticated():
        messages.info(request, _("To submit a proposal, please "
                                 "<a href='{0}'>log in</a> and create a speaker profile "
                                 "via the dashboard.".format(settings.LOGIN_URL)))
        return redirect("home")  # @@@ unauth'd speaker info page?
    else:
        try:
            request.user.speaker_profile
        except ObjectDoesNotExist:
            url = reverse("speaker_create")
            messages.info(request, _("To submit a proposal, first "
                                     "<a href='{0}'>create a speaker "
                                     "profile</a>.".format(url)))
            return redirect("dashboard")

    kinds = []
    for proposal_section in ProposalSection.available():
        for kind in proposal_section.section.proposal_kinds.all():
            kinds.append(kind)

    return render(request, "app_list/proposals/proposal_submit.html", {
        "kinds": kinds,
    })


def proposal_submit_kind(request, kind_slug):

    kind = get_object_or_404(ProposalKind, slug=kind_slug)

    if not request.user.is_authenticated():
        return redirect("home")  # @@@ unauth'd speaker info page?
    else:
        try:
            speaker_profile = request.user.speaker_profile
        except ObjectDoesNotExist:
            return redirect("dashboard")

    if not kind.section.proposalsection.is_available():
        return redirect("proposal_submit")

    form_class = get_form(settings.PROPOSAL_FORMS[kind_slug])

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.kind = kind
            proposal.speaker = speaker_profile
            proposal.save()
            form.save_m2m()
            messages.success(request, _("Proposal submitted."))
            if "add-speakers" in request.POST:
                return redirect("proposal_speaker_manage", proposal.pk)
            return redirect("dashboard")
    else:
        form = form_class()

    return render(request, "app_list/proposals/proposal_submit_kind.html", {
        "kind": kind,
        "proposal_form": form,
    })


@login_required
def proposal_speaker_manage(request, pk):
    queryset = ProposalBase.objects.select_related("speaker")
    proposal = get_object_or_404(queryset, pk=pk)
    proposal = ProposalBase.objects.get_subclass(pk=proposal.pk)

    if proposal.speaker != request.user.speaker_profile:
        raise Http404()

    if request.method == "POST":
        add_speaker_form = AddSpeakerForm(request.POST, proposal=proposal)
        if add_speaker_form.is_valid():
            message_ctx = {
                "proposal": proposal,
            }

            def create_speaker_token(email_address):
                # create token and look for an existing speaker to prevent
                # duplicate tokens and confusing the pending speaker
                try:
                    pending = Speaker.objects.get(
                        Q(user=None, invite_email=email_address)
                    )
                except Speaker.DoesNotExist:
                    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                    token = hashlib.sha1(salt + email_address).hexdigest()
                    pending = Speaker.objects.create(
                        invite_email=email_address,
                        invite_token=token,
                    )
                else:
                    token = pending.invite_token
                return pending, token
            email_address = add_speaker_form.cleaned_data["email"]
            # check if email is on the site now
            users = EmailAddress.objects.get_users_for(email_address)
            if users:
                # should only be one since we enforce unique email
                user = users[0]
                message_ctx["user"] = user
                # look for speaker profile
                try:
                    speaker = user.speaker_profile
                except ObjectDoesNotExist:
                    speaker, token = create_speaker_token(email_address)
                    message_ctx["token"] = token
                    # fire off email to user to create profile
                    send_email(
                        [email_address], "speaker_no_profile",
                        context=message_ctx
                    )
                else:
                    # fire off email to user letting them they are loved.
                    send_email(
                        [email_address], "speaker_addition",
                        context=message_ctx
                    )
            else:
                speaker, token = create_speaker_token(email_address)
                message_ctx["token"] = token
                # fire off email letting user know about site and to create
                # account and speaker profile
                send_email(
                    [email_address], "speaker_invite",
                    context=message_ctx
                )
            invitation, created = AdditionalSpeaker.objects.get_or_create(
                proposalbase=proposal.proposalbase_ptr, speaker=speaker)
            messages.success(request, "Speaker invited to proposal.")
            return redirect("proposal_speaker_manage", proposal.pk)
    else:
        add_speaker_form = AddSpeakerForm(proposal=proposal)
    ctx = {
        "proposal": proposal,
        "speakers": proposal.speakers(),
        "add_speaker_form": add_speaker_form,
    }
    return render(request, "app_list/proposals/proposal_speaker_manage.html", ctx)


@login_required
def proposal_edit(request, pk):
    queryset = ProposalBase.objects.select_related("speaker")
    proposal = get_object_or_404(queryset, pk=pk)
    proposal = ProposalBase.objects.get_subclass(pk=proposal.pk)

    if request.user != proposal.speaker.user:
        raise Http404()

    if not proposal.can_edit():
        ctx = {
            "title": "Proposal editing closed",
            "body": "Proposal editing is closed for this session type."
        }
        return render(request, "app_list/proposals/proposal_error.html", ctx)

    form_class = get_form(settings.PROPOSAL_FORMS[proposal.kind.slug])

    if request.method == "POST":
        form = form_class(request.POST, instance=proposal)
        if form.is_valid():
            form.save()
            if hasattr(proposal, "reviews"):
                users = User.objects.filter(
                    Q(review__proposal=proposal) |
                    Q(proposalmessage__proposal=proposal)
                )
                users = users.exclude(id=request.user.id).distinct()
                for user in users:
                    ctx = {
                        "user": request.user,
                        "proposal": proposal,
                    }
                    send_email(
                        [user.email], "proposal_updated",
                        context=ctx
                    )
            messages.success(request, "Proposal updated.")
            return redirect("proposal_detail", proposal.pk)
    else:
        form = form_class(instance=proposal)

    return render(request, "app_list/proposals/proposal_edit.html", {
        "proposal": proposal,
        "form": form,
    })


@login_required
def proposal_detail(request, pk):
    queryset = ProposalBase.objects.select_related("speaker", "speaker__user")
    proposal = get_object_or_404(queryset, pk=pk)
    proposal = ProposalBase.objects.get_subclass(pk=proposal.pk)

    if request.user not in [p.user for p in proposal.speakers()]:
        raise Http404()

    if "creme.reviews" in settings.INSTALLED_APPS:
        from ..reviews.forms import SpeakerCommentForm
        message_form = SpeakerCommentForm()
        if request.method == "POST":
            message_form = SpeakerCommentForm(request.POST)
            if message_form.is_valid():

                message = message_form.save(commit=False)
                message.user = request.user
                message.proposal = proposal
                message.save()

                ProposalMessage = SpeakerCommentForm.Meta.model
                reviewers = User.objects.filter(
                    id__in=ProposalMessage.objects.filter(
                        proposal=proposal
                    ).exclude(
                        user=request.user
                    ).distinct().values_list("user", flat=True)
                )

                for reviewer in reviewers:
                    ctx = {
                        "proposal": proposal,
                        "message": message,
                        "reviewer": True,
                    }
                    send_email(
                        [reviewer.email], "proposal_new_message",
                        context=ctx
                    )

                return redirect(request.path)
        else:
            message_form = SpeakerCommentForm()
    else:
        message_form = None

    return render(request, "app_list/proposals/proposal_detail.html", {
        "proposal": proposal,
        "message_form": message_form
    })


@login_required
def proposal_cancel(request, pk):
    queryset = ProposalBase.objects.select_related("speaker")
    proposal = get_object_or_404(queryset, pk=pk)
    proposal = ProposalBase.objects.get_subclass(pk=proposal.pk)

    if proposal.speaker.user != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        proposal.cancelled = True
        proposal.save()
        # @@@ fire off email to submitter and other speakers
        messages.success(request, "%s has been cancelled" % proposal.title)
        return redirect("dashboard")

    return render(request, "app_list/proposals/proposal_cancel.html", {
        "proposal": proposal,
    })


@login_required
def proposal_leave(request, pk):
    queryset = ProposalBase.objects.select_related("speaker")
    proposal = get_object_or_404(queryset, pk=pk)
    proposal = ProposalBase.objects.get_subclass(pk=proposal.pk)

    try:
        speaker = proposal.additional_speakers.get(user=request.user)
    except ObjectDoesNotExist:
        return HttpResponseForbidden()
    if request.method == "POST":
        proposal.additional_speakers.remove(speaker)
        # @@@ fire off email to submitter and other speakers
        messages.success(request, "You are no longer speaking on %s" % proposal.title)
        return redirect("dashboard")
    ctx = {
        "proposal": proposal,
    }
    return render(request, "app_list/proposals/proposal_leave.html", ctx)


@login_required
def proposal_pending_join(request, pk):
    proposal = get_object_or_404(ProposalBase, pk=pk)
    speaking = get_object_or_404(AdditionalSpeaker, speaker=request.user.speaker_profile,
                                 proposalbase=proposal)
    if speaking.status == AdditionalSpeaker.SPEAKING_STATUS_PENDING:
        speaking.status = AdditionalSpeaker.SPEAKING_STATUS_ACCEPTED
        speaking.save()
        messages.success(request, "You have accepted the invitation to join %s" % proposal.title)
        return redirect("dashboard")
    else:
        return redirect("dashboard")


@login_required
def proposal_pending_decline(request, pk):
    proposal = get_object_or_404(ProposalBase, pk=pk)
    speaking = get_object_or_404(AdditionalSpeaker, speaker=request.user.speaker_profile,
                                 proposalbase=proposal)
    if speaking.status == AdditionalSpeaker.SPEAKING_STATUS_PENDING:
        speaking.status = AdditionalSpeaker.SPEAKING_STATUS_DECLINED
        speaking.save()
        messages.success(request, "You have declined to speak on %s" % proposal.title)
        return redirect("dashboard")
    else:
        return redirect("dashboard")


# Returns a list of all proposals, proposals reviewed by the user, or the proposals the user has
# yet to review depending on the link user clicks in dashboard
@login_required
def review_section(request, section_slug, assigned=False, reviewed="all"):

    if not request.user.has_perm("reviews.can_review_%s" % section_slug):
        return access_not_permitted(request)

    section = get_object_or_404(ProposalSection, section__slug=section_slug)
    queryset = ProposalBase.objects.filter(kind__section=section.section)

    if assigned:
        assignments = ReviewAssignment.objects.filter(user=request.user)\
            .values_list("proposal__id")
        queryset = queryset.filter(id__in=assignments)

    # passing reviewed in from reviews.urls and out to review_list for
    # appropriate template header rendering
    if reviewed == "all":
        queryset = queryset.select_related("result").select_subclasses()
        reviewed = "all_reviews"
    elif reviewed == "reviewed":
        queryset = queryset.filter(reviews__user=request.user)
        reviewed = "user_reviewed"
    else:
        queryset = queryset.exclude(reviews__user=request.user).exclude(
            speaker__user=request.user)
        reviewed = "user_not_reviewed"

    proposals = proposals_generator(request, queryset)

    ctx = {
        "proposals": proposals,
        "section": section,
        "reviewed": reviewed,
    }

    return render(request, "app_list/reviews/review_list.html", ctx)


@login_required
def review_list(request, section_slug, user_pk):

    # if they're not a reviewer admin and they aren't the person whose
    # review list is being asked for, don't let them in
    if not request.user.has_perm("reviews.can_manage_%s" % section_slug):
        if not request.user.pk == user_pk:
            return access_not_permitted(request)

    queryset = ProposalBase.objects.select_related("speaker__user", "result")
    reviewed = LatestVote.objects.filter(user__pk=user_pk).values_list("proposal", flat=True)
    queryset = queryset.filter(pk__in=reviewed)
    proposals = queryset.order_by("submitted")

    admin = request.user.has_perm("reviews.can_manage_%s" % section_slug)

    proposals = proposals_generator(request, proposals, user_pk=user_pk, check_speaker=not admin)

    ctx = {
        "proposals": proposals,
    }
    return render(request, "app_list/reviews/review_list.html", ctx)


@login_required
def review_admin(request, section_slug):

    if not request.user.has_perm("reviews.can_manage_%s" % section_slug):
        return access_not_permitted(request)

    def reviewers():
        already_seen = set()

        for team in Team.objects.filter(permissions__codename="can_review_%s" % section_slug):
            for membership in team.memberships.filter(Q(state="member") | Q(state="manager")):
                user = membership.user
                if user.pk in already_seen:
                    continue
                already_seen.add(user.pk)

                user.comment_count = Review.objects.filter(user=user).count()
                user.total_votes = LatestVote.objects.filter(user=user).count()
                user.plus_one = LatestVote.objects.filter(
                    user=user,
                    vote=LatestVote.VOTES.PLUS_ONE
                ).count()
                user.plus_zero = LatestVote.objects.filter(
                    user=user,
                    vote=LatestVote.VOTES.PLUS_ZERO
                ).count()
                user.minus_zero = LatestVote.objects.filter(
                    user=user,
                    vote=LatestVote.VOTES.MINUS_ZERO
                ).count()
                user.minus_one = LatestVote.objects.filter(
                    user=user,
                    vote=LatestVote.VOTES.MINUS_ONE
                ).count()

                yield user

    ctx = {
        "section_slug": section_slug,
        "reviewers": reviewers(),
    }
    return render(request, "app_list/reviews/review_admin.html", ctx)


# FIXME: This view is too complex according to flake8
@login_required
def review_detail(request, pk):

    proposals = ProposalBase.objects.select_related("result").select_subclasses()
    proposal = get_object_or_404(proposals, pk=pk)

    if not request.user.has_perm("reviews.can_review_%s" % proposal.kind.section.slug):
        return access_not_permitted(request)

    speakers = [s.user for s in proposal.speakers()]

    if not request.user.is_superuser and request.user in speakers:
        return access_not_permitted(request)

    admin = request.user.is_staff

    try:
        latest_vote = LatestVote.objects.get(proposal=proposal, user=request.user)
    except LatestVote.DoesNotExist:
        latest_vote = None

    if request.method == "POST":
        if request.user in speakers:
            return access_not_permitted(request)

        if "vote_submit" in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():

                review = review_form.save(commit=False)
                review.user = request.user
                review.proposal = proposal
                review.save()

                return redirect(request.path)
            else:
                message_form = SpeakerCommentForm()
        elif "message_submit" in request.POST:
            message_form = SpeakerCommentForm(request.POST)
            if message_form.is_valid():

                message = message_form.save(commit=False)
                message.user = request.user
                message.proposal = proposal
                message.save()

                for speaker in speakers:
                    if speaker and speaker.email:
                        ctx = {
                            "proposal": proposal,
                            "message": message,
                            "reviewer": False,
                        }
                        send_email(
                            [speaker.email], "proposal_new_message",
                            context=ctx
                        )

                return redirect(request.path)
            else:
                initial = {}
                if latest_vote:
                    initial["vote"] = latest_vote.vote
                if request.user in speakers:
                    review_form = None
                else:
                    review_form = ReviewForm(initial=initial)
        elif "result_submit" in request.POST:
            if admin:
                result = request.POST["result_submit"]

                if result == "accept":
                    proposal.result.status = "accepted"
                    proposal.result.save()
                elif result == "reject":
                    proposal.result.status = "rejected"
                    proposal.result.save()
                elif result == "undecide":
                    proposal.result.status = "undecided"
                    proposal.result.save()
                elif result == "standby":
                    proposal.result.status = "standby"
                    proposal.result.save()

            return redirect(request.path)
    else:
        initial = {}
        if latest_vote:
            initial["vote"] = latest_vote.vote
        if request.user in speakers:
            review_form = None
        else:
            review_form = ReviewForm(initial=initial)
        message_form = SpeakerCommentForm()

    proposal.comment_count = proposal.result.comment_count
    proposal.total_votes = proposal.result.vote_count
    proposal.plus_one = proposal.result.plus_one
    proposal.plus_zero = proposal.result.plus_zero
    proposal.minus_zero = proposal.result.minus_zero
    proposal.minus_one = proposal.result.minus_one

    reviews = Review.objects.filter(proposal=proposal).order_by("-submitted_at")
    messages = proposal.messages.order_by("submitted_at")

    return render(request, "app_list/reviews/review_detail.html", {
        "proposal": proposal,
        "latest_vote": latest_vote,
        "reviews": reviews,
        "review_messages": messages,
        "review_form": review_form,
        "message_form": message_form
    })


@login_required
@require_POST
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    section_slug = review.section.slug

    if not request.user.has_perm("reviews.can_manage_%s" % section_slug):
        return access_not_permitted(request)

    review = get_object_or_404(Review, pk=pk)
    review.delete()

    return redirect("review_detail", pk=review.proposal.pk)


@login_required
def review_status(request, section_slug=None, key=None):

    if not request.user.has_perm("reviews.can_review_%s" % section_slug):
        return access_not_permitted(request)

    VOTE_THRESHOLD = settings.SYMPOSION_VOTE_THRESHOLD

    ctx = {
        "section_slug": section_slug,
        "vote_threshold": VOTE_THRESHOLD,
    }

    queryset = ProposalBase.objects.select_related("speaker__user", "result").select_subclasses()
    if section_slug:
        queryset = queryset.filter(kind__section__slug=section_slug)

    proposals = {
        # proposals with at least VOTE_THRESHOLD reviews and at least one +1 and no -1s, sorted by
        # the 'score'
        "positive": queryset.filter(result__vote_count__gte=VOTE_THRESHOLD, result__plus_one__gt=0,
                                    result__minus_one=0).order_by("-result__score"),
        # proposals with at least VOTE_THRESHOLD reviews and at least one -1 and no +1s, reverse
        # sorted by the 'score'
        "negative": queryset.filter(result__vote_count__gte=VOTE_THRESHOLD, result__minus_one__gt=0,
                                    result__plus_one=0).order_by("result__score"),
        # proposals with at least VOTE_THRESHOLD reviews and neither a +1 or a -1, sorted by total
        # votes (lowest first)
        "indifferent": queryset.filter(result__vote_count__gte=VOTE_THRESHOLD, result__minus_one=0,
                                       result__plus_one=0).order_by("result__vote_count"),
        # proposals with at least VOTE_THRESHOLD reviews and both a +1 and -1, sorted by total
        # votes (highest first)
        "controversial": queryset.filter(result__vote_count__gte=VOTE_THRESHOLD,
                                         result__plus_one__gt=0, result__minus_one__gt=0)
        .order_by("-result__vote_count"),
        # proposals with fewer than VOTE_THRESHOLD reviews
        "too_few": queryset.filter(result__vote_count__lt=VOTE_THRESHOLD)
        .order_by("result__vote_count"),
    }

    admin = request.user.has_perm("reviews.can_manage_%s" % section_slug)

    for status in proposals:
        if key and key != status:
            continue
        proposals[status] = list(proposals_generator(request, proposals[status], check_speaker=not admin))

    if key:
        ctx.update({
            "key": key,
            "proposals": proposals[key],
        })
    else:
        ctx["proposals"] = proposals

    return render(request, "app_list/reviews/review_stats.html", ctx)


@login_required
def review_assignments(request):
    if not request.user.groups.filter(name="reviewers").exists():
        return access_not_permitted(request)
    assignments = ReviewAssignment.objects.filter(
        user=request.user,
        opted_out=False
    )
    return render(request, "app_list/reviews/review_assignment.html", {
        "assignments": assignments,
    })


@login_required
@require_POST
def review_assignment_opt_out(request, pk):
    review_assignment = get_object_or_404(
        ReviewAssignment, pk=pk, user=request.user)
    if not review_assignment.opted_out:
        review_assignment.opted_out = True
        review_assignment.save()
        ReviewAssignment.create_assignments(
            review_assignment.proposal, origin=ReviewAssignment.AUTO_ASSIGNED_LATER)
    return redirect("review_assignments")


@login_required
def review_bulk_accept(request, section_slug):
    if not request.user.has_perm("reviews.can_manage_%s" % section_slug):
        return access_not_permitted(request)
    if request.method == "POST":
        form = BulkPresentationForm(request.POST)
        if form.is_valid():
            talk_ids = form.cleaned_data["talk_ids"].split(",")
            talks = ProposalBase.objects.filter(id__in=talk_ids).select_related("result")
            for talk in talks:
                talk.result.status = "accepted"
                talk.result.save()
            return redirect("review_section", section_slug=section_slug)
    else:
        form = BulkPresentationForm()

    return render(request, "app_list/reviews/review_bulk_accept.html", {
        "form": form,
    })


@login_required
def result_notification(request, section_slug, status):
    if not request.user.has_perm("reviews.can_manage_%s" % section_slug):
        return access_not_permitted(request)

    proposals = ProposalBase.objects.filter(kind__section__slug=section_slug, result__status=status).select_related("speaker__user", "result").select_subclasses()
    notification_templates = NotificationTemplate.objects.all()

    ctx = {
        "section_slug": section_slug,
        "status": status,
        "proposals": proposals,
        "notification_templates": notification_templates,
    }
    return render(request, "app_list/reviews/result_notification.html", ctx)


@login_required
def result_notification_prepare(request, section_slug, status):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    if not request.user.has_perm("reviews.can_manage_%s" % section_slug):
        return access_not_permitted(request)

    proposal_pks = []
    try:
        for pk in request.POST.getlist("_selected_action"):
            proposal_pks.append(int(pk))
    except ValueError:
        return HttpResponseBadRequest()
    proposals = ProposalBase.objects.filter(
        kind__section__slug=section_slug,
        result__status=status,
    )
    proposals = proposals.filter(pk__in=proposal_pks)
    proposals = proposals.select_related("speaker__user", "result")
    proposals = proposals.select_subclasses()

    notification_template_pk = request.POST.get("notification_template", "")
    if notification_template_pk:
        notification_template = NotificationTemplate.objects.get(pk=notification_template_pk)
    else:
        notification_template = None

    ctx = {
        "section_slug": section_slug,
        "status": status,
        "notification_template": notification_template,
        "proposals": proposals,
        "proposal_pks": ",".join([str(pk) for pk in proposal_pks]),
    }
    return render(request, "app_list/reviews/result_notification_prepare.html", ctx)


@login_required
def result_notification_send(request, section_slug, status):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    if not request.user.has_perm("reviews.can_manage_%s" % section_slug):
        return access_not_permitted(request)

    if not all([k in request.POST for k in ["proposal_pks", "from_address", "subject", "body"]]):
        return HttpResponseBadRequest()

    try:
        proposal_pks = [int(pk) for pk in request.POST["proposal_pks"].split(",")]
    except ValueError:
        return HttpResponseBadRequest()

    proposals = ProposalBase.objects.filter(
        kind__section__slug=section_slug,
        result__status=status,
    )
    proposals = proposals.filter(pk__in=proposal_pks)
    proposals = proposals.select_related("speaker__user", "result")
    proposals = proposals.select_subclasses()

    notification_template_pk = request.POST.get("notification_template", "")
    if notification_template_pk:
        notification_template = NotificationTemplate.objects.get(pk=notification_template_pk)
    else:
        notification_template = None

    emails = []

    for proposal in proposals:
        rn = ResultNotification()
        rn.proposal = proposal
        rn.template = notification_template
        rn.to_address = proposal.speaker_email
        rn.from_address = request.POST["from_address"]
        rn.subject = request.POST["subject"]
        rn.body = Template(request.POST["body"]).render(
            Context({
                "proposal": proposal.notification_email_context()
            })
        )
        rn.save()
        emails.append(rn.email_args)

    send_mass_mail(emails)

    return redirect("result_notification", section_slug=section_slug, status=status)


# DOCUMENT VIEWS #############################################################
# @@@|TODO write class-based views for these

@login_required
def document_create(request, proposal_pk):
    proposal = get_object_or_404(ProposalBase, pk=proposal_pk, submitter=request.user)
    proposal = ProposalBase.objects.get_subclass(pk=proposal.pk)
    #queryset = ProposalBase.objects.select_related("speaker")
    #proposal = get_object_or_404(queryset, pk=proposal_pk)
    #proposal = ProposalBase.objects.get_subclass(pk=proposal.pk)

    if proposal.cancelled:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = SupportingDocumentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.submission = proposal
            document.uploaded_by = request.user
            document.save()
            return redirect("reviews:reviews_detail", proposal.pk)
    else:
        form = SupportingDocumentCreateForm()

    return render(request, "app_list/proposal/document_create.html", {
        "submission": proposal,
        "form": form,
    })


@login_required
def document_download(request, pk, *args):
    document = get_object_or_404(SupportingDocument, pk=pk)
    if getattr(settings, "USE_X_ACCEL_REDIRECT", False):
        response = HttpResponse()
        response["X-Accel-Redirect"] = document.document.url
        del response["content-type"]
    else:
        response = static.serve(
            request,
            document.document.name,
            document_root=settings.MEDIA_ROOT
        )
    return response


@login_required
def document_delete(request, pk):
    document = get_object_or_404(
        SupportingDocument, pk=pk,
        uploaded_by=request.user
    )
    proposal_pk = document.proposal.pk

    if request.method == "POST":
        document.delete()
    return redirect("reviews:reviews_detail", document.submission.pk)
    #return redirect("proposal_detail", proposal_pk)


class ProposalKindList(LoggedInMixin, ListView):
    """
    ListView to provide a list of submission kinds to choose from.

    """

    template_name = "app_list/submissions/submission_submit.html"
    context_object_name = "kinds"

    def get_queryset(self):
        return ProposalKind.objects.all()


class SubmissionAdd(LoggedInMixin, FormView):
    template_name = "app_list/submissions/submission_submit_kind.html"

    def dispatch(self, request, *args, **kwargs):
        self.kind = get_object_or_404(ProposalKind, slug=kwargs.get("kind_slug"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        print(hookset)
        return hookset.get_submission_add_success_url(self.submission)

    def get_form_class(self):
        return settings.PINAX_SUBMISSIONS_FORMS[self.kwargs["kind_slug"]]

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            kind=self.kind,
            kind_slug=self.kind.slug,
            proposal_form=self.get_form(),
            **kwargs
        )

    def form_valid(self, form):
        self.submission = form.save(commit=False)
        self.submission.submitter = self.request.user
        self.submission.kind = self.kind
        self.submission.save()
        form.save_m2m()
        messages.success(self.request, _("Submission submitted."))
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # @@@|TODO change this message
        messages.error(
            self.request,
            _("All fields are required.  Please correct errors and resubmit.")
        )
        context = self.get_context_data()
        context["proposal_form"] = form
        return self.render_to_response(context)


class SubmissionEdit(LoggedInMixin, UpdateView):

    template_name = "app_list/submissions/submission_edit.html"

    def get_success_url(self):
        return hookset.get_submission_edit_success_url(self.submission)

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        submission = get_object_or_404(ProposalBase, pk=pk)
        submission = ProposalBase.objects.get_subclass(pk=submission.pk)

        if self.request.user != submission.submitter:
            raise Http404()

        if not submission.can_edit():
            ctx = {
                "title": "Submission editing closed",
                "body": "Submission editing is closed for this session type."
            }
            return render(
                self.request,
                "app_list/submissions/submission_error.html",
                ctx
            )
        return submission

    def get_form_class(self):
        return settings.PINAX_SUBMISSIONS_FORMS[self.get_object().kind.slug]

    def get_context_data(self, **kwargs):
        return super().get_context_data(submission=self.get_object(), **kwargs)

    def form_valid(self, form):
        self.submission = form.save()
        if hasattr(self.submission, "reviews"):
            users = get_user_model().objects.filter(
                Q(review__submission=self.submission) |
                Q(submissionmessage__submission=self.submission)
            )
            users = users.exclude(pk=self.request.user.pk).distinct()
            for user in users:
                ctx = {
                    "user": self.request.user,
                    "submission": self.submission,
                }
                hookset.send_email(
                    [user.email],
                    "submission_updated",
                    context=ctx
                )
        messages.success(self.request, "Submission updated.")
        return redirect(self.get_success_url())


class SubmissionDetail(LoggedInMixin, DetailView):

    template_name = "app_list/submissions/submission_detail.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        submission = get_object_or_404(
            ProposalBase,
            pk=pk,
            submitter=self.request.user
        )
        submission = ProposalBase.objects.get_subclass(pk=submission.pk)
        return submission

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = SubmitterCommentForm(self.request.POST)

        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        submission = self.get_object()
        message = form.save(commit=False)
        message.user = self.request.user
        message.submission = submission
        message.save()

        reviewers = get_user_model().objects.filter(
            id__in=ProposalMessage.objects.filter(
                submission=submission
            ).exclude(
                user=self.request.user
            ).distinct().values_list("user", flat=True)
        )

        for reviewer in reviewers:
            ctx = {
                "submission": submission,
                "message": message,
                "reviewer": True,
            }
            hookset.send_email(
                [reviewer.email],
                "submission_new_message",
                context=ctx
            )

        return redirect(self.request.path)

    def form_invalid(self, form):
        messages.error(self.request, _("Comment Form failed."))
        return self.render_to_response(
            self.get_context_data(message_form=form)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context["submission"] = self.object
        context["message_form"] = SubmitterCommentForm(instance=self.object)
        return context


class SubmissionCancel(LoggedInMixin, DetailView):

    template_name = "app_list/submissions/submission_cancel.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        submission = get_object_or_404(
            ProposalBase,
            pk=pk,
            submitter=self.request.user
        )
        submission = ProposalBase.objects.get_subclass(pk=submission.pk)
        return submission

    def post(self, request, *args, **kwargs):
        submission = self.get_object()
        submission.cancel()
        # @@@|TODO fire off email to submitter and other speakers
        messages.success(request, "Submission has been cancelled")
        return redirect(hookset.get_submission_cancel_success_url(submission))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context["submission"] = self.object
        return context


# REVIEW VIEWS ################################################################


def access_not_permitted(request):
    return render(request, "app_list/reviews/access_not_permitted.html")


class Reviews(LoggedInMixin, CanReviewMixin, ListView):
    """
    Returns a list of all proposals, proposals reviewed by the user, or the
    proposals the user has yet to review depending on the link user clicks in
    dashboard

    """

    template_name = "app_list/reviews/review_list.html"
    assigned = False
    reviewed = "all"
    context_object_name = "reviews"
    queryset = ProposalBase.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.queryset

        if self.assigned:
            assignments = ReviewAssignment.objects.filter(
                user=self.request.user
            ).values_list("submission__id")
            queryset = queryset.filter(id__in=assignments)

        # passing reviewed in from reviews.urls and out to review_list for
        # appropriate template header rendering
        if self.reviewed == "all":
            queryset = queryset.select_related("result").select_subclasses()
            reviewed = "all_reviews"
        elif self.reviewed == "reviewed":
            queryset = queryset.filter(reviews__user=self.request.user)
            reviewed = "user_reviewed"
        else:
            queryset = queryset.exclude(
                reviews__user=self.request.user
            ).exclude(submitter=self.request.user)
            reviewed = "user_not_reviewed"

        reviews = reviews_generator(self.request, queryset)

        context["reviewed"] = reviewed
        context["reviews"] = reviews

        return context


class ReviewList(LoggedInMixin, CanReviewMixin, ListView):

    template_name = "app_list/reviews/review_list.html"
    context_object_name = "reviews"

    def get_queryset(self):
        queryset = ProposalBase.objects.select_related("result")
        reviewed = Review.objects.filter(
            user__pk=self.kwargs["user_pk"]
        ).values_list("review", flat=True)
        queryset = queryset.filter(pk__in=reviewed)
        reviews = queryset.order_by("submitted")
        reviews = reviews_generator(self.request, reviews, user_pk=self.kwargs["user_pk"])
        return reviews


class ReviewAdmin(LoggedInMixin, CanReviewMixin, ListView):

    template_name = "app_list/reviews/review_admin.html"
    context_object_name = "reviewers"

    def get_queryset(self):
        return hookset.reviewers()


class ReviewDetail(LoggedInMixin, CanReviewMixin, DetailView):

    template_name = "app_list/reviews/review_detail.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        reviews = ProposalBase.objects.select_related("result").select_subclasses()
        reviews = get_object_or_404(reviews, pk=pk)
        return reviews

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        admin = self.request.user.is_staff
        message_form = SubmitterCommentForm(self.request.POST)
        if "message_submit" in request.POST:
            if message_form.is_valid():
                return self.form_valid(message_form)
        elif "result_submit" in request.POST:
            if admin:
                result = request.POST["result_submit"]
                self.object.update_result(result)
            return redirect(request.path)

    def form_valid(self, form):
        message = form.save(commit=False)
        message.user = self.request.user
        message.submission = self.object
        message.save()
        return redirect(self.request.path)

    def form_invalid(self, form):
        initial = {}
        review_form = ReviewForm(initial=initial)
        return self.render_to_response(
            self.get_context_data(review_form=review_form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submission = self.get_object()
        reviews = Review.objects.filter(
            submission=submission
        ).order_by("-submitted_at")
        messages = submission.messages.order_by("submitted_at")

        context["submission"] = submission
        context["reviews"] = reviews
        context["review_messages"] = messages
        context["review_form"] = ReviewForm(initial={})
        context["message_form"] = SubmitterCommentForm()
        return context


class ReviewDelete(LoggedInMixin, CanReviewMixin, DeleteView):
    model = Review
    success_url = "reviews:review_detail"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url, pk=self.object.proposal.pk)


class CreateProductReview(CreateView):
    template_name = "oscar/catalogue/reviews/review_form.html"
    model = ProductReview
    product_model = Product
    form_class = ProductReviewForm
    view_signal = review_added

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(
            self.product_model, pk=kwargs['product_pk'], is_public=True)
        # check permission to leave review
        if not self.product.is_review_permitted(request.user):
            if self.product.has_review_by(request.user):
                message = _("You have already reviewed this product!")
            else:
                message = _("You can't leave a review for this product.")
            messages.warning(self.request, message)
            return redirect(self.product.get_absolute_url())

        return super().dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['product'] = self.product
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_signal(self.request, response, self.object)
        return response

    def get_success_url(self):
        messages.success(
            self.request, _("Thank you for reviewing this product"))
        return self.product.get_absolute_url()

    def send_signal(self, request, response, review):
        self.view_signal.send(sender=self, review=review, user=request.user,
                              request=request, response=response)


class ProductReviewDetail(DetailView):
    template_name = "oscar/catalogue/reviews/review_detail.html"
    context_object_name = 'review'
    model = ProductReview

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(
            Product, pk=self.kwargs['product_pk'], is_public=True)
        return context


class AddVoteView(View):
    """
    Simple view for voting on a review.

    We use the URL path to determine the product and review and use a 'delta'
    POST variable to indicate it the vote is up or down.
    """

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'], is_public=True)
        review = get_object_or_404(ProductReview, pk=self.kwargs['pk'])

        form = VoteForm(review, request.user, request.POST)
        if form.is_valid():
            if form.is_up_vote:
                review.vote_up(request.user)
            elif form.is_down_vote:
                review.vote_down(request.user)
            messages.success(request, _("Thanks for voting!"))
        else:
            for error_list in form.errors.values():
                for msg in error_list:
                    messages.error(request, msg)
        return redirect_to_referrer(request, product.get_absolute_url())


class ProductReviewList(ListView):
    """
    Browse reviews for a product
    """
    template_name = 'oscar/catalogue/reviews/review_list.html'
    context_object_name = "reviews"
    model = ProductReview
    product_model = Product
    paginate_by = settings.OSCAR_REVIEWS_PER_PAGE

    def get_queryset(self):
        qs = self.model.objects.approved().filter(product=self.kwargs['product_pk'])
        self.form = SortReviewsForm(self.request.GET)
        if self.request.GET and self.form.is_valid():
            sort_by = self.form.cleaned_data['sort_by']
            if sort_by == SortReviewsForm.SORT_BY_RECENCY:
                return qs.order_by('-date_created')
        return qs.order_by('-score')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(
            self.product_model, pk=self.kwargs['product_pk'], is_public=True)
        context['form'] = self.form
        return context