################################################################################
#    Creme is a free/open-source Customer Relationship Management software
#    Copyright (C) 2009-2022  Hybird
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
from __future__ import annotations
import json
from django.db.models import Q
from django.forms import BaseForm, ModelChoiceField
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext

from datetime import datetime, timedelta
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ...creme_core.common.models import Attachments
from ...comments.models import Comment
# from ..creme_core.common.custom_auth import JSONWebTokenAuthentication
from ...creme_core.common.serializer import (
    AttachmentsSerializer,
    CommentSerializer,
    ProfileSerializer,
    TeamsSerializer,
    ContactSerializer,
)
from .. import swagger_params
from ..models import Event
from ..serializer import EventCreateSerializer, EventSerializer
from ..tasks import send_email
from ...persons.models import Teams, Profile, Contact
from ...creme_core.models import CremeUser

from ...creme_core.gui import listview as lv_gui
from ...persons import constants as persons_constants
from ... import persons
from ...creme_core.actions import ViewAction
from ...creme_core.core.entity_cell import EntityCellRelation
from ...creme_core.gui.actions import EntityAction
from ...creme_core.models import Relation, RelationType
from ...creme_core.utils import get_from_POST_or_404
from ...creme_core.views import generic
from ...creme_core.views.generic.base import EntityRelatedMixin
from ...opportunities import get_opportunity_model
from ...opportunities.custom_forms import OPPORTUNITY_CREATION_CFORM
from ...persons.views.contact import ContactsList

from .. import constants, custom_forms, get_event_model, gui
from ..forms import event as event_forms
from ..models import EventType

Contact = persons.get_contact_model()
Organisation = persons.get_organisation_model()
Event = get_event_model()
Opportunity = get_opportunity_model()


class AddRelatedOpportunityAction(EntityAction):
    id = EntityAction.generate_id('events', 'create_related_opportunity')
    model = Contact

    type = 'redirect'
    url_name = 'events__create_related_opportunity'

    label = _('Create an opportunity')
    icon = 'opportunity'

    def __init__(self, event, **kwargs):
        super().__init__(**kwargs)
        self.event = event

    @property
    def url(self):
        return reverse(self.url_name, args=(self.event.id, self.instance.id))

    @property
    def is_enabled(self):
        user = self.user

        return (
            user.has_perm_to_create(Opportunity) and user.has_perm_to_link(self.event)
        )


class EventCreation(generic.EntityCreation):
    model = Event
    form_class = custom_forms.EVENT_CREATION_CFORM

    def get_initial(self):
        initial = super().get_initial()
        initial['type'] = EventType.objects.first()

        return initial


class EventDetail(generic.EntityDetail):
    model = Event
    template_name = 'events/view_event.html'
    pk_url_kwarg = 'event_id'


class EventEdition(generic.EntityEdition):
    model = Event
    form_class = custom_forms.EVENT_EDITION_CFORM
    pk_url_kwarg = 'event_id'


class EventsList(generic.EntitiesList):
    model = Event
    default_headerfilter_id = constants.DEFAULT_HFILTER_EVENT


class RelatedContactsList(EntityRelatedMixin, ContactsList):
    entity_id_url_kwarg = 'event_id'
    entity_classes = Event

    title = _('List of contacts related to «{event}»')

    RTYPE_IDS = (
        constants.REL_SUB_IS_INVITED_TO,
        constants.REL_SUB_ACCEPTED_INVITATION,
        constants.REL_SUB_REFUSED_INVITATION,
        constants.REL_SUB_CAME_EVENT,
        constants.REL_SUB_NOT_CAME_EVENT,
    )

    def check_related_entity_permissions(self, entity, user):
        user.has_perm_to_view_or_die(entity)  # NB: entity == event

    def get_actions_registry(self):
        view_action_class = next(
            (
                c
                for c in self.actions_registry.instance_action_classes(model=Contact)
                if (issubclass(c, ViewAction))
            ),
            None
        )

        registry = gui.RelatedContactsActionsRegistry(event=self.get_related_entity())
        registry.register_instance_actions(AddRelatedOpportunityAction)

        if view_action_class is not None:
            registry.register_instance_actions(view_action_class)

        return registry

    def get_buttons(self):
        # TODO: let BatchProcessButton when it manages the internal Q
        # TODO: let MassImportButton when we can set a fixed relation to the event
        # TODO: let MassExportHeaderButton when MassImportButton is here
        return super().get_buttons()\
                      .update_context(event_entity=self.get_related_entity()) \
                      .insert(0, gui.EventDetailButton) \
                      .replace(old=lv_gui.CreationButton, new=gui.AddContactsButton) \
                      .remove(lv_gui.BatchProcessButton) \
                      .remove(lv_gui.MassImportButton) \
                      .remove(lv_gui.MassExportHeaderButton)

    def get_cells(self, hfilter):
        cells = super().get_cells(hfilter=hfilter)

        rtypes = RelationType.objects.filter(pk__in=self.RTYPE_IDS)

        # NB: add relations items to use the pre-cache system of HeaderFilter
        #     (TODO: problem: retrieve other related events too)
        cells.extend(
            EntityCellRelation(model=Contact, rtype=rtype, is_hidden=True)
            for rtype in rtypes
        )

        event = self.get_related_entity()
        cells.append(gui.EntityCellVolatileInvitation(event=event))
        cells.append(gui.EntityCellVolatilePresence(event=event))

        return cells

    def get_internal_q(self):
        return Q(
            relations__type__in=self.RTYPE_IDS,
            relations__object_entity=self.get_related_entity().id,
        )

    def get_title_format_data(self):
        return {
            'event': self.get_related_entity(),
        }


class AddContactsToEvent(generic.EntityEdition):
    model = Event
    form_class: type[BaseForm] = event_forms.AddContactsToEventForm
    template_name = 'creme_core/generics/blockform/link.html'
    pk_url_kwarg = 'event_id'
    title = _('Link some contacts to «{object}»')
    submit_label = _('Link these contacts')


class RelatedOpportunityCreation(generic.EntityCreation):
    model = Opportunity
    form_class = OPPORTUNITY_CREATION_CFORM
    permissions = 'events'
    title = _('Create an opportunity related to «{contact}»')
    event_id_url_kwarg = 'event_id'
    contact_id_url_kwarg = 'contact_id'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = None
        self.contact = None

    def get_contact(self):
        contact = self.contact
        if contact is None:
            self.contact = contact = get_object_or_404(
                Contact, pk=self.kwargs[self.contact_id_url_kwarg],
            )
            self.request.user.has_perm_to_view_or_die(contact)

        return contact

    def get_event(self):
        event = self.event
        if event is None:
            self.event = event = get_object_or_404(
                Event, pk=self.kwargs[self.event_id_url_kwarg],
            )
            self.request.user.has_perm_to_link_or_die(event)

        return event

    def get_form_class(self):
        form_cls = super().get_form_class()

        class RelatedOpportunityCreationForm(form_cls):
            def __init__(this, event, contact, *args, **kwargs):
                super().__init__(*args, **kwargs)
                fields = this.fields
                this.event = event

                qs = Organisation.objects.filter(
                    relations__type__in=[
                        persons_constants.REL_OBJ_EMPLOYED_BY,
                        persons_constants.REL_OBJ_MANAGES,
                    ],
                    relations__object_entity=contact.id,
                )

                description_f = fields.get('description')
                if description_f:
                    description_f.initial = gettext(
                        'Generated by the event «{}»'
                    ).format(event)

                if not qs:
                    fields[this.target_cell_key].help_text = gettext(
                        '(The contact «{}» is not related to an organisation).'
                    ).format(contact)
                else:
                    fields[this.target_cell_key] = ModelChoiceField(
                        label=pgettext('events-opportunity', 'Target organisation'),
                        queryset=qs,
                        empty_label=None,
                    )

            def _get_relations_to_create(this):
                instance = this.instance

                return super()._get_relations_to_create().append(Relation(
                    user=instance.user,
                    subject_entity=instance,
                    type_id=constants.REL_SUB_GEN_BY_EVENT,
                    object_entity=this.event,
                ))

        return RelatedOpportunityCreationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['event'] = self.get_event()
        kwargs['contact'] = self.get_contact()

        return kwargs

    def get_title_format_data(self):
        data = super().get_title_format_data()
        data['contact'] = self.get_contact()
        # data['event'] = self.get_event()  TODO ?

        return data


class BaseStatusSetting(generic.CheckedView):
    permissions = 'events'
    status_map = constants.INV_STATUS_MAP
    status_arg = 'status'
    event_id_url_kwarg = 'event_id'
    contact_id_url_kwarg = 'contact_id'

    def check_contact_permissions(self, contact, user):
        user.has_perm_to_link_or_die(contact)

    def check_event_permissions(self, event, user):
        user.has_perm_to_link_or_die(event)

    def get_contact(self):
        contact = get_object_or_404(Contact, pk=self.kwargs[self.contact_id_url_kwarg])
        self.check_contact_permissions(contact, self.request.user)

        return contact

    def get_event(self):
        event = get_object_or_404(Event, pk=self.kwargs[self.event_id_url_kwarg])
        self.check_event_permissions(event, self.request.user)

        return event

    def get_status(self):
        status = get_from_POST_or_404(self.request.POST, self.status_arg, cast=int)

        if status not in self.status_map:
            raise Http404(f'Unknown status: {status}')

        return status

    def post(self, *args, **kwargs):
        self.update(
            status=self.get_status(),
            event=self.get_event(),
            contact=self.get_contact(),
        )

        return HttpResponse()

    def update(self, *, event, contact, status):
        raise NotImplementedError


class InvitationStatusSetting(BaseStatusSetting):
    def update(self, *, event, contact, status):
        event.set_invitation_status(contact=contact, status=status, user=self.request.user)


class PresenceStatusSetting(BaseStatusSetting):
    def update(self, *, event, contact, status):
        event.set_presence_status(contact=contact, status=status, user=self.request.user)



class EventListView(APIView, LimitOffsetPagination):
    model = Event
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_context_data(self, **kwargs):
        params = self.request.post_data
        queryset = self.model.objects.filter(org=self.request.org).order_by("-id")
        contacts = Contact.objects.filter(org=self.request.org)
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            queryset = queryset.filter(
                Q(assigned_to__in=[self.request.profile])
                | Q(created_by=self.request.profile)
            )
            contacts = contacts.filter(
                Q(created_by=self.request.profile) | Q(assigned_to=self.request.profile)
            ).distinct()

        if params:
            if params.get("name"):
                queryset = queryset.filter(name__icontains=params.get("name"))
            if params.get("created_by"):
                queryset = queryset.filter(created_by=params.get("created_by"))
            if params.getlist("assigned_users"):
                queryset = queryset.filter(
                    assigned_to__id__in=json.loads(params.get("assigned_users"))
                )
            if params.get("date_of_meeting"):
                queryset = queryset.filter(
                    date_of_meeting=params.get("date_of_meeting")
                )
        context = {}
        results_events = self.paginate_queryset(queryset, self.request, view=self)
        events = EventSerializer(results_events, many=True).data
        if results_events:
            offset = queryset.filter(id__gte=results_events[-1].id).count()
            if offset == queryset.count():
                offset = None
        else:
            offset = 0
        context.update({"events_count": self.count, "offset": offset})
        context["events"] = events
        context["recurring_days"] = WEEKDAYS
        context["contacts_list"] = ContactSerializer(contacts, many=True).data
        return context

    @swagger_auto_schema(
        tags=["Events"], manual_parameters=swagger_params.event_list_get_params
    )
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return Response(context)

    @swagger_auto_schema(
        tags=["Events"], manual_parameters=swagger_params.event_create_post_params
    )
    def post(self, request, *args, **kwargs):
        params = request.post_data
        data = {}
        serializer = EventCreateSerializer(data=params, request_obj=request)
        if serializer.is_valid():
            start_date = params.get("start_date")
            end_date = params.get("end_date")
            recurring_days = json.dumps(params.get("recurring_days"))
            if params.get("event_type") == "Non-Recurring":
                event_obj = serializer.save(
                    created_by=request.profile,
                    date_of_meeting=params.get("start_date"),
                    is_active=True,
                    disabled=False,
                    org=request.org,
                )

                if params.get("contacts"):
                    obj_contact = Contact.objects.filter(
                        id=params.get("contacts"), org=request.org
                    )
                    event_obj.contacts.add(obj_contact)

                if params.get("teams"):
                    teams_list = json.loads(params.get("teams"))
                    teams = settings.PERSONS_TEAM_MODEL.objects.filter(id__in=teams_list, org=request.org)
                    event_obj.teams.add(*teams)

                if params.get("assigned_to"):
                    assinged_to_list = json.loads(params.get("assigned_to"))
                    profiles = Profile.objects.filter(
                        id__in=assinged_to_list, org=request.org
                    )
                    event_obj.assigned_to.add(*profiles)

                assigned_to_list = list(
                    event_obj.assigned_to.all().values_list("id", flat=True)
                )
                send_email.delay(
                    event_obj.id,
                    assigned_to_list,
                )
            if params.get("event_type") == "Recurring":
                recurring_days = params.get("recurring_days")
                if not recurring_days:
                    return Response(
                        {"error": True, "errors": "Choose atleast one recurring day"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

                delta = end_date - start_date
                required_dates = []

                for day in range(delta.days + 1):
                    each_date = start_date + timedelta(days=day)
                    if each_date.strftime("%A") in recurring_days:
                        required_dates.append(each_date)

                for each in required_dates:
                    each = datetime.strptime(str(each), "%Y-%m-%d").date()
                    data = serializer.validated_data

                    event = Event.objects.create(
                        created_by=request.profile,
                        start_date=start_date,
                        end_date=end_date,
                        name=data["name"],
                        event_type=data["event_type"],
                        description=data["description"],
                        start_time=data["start_time"],
                        end_time=data["end_time"],
                        date_of_meeting=each,
                        org=request.org,
                    )

                    if params.get("contacts"):
                        obj_contact = Contact.objects.filter(
                            id=params.get("contacts"), org=request.org
                        )
                        event.contacts.add(obj_contact)

                    if params.get("teams"):
                        teams_list = json.loads(params.get("teams"))
                        teams = settings.PERSONS_TEAM_MODEL.objects.filter(id__in=teams_list, org=request.org)
                        event.teams.add(*teams)

                    if params.get("assigned_to"):
                        assinged_to_list = json.loads(params.get("assigned_to"))
                        profiles = Profile.objects.filter(
                            id__in=assinged_to_list, org=request.org
                        )
                        event.assigned_to.add(*profiles)

                    assigned_to_list = list(
                        event.assigned_to.all().values_list("id", flat=True)
                    )
                    send_email.delay(
                        event.id,
                        assigned_to_list,
                    )
            return Response(
                {"error": False, "message": "Event Created Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": True, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class EventDetailView(APIView):
    model = Event
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        return Event.objects.get(pk=pk)

    def get_context_data(self, **kwargs):
        context = {}
        user_assgn_list = [
            assigned_to.id for assigned_to in self.event_obj.assigned_to.all()
        ]
        if self.request.profile == self.event_obj.created_by:
            user_assgn_list.append(self.request.profile.id)
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            if self.request.profile.id not in user_assgn_list:
                return Response(
                    {
                        "error": True,
                        "errors": "You don't have Permission to perform this action",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        comments = Comment.objects.filter(event=self.event_obj).order_by("-id")
        attachments = Attachments.objects.filter(event=self.event_obj).order_by("-id")
        assigned_data = self.event_obj.assigned_to.values("id", "user__email")
        if self.request.profile.is_admin or self.request.profile.role == "ADMIN":
            users_mention = list(
                Profile.objects.filter(
                    is_active=True,
                ).values("user__username")
            )
        elif self.request.profile != self.event_obj.created_by:
            users_mention = [{"username": self.event_obj.created_by.user.username}]
        else:
            users_mention = list(
                self.event_obj.assigned_to.all().values("user__username")
            )
        profile_list = Profile.objects.filter(is_active=True, org=self.request.org)
        if self.request.profile.role == "ADMIN" or self.request.profile.is_admin:
            profiles = profile_list.order_by("user__email")
        else:
            profiles = profile_list.filter(role="ADMIN").order_by("user__email")

        if self.request.profile == self.event_obj.created_by:
            user_assgn_list.append(self.request.profile.id)
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            if self.request.profile.id not in user_assgn_list:
                return Response(
                    {
                        "error": True,
                        "errors": "You don't have Permission to perform this action",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        team_ids = [user.id for user in self.event_obj.get_team_users]
        all_user_ids = profiles.values_list("id", flat=True)
        users_excluding_team_id = set(all_user_ids) - set(team_ids)
        users_excluding_team = Profile.objects.filter(id__in=users_excluding_team_id)

        selected_recurring_days = Event.objects.filter(
            name=self.event_obj.name
        ).values_list("date_of_meeting", flat=True)
        selected_recurring_days = set(
            [day.strftime("%A") for day in selected_recurring_days]
        )
        context.update(
            {
                "event_obj": EventSerializer(self.event_obj).data,
                "attachments": AttachmentsSerializer(attachments, many=True).data,
                "comments": CommentSerializer(comments, many=True).data,
                "selected_recurring_days": selected_recurring_days,
                "users_mention": users_mention,
                "assigned_data": assigned_data,
            }
        )

        context["users"] = ProfileSerializer(profiles, many=True).data
        context["users_excluding_team"] = ProfileSerializer(
            users_excluding_team, many=True
        ).data
        context["teams"] = TeamsSerializer(Teams.objects.all(), many=True).data
        return context

    @swagger_auto_schema(
        tags=["Events"], manual_parameters=swagger_params.organization_params
    )
    def get(self, request, pk, **kwargs):
        self.event_obj = self.get_object(pk)
        if self.event_obj.org != request.org:
            return Response(
                {"error": True, "errors": "User company doesnot match with header...."},
                status=status.HTTP_403_FORBIDDEN,
            )
        context = self.get_context_data(**kwargs)
        return Response(context)

    @swagger_auto_schema(
        tags=["Events"], manual_parameters=swagger_params.event_detail_post_params
    )
    def post(self, request, pk, **kwargs):
        params = request.post_data
        context = {}
        self.event_obj = Event.objects.get(pk=pk)
        if self.event_obj.org != request.org:
            return Response(
                {
                    "error": True,
                    "errors": "User company does not match with header....",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            if not (
                (self.request.profile == self.event_obj.created_by)
                or (self.request.profile in self.event_obj.assigned_to.all())
            ):
                return Response(
                    {
                        "error": True,
                        "errors": "You don't have Permission to perform this action",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        comment_serializer = CommentSerializer(data=params)
        if comment_serializer.is_valid():
            if params.get("comment"):
                comment_serializer.save(
                    event_id=self.event_obj.id,
                    commented_by_id=self.request.profile.id,
                )

        if self.request.FILES.get("event_attachment"):
            attachment = Attachments()
            attachment.created_by = self.request.profile
            attachment.file_name = self.request.FILES.get("event_attachment").name
            attachment.event = self.event_obj
            attachment.attachment = self.request.FILES.get("event_attachment")
            attachment.save()

        comments = Comment.objects.filter(event__id=self.event_obj.id).order_by("-id")
        attachments = Attachments.objects.filter(event__id=self.event_obj.id).order_by(
            "-id"
        )
        context.update(
            {
                "event_obj": EventSerializer(self.event_obj).data,
                "attachments": AttachmentsSerializer(attachments, many=True).data,
                "comments": CommentSerializer(comments, many=True).data,
            }
        )
        return Response(context)

    @swagger_auto_schema(
        tags=["Events"], manual_parameters=swagger_params.event_create_post_params
    )
    def put(self, request, pk, **kwargs):
        params = request.post_data
        data = {}
        self.event_obj = self.get_object(pk)
        if self.event_obj.org != request.org:
            return Response(
                {"error": True, "errors": "User company doesnot match with header...."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = EventCreateSerializer(
            data=params,
            instance=self.event_obj,
            request_obj=request,
        )
        if serializer.is_valid():
            event_obj = serializer.save()
            previous_assigned_to_users = list(
                event_obj.assigned_to.all().values_list("id", flat=True)
            )
            if params.get("event_type") == "Non-Recurring":
                event_obj.date_of_meeting = event_obj.start_date

            event_obj.contacts.clear()
            if params.get("contacts"):
                obj_contact = Contact.objects.filter(
                    id=params.get("contacts"), org=request.org
                )
                event_obj.contacts.add(obj_contact)

            event_obj.teams.clear()
            if params.get("teams"):
                teams_list = json.loads(params.get("teams"))
                teams = settings.PERSONS_TEAM_MODEL.objects.filter(id__in=teams_list, org=request.org)
                event_obj.teams.add(*teams)

            event_obj.assigned_to.clear()
            if params.get("assigned_to"):
                assinged_to_list = json.loads(params.get("assigned_to"))
                profiles = Profile.objects.filter(
                    id__in=assinged_to_list, org=request.org
                )
                event_obj.assigned_to.add(*profiles)

            assigned_to_list = list(
                event_obj.assigned_to.all().values_list("id", flat=True)
            )
            recipients = list(set(assigned_to_list) - set(previous_assigned_to_users))
            send_email.delay(
                event_obj.id,
                recipients,
            )
            return Response(
                {"error": False, "message": "Event updated Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": True, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        tags=["Events"], manual_parameters=swagger_params.organization_params
    )
    def delete(self, request, pk, **kwargs):
        self.object = self.get_object(pk)
        if (
            request.profile.role == "ADMIN"
            or request.profile.is_admin
            or request.profile == self.object.created_by
        ) and self.object.org == request.org:
            self.object.delete()
            return Response(
                {"error": False, "message": "Event deleted Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": True, "errors": "you don't have permission to delete this event"},
            status=status.HTTP_403_FORBIDDEN,
        )


class EventCommentView(APIView):
    model = Comment
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        return self.model.objects.get(pk=pk)

    @swagger_auto_schema(
        tags=["Events"], manual_parameters=swagger_params.event_comment_edit_params
    )
    def put(self, request, pk, format=None):
        params = request.post_data
        obj = self.get_object(pk)
        if (
            request.profile.role == "ADMIN"
            or request.profile.is_admin
            or request.profile == obj.commented_by
        ):
            serializer = CommentSerializer(obj, data=params)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"error": False, "message": "Comment Submitted"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": True, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "error": True,
                "errors": "You don't have Permission to perform this action",
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    @swagger_auto_schema(
        tags=["Events"], manual_parameters=swagger_params.organization_params
    )
    def delete(self, request, pk, format=None):
        self.object = self.get_object(pk)
        if (
            request.profile.role == "ADMIN"
            or request.profile.is_admin
            or request.profile == self.object.commented_by
        ):
            self.object.delete()
            return Response(
                {"error": False, "message": "Comment Deleted Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "error": True,
                "errors": "You don't have Permission to perform this action",
            },
            status=status.HTTP_403_FORBIDDEN,
        )


class EventAttachmentView(APIView):
    model = Attachments
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=["Events"], manual_parameters=swagger_params.organization_params
    )
    def delete(self, request, pk, format=None):
        self.object = self.model.objects.get(pk=pk)
        if (
            request.profile.role == "ADMIN"
            or request.profile.is_admin
            or request.profile == self.object.created_by
        ):
            self.object.delete()
            return Response(
                {"error": False, "message": "Attachment Deleted Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "error": True,
                "errors": "You don't have Permission to perform this action",
            },
            status=status.HTTP_403_FORBIDDEN,
        )
