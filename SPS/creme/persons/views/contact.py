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
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.db.models import Q
from django.conf import settings

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ...creme_core.common.serializer import *
from ...creme_core.common.utils import COUNTRIES
# from ...creme_core.common.custom_auth import JSONWebTokenAuthentication
from ...tasks.serializer import TaskSerializer
from ... import persons
from ...creme_core.core.exceptions import ConflictError
from ...creme_core.forms.validators import validate_linkable_model
from ...creme_core.gui.custom_form import CustomFormDescriptor
from ...creme_core.models import Relation, RelationType
from ...creme_core.views import generic

from ..models import (Profile, Teams, AbstractOrganisation)
from .. import swagger_params
from ..tasks import send_email_to_assigned_user
from .. import custom_forms
from ..constants import DEFAULT_HFILTER_CONTACT
from ..forms import contact as c_forms
from ..models import AbstractOrganisation

Contact = persons.get_contact_model()
Organisation = persons.get_organisation_model()


class _ContactBaseCreation(generic.EntityCreation):
    model = Contact
    form_class: type[forms.BaseForm] | CustomFormDescriptor = \
        custom_forms.CONTACT_CREATION_CFORM


class ContactCreation(_ContactBaseCreation):
    pass


class RelatedContactCreation(_ContactBaseCreation):
    title = _('Create a contact related to «{organisation}»')
    orga_id_url_kwarg = 'orga_id'
    rtype_id_url_kwarg = 'rtype_id'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.linked_orga = None

    def get(self, *args, **kwargs):
        self.linked_orga = self.get_linked_orga()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.linked_orga = self.get_linked_orga()
        return super().post(*args, **kwargs)

    def check_view_permissions(self, user):
        super().check_view_permissions(user=user)
        self.request.user.has_perm_to_link_or_die(Contact)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        rtype = self.get_rtype()
        if rtype:
            kwargs['forced_relations'] = [
                Relation(object_entity=self.linked_orga, type=rtype),
            ]

        return kwargs

    def get_form_class(self):
        form_cls = super().get_form_class()
        rtype = self.get_rtype()

        if rtype:
            return form_cls

        linked_orga = self.linked_orga
        get_ct = ContentType.objects.get_for_model

        class RelatedContactForm(form_cls):
            rtype_for_organisation = forms.ModelChoiceField(
                label=_('Status in «{organisation}»').format(
                    organisation=linked_orga,
                ),
                # TODO: factorise (see User form hooking)
                queryset=RelationType.objects.filter(
                    subject_ctypes=get_ct(Contact),
                    symmetric_type__subject_ctypes=get_ct(Organisation),
                    is_internal=False,
                    enabled=True,
                ),
            )

            blocks = form_cls.blocks.new({
                'id': 'relation_to_orga',
                'label': 'Status in organisation',
                'fields': ['rtype_for_organisation'],
                'order': 0,
            })

            def clean_rtype_for_organisation(this):
                rtype = this.cleaned_data['rtype_for_organisation']

                this._check_properties([rtype])  # Checks subject's properties

                needed_object_ptypes = rtype.object_properties.all()
                if needed_object_ptypes:
                    object_prop_ids = {
                        prop.type_id for prop in self.linked_orga.get_properties()
                    }
                    object_missing_ptypes = [
                        ptype
                        for ptype in needed_object_ptypes
                        if ptype.id not in object_prop_ids
                    ]

                    if object_missing_ptypes:
                        raise ValidationError(
                            _(
                                'The entity «%(entity)s» has no property «%(property)s» which is '
                                'required by the relationship «%(predicate)s».'
                            ) % {
                                'entity': self.linked_orga,
                                'property': object_missing_ptypes[0],
                                'predicate': rtype.predicate,
                            }
                        )

                forbidden_object_ptype_ids = {
                    *rtype.object_forbidden_properties.values_list('id', flat=True),
                }
                if forbidden_object_ptype_ids:
                    object_refused_ptypes = [
                        prop.type
                        for prop in self.linked_orga.get_properties()
                        if prop.type_id in forbidden_object_ptype_ids
                    ]

                    if object_refused_ptypes:
                        raise ValidationError(
                            _(
                                'The entity «%(entity)s» has the property «%(property)s» '
                                'which is forbidden by the relationship «%(predicate)s».'
                            ) % {
                                'entity': self.linked_orga,
                                'property': object_refused_ptypes[0],
                                'predicate': rtype.predicate,
                            }
                        )

                return rtype

            def clean_user(this):
                super().clean_user()

                return validate_linkable_model(
                    Contact, this.user, owner=this.cleaned_data['user'],
                )

            def _get_relations_to_create(this):
                relations = super()._get_relations_to_create()
                rtype = this.cleaned_data.get('rtype_for_organisation')
                instance = this.instance

                if rtype:
                    # TODO: check properties constraints?
                    relations.append(Relation(
                        subject_entity=instance,
                        type=rtype,
                        object_entity=self.linked_orga,
                        user=instance.user,
                    ))

                return relations

        return RelatedContactForm

    def get_linked_orga(self) -> AbstractOrganisation:
        orga = get_object_or_404(Organisation, id=self.kwargs[self.orga_id_url_kwarg])

        user = self.request.user
        user.has_perm_to_view_or_die(orga)  # Displayed in the form....
        user.has_perm_to_link_or_die(orga)

        return orga

    def get_rtype(self) -> RelationType | None:
        rtype_id = self.kwargs.get(self.rtype_id_url_kwarg)

        if rtype_id:
            rtype = get_object_or_404(RelationType, id=rtype_id)
            rtype.is_not_internal_or_die()
            rtype.is_enabled_or_die()

            if not rtype.is_compatible(self.linked_orga):
                raise ConflictError(
                    'This RelationType is not compatible with Organisation as subject'
                )

            if not rtype.symmetric_type.is_compatible(Contact):
                raise ConflictError(
                    'This RelationType is not compatible with Contact as relationship-object'
                )

            return rtype.symmetric_type

        return None

    def get_title_format_data(self):
        data = super().get_title_format_data()
        data['organisation'] = self.linked_orga

        return data


class ContactDetail(generic.EntityDetail):
    model = Contact
    template_name = 'persons/view_contact.html'
    pk_url_kwarg = 'contact_id'


class ContactEdition(generic.EntityEdition):
    model = Contact
    form_class: type[forms.BaseForm] | CustomFormDescriptor = \
        custom_forms.CONTACT_EDITION_CFORM
    pk_url_kwarg = 'contact_id'


class ContactNamesEdition(generic.EntityEditionPopup):
    model = Contact
    form_class: type[c_forms.ContactNamesForm] = c_forms.ContactNamesForm
    pk_url_kwarg = 'contact_id'


class ContactsList(generic.EntitiesList):
    model = Contact
    default_headerfilter_id = DEFAULT_HFILTER_CONTACT


class ContactsListView(APIView, LimitOffsetPagination):
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Contact

    def get_context_data(self, request, **kwargs):
        params = request.post_data
        queryset = self.model.objects.filter(org=self.request.org).order_by("-id")
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            queryset = queryset.filter(
                Q(assigned_to__in=[self.request.profile])
                | Q(created_by=self.request.profile)
            ).distinct()

        if params:
            if params.get("name"):
                queryset = queryset.filter(first_name__icontains=params.get("name"))
            if params.get("city"):
                queryset = queryset.filter(address__city__icontains=params.get("city"))
            if params.get("phone"):
                queryset = queryset.filter(mobile_number__icontains=params.get("phone"))
            if params.get("email"):
                queryset = queryset.filter(primary_email__icontains=params.get("email"))
            if params.getlist("assigned_to"):
                queryset = queryset.filter(
                    assigned_to__id__in=json.loads(params.get("assigned_to"))
                ).distinct()

        context = {}
        results_contact = self.paginate_queryset(
            queryset.distinct(), self.request, view=self
        )
        contacts = ContactSerializer(results_contact, many=True).data
        if results_contact:
            offset = queryset.filter(id__gte=results_contact[-1].id).count()
            if offset == queryset.count():
                offset = None
        else:
            offset = 0
        context["per_page"] = 10
        page_number = (int(self.offset / 10) + 1,)
        context["page_number"] = page_number
        context.update({"contacts_count": self.count, "offset": offset})
        context["contact_obj_list"] = contacts
        context["countries"] = COUNTRIES
        users = Profile.objects.filter(is_active=True, org=self.request.org).values(
            "id", "user__email"
        )
        context["users"] = users

        return context

    @swagger_auto_schema(
        tags=["contacts"], manual_parameters=swagger_params.contact_list_get_params
    )
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return Response(context)

    @swagger_auto_schema(
        tags=["contacts"], manual_parameters=swagger_params.contact_create_post_params
    )
    def post(self, request, *args, **kwargs):
        params = request.post_data
        contact_serializer = CreateContactSerializer(data=params, request_obj=request)
        address_serializer = BillingAddressSerializer(data=params)

        data = {}
        if not contact_serializer.is_valid():
            data["contact_errors"] = contact_serializer.errors
        if not address_serializer.is_valid():
            data["address_errors"] = (address_serializer.errors,)
        if data:
            return Response(
                {"error": True, "errors": data},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # if contact_serializer.is_valid() and address_serializer.is_valid():
        address_obj = address_serializer.save()
        contact_obj = contact_serializer.save(date_of_birth=params.get("date_of_birth"))
        contact_obj.address = address_obj
        contact_obj.created_by = self.request.profile
        contact_obj.org = request.org
        contact_obj.save()

        if params.get("teams"):
            teams_list = json.loads(params.get("teams"))
            teams = settings.PERSONS_TEAM_MODEL.objects.filter(id__in=teams_list, org=request.org)
            contact_obj.teams.add(*teams)

        if params.get("assigned_to"):
            assinged_to_list = json.loads(params.get("assigned_to"))
            profiles = Profile.objects.filter(id__in=assinged_to_list, org=request.org)
            contact_obj.assigned_to.add(*profiles)

        recipients = list(contact_obj.assigned_to.all().values_list("id", flat=True))
        send_email_to_assigned_user.delay(
            recipients,
            contact_obj.id,
        )

        if request.FILES.get("contact_attachment"):
            attachment = Attachments()
            attachment.created_by = request.profile
            attachment.file_name = request.FILES.get("contact_attachment").name
            attachment.contact = contact_obj
            attachment.attachment = request.FILES.get("contact_attachment")
            attachment.save()
        return Response(
            {"error": False, "message": "Contact created Successfuly"},
            status=status.HTTP_200_OK,
        )


class ContactDetailView(APIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Contact

    def get_object(self, pk):
        return get_object_or_404(Contact, pk=pk)

    @swagger_auto_schema(
        tags=["contacts"], manual_parameters=swagger_params.contact_create_post_params
    )
    def put(self, request, pk, format=None):
        params = request.post_data
        contact_obj = self.get_object(pk=pk)
        address_obj = contact_obj.address
        if contact_obj.org != request.org:
            return Response(
                {"error": True, "errors": "User company doesnot match with header...."},
                status=status.HTTP_403_FORBIDDEN,
            )
        contact_serializer = CreateContactSerializer(
            data=params, instance=contact_obj, request_obj=request
        )
        address_serializer = BillingAddressSerializer(data=params, instance=address_obj)
        data = {}
        if not contact_serializer.is_valid():
            data["contact_errors"] = contact_serializer.errors
        if not address_serializer.is_valid():
            data["address_errors"] = (address_serializer.errors,)
        if data:
            data["error"] = True
            return Response(
                data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if contact_serializer.is_valid():
            if (
                self.request.profile.role != "ADMIN"
                and not self.request.profile.is_admin
            ):
                if not (
                    (self.request.profile == contact_obj.created_by)
                    or (self.request.profile in contact_obj.assigned_to.all())
                ):
                    return Response(
                        {
                            "error": True,
                            "errors": "You do not have Permission to perform this action",
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

            address_obj = address_serializer.save()
            contact_obj = contact_serializer.save(
                date_of_birth=params.get("date_of_birth")
            )
            contact_obj.address = address_obj
            contact_obj.save()
            contact_obj = contact_serializer.save()
            contact_obj.teams.clear()
            if params.get("teams"):
                teams_list = json.loads(params.get("teams"))
                teams = settings.PERSONS_TEAM_MODEL.objects.filter(id__in=teams_list, org=request.org)
                contact_obj.teams.add(*teams)

            contact_obj.assigned_to.clear()
            if params.get("assigned_to"):
                assinged_to_list = json.loads(params.get("assigned_to"))
                profiles = Profile.objects.filter(
                    id__in=assinged_to_list, org=request.org
                )
                contact_obj.assigned_to.add(*profiles)

            previous_assigned_to_users = list(
                contact_obj.assigned_to.all().values_list("id", flat=True)
            )

            assigned_to_list = list(
                contact_obj.assigned_to.all().values_list("id", flat=True)
            )
            recipients = list(set(assigned_to_list) - set(previous_assigned_to_users))
            send_email_to_assigned_user.delay(
                recipients,
                contact_obj.id,
            )
            if request.FILES.get("contact_attachment"):
                attachment = Attachments()
                attachment.created_by = request.profile
                attachment.file_name = request.FILES.get("contact_attachment").name
                attachment.contact = contact_obj
                attachment.attachment = request.FILES.get("contact_attachment")
                attachment.save()
            return Response(
                {"error": False, "message": "Contact Updated Successfully"},
                status=status.HTTP_200_OK,
            )

    @swagger_auto_schema(
        tags=["contacts"], manual_parameters=swagger_params.organization_params
    )
    def get(self, request, pk, format=None):
        context = {}
        contact_obj = self.get_object(pk)
        context["contact_obj"] = ContactSerializer(contact_obj).data
        user_assgn_list = [
            assigned_to.id for assigned_to in contact_obj.assigned_to.all()
        ]
        user_assigned_accounts = set(
            self.request.profile.account_assigned_users.values_list("id", flat=True)
        )
        contact_accounts = set(
            contact_obj.account_contacts.values_list("id", flat=True)
        )
        if user_assigned_accounts.intersection(contact_accounts):
            user_assgn_list.append(self.request.profile.id)
        if self.request.profile == contact_obj.created_by:
            user_assgn_list.append(self.request.profile.id)
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            if self.request.profile.id not in user_assgn_list:
                return Response(
                    {
                        "error": True,
                        "errors": "You do not have Permission to perform this action",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        assigned_data = []
        for each in contact_obj.assigned_to.all():
            assigned_dict = {}
            assigned_dict["id"] = each.user.id
            assigned_dict["name"] = each.user.email
            assigned_data.append(assigned_dict)

        if self.request.profile.is_admin or self.request.profile.role == "ADMIN":
            users_mention = list(
                Profile.objects.filter(is_active=True, org=request.org).values(
                    "user__username"
                )
            )
        elif self.request.profile != contact_obj.created_by:
            users_mention = [{"username": contact_obj.created_by.user.username}]
        else:
            users_mention = list(contact_obj.assigned_to.all().values("user__username"))

        if request.profile == contact_obj.created_by:
            user_assgn_list.append(self.request.profile.id)

        context["address_obj"] = BillingAddressSerializer(contact_obj.address).data
        context["countries"] = COUNTRIES
        context.update(
            {
                "comments": CommentSerializer(
                    contact_obj.contact_comments.all(), many=True
                ).data,
                "attachments": AttachmentsSerializer(
                    contact_obj.contact_attachment.all(), many=True
                ).data,
                "assigned_data": assigned_data,
                "tasks": TaskSerializer(
                    contact_obj.contacts_tasks.all(), many=True
                ).data,
                "users_mention": users_mention,
            }
        )
        return Response(context)

    @swagger_auto_schema(
        tags=["contacts"], manual_parameters=swagger_params.organization_params
    )
    def delete(self, request, pk, format=None):
        self.object = self.get_object(pk)
        if self.object.org != request.org:
            return Response(
                {"error": True, "errors": "User company doesnot match with header...."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if (
            self.request.profile.role != "ADMIN"
            and not self.request.profile.is_admin
            and self.request.profile != self.object.created_by
        ):
            return Response(
                {
                    "error": True,
                    "errors": "You don't have permission to perform this action.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        if self.object.address_id:
            self.object.address.delete()
        self.object.delete()
        return Response(
            {"error": False, "message": "Contact Deleted Successfully."},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        tags=["contacts"], manual_parameters=swagger_params.contact_detail_get_params
    )
    def post(self, request, pk, **kwargs):
        params = request.post_data
        context = {}
        self.contact_obj = Contact.objects.get(pk=pk)
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            if not (
                (self.request.profile == self.contact_obj.created_by)
                or (self.request.profile in self.contact_obj.assigned_to.all())
            ):
                return Response(
                    {
                        "error": True,
                        "errors": "You do not have Permission to perform this action",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        comment_serializer = CommentSerializer(data=params)
        if comment_serializer.is_valid():
            if params.get("comment"):
                comment_serializer.save(
                    contact_id=self.contact_obj.id,
                    commented_by_id=self.request.profile.id,
                    org=request.org,
                )

        if self.request.FILES.get("contact_attachment"):
            attachment = Attachments()
            attachment.created_by = self.request.profile
            attachment.file_name = self.request.FILES.get("contact_attachment").name
            attachment.contact = self.contact_obj
            attachment.attachment = self.request.FILES.get("contact_attachment")
            attachment.save()

        comments = Comment.objects.filter(contact__id=self.contact_obj.id).order_by(
            "-id"
        )
        attachments = Attachments.objects.filter(
            contact__id=self.contact_obj.id
        ).order_by("-id")
        context.update(
            {
                "contact_obj": ContactSerializer(self.contact_obj).data,
                "attachments": AttachmentsSerializer(attachments, many=True).data,
                "comments": CommentSerializer(comments, many=True).data,
            }
        )
        return Response(context)


class ContactCommentView(APIView):
    model = Comment
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        return self.model.objects.get(pk=pk)

    @swagger_auto_schema(
        tags=["contacts"], manual_parameters=swagger_params.contact_comment_edit_params
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
                "errors": "You don't have permission to edit this Comment",
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    @swagger_auto_schema(
        tags=["contacts"], manual_parameters=swagger_params.organization_params
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
                "errors": "You don't have permission to perform this action",
            },
            status=status.HTTP_403_FORBIDDEN,
        )


class ContactAttachmentView(APIView):
    model = Attachments
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=["contacts"], manual_parameters=swagger_params.organization_params
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
                "errors": "You don't have permission to delete this Attachment",
            },
            status=status.HTTP_403_FORBIDDEN,
        )