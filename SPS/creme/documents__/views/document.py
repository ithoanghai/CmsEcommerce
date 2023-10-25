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

from functools import partial

from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.utils.translation import gettext as _
from django.db import transaction
from django.db.models import F
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.views import static
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
)

from ... import documents
from ...creme_core.auth import build_creation_perm as cperm
from ...creme_core.forms.validators import validate_linkable_model
from ...creme_core.models import Relation
from ...creme_core.utils import ellipsis
from ...creme_core.views import generic

from .. import constants, custom_forms
from ..constants import DEFAULT_HFILTER_DOCUMENT
from ..models import FolderCategory, Document, Folder, UserStorage
from ..compat import LoginRequiredMixin
from ..forms.document import (
    DocumentCreateForm,
    DocumentCreateFormWithName,
)
from ..hooks import hookset


Folder = documents.get_folder_model()
Document = documents.get_document_model()


class DocumentCreation(generic.EntityCreation):
    model = Document
    form_class = custom_forms.DOCUMENT_CREATION_CFORM

    def get_initial(self):
        initial = super().get_initial()
        initial['linked_folder'] = Folder.objects.first()

        return initial


class RelatedDocumentCreation(generic.AddingInstanceToEntityPopup):
    model = Document
    form_class = custom_forms.DOCUMENT_CREATION_CFORM
    permissions = ['documents', cperm(Document)]
    title = _('New document for «{entity}»')

    def check_related_entity_permissions(self, entity, user):
        user.has_perm_to_view_or_die(entity)
        user.has_perm_to_link_or_die(entity)

    def check_view_permissions(self, user):
        super().check_view_permissions(user=user)
        user.has_perm_to_link_or_die(Document, owner=None)

    def get_form_class(self):
        form_cls = super().get_form_class()

        class RelatedDocumentCreationForm(form_cls):
            def __init__(this, entity, *args, **kwargs):
                super().__init__(*args, **kwargs)
                this.related_entity = entity
                this.folder_category = None
                this.root_folder = None

                del this.fields['linked_folder']

            def clean_user(this):
                return validate_linkable_model(
                    Document, this.user, owner=this.cleaned_data['user'],
                )

            def clean(this):
                cleaned_data = super().clean()

                if not this._errors:
                    this.folder_category = cat = FolderCategory.objects.filter(
                        uuid=constants.UUID_FOLDER_CAT_ENTITIES,
                    ).first()
                    if cat is None:
                        raise ValidationError(
                            f'Populate script has not been run (unknown folder category '
                            f'uuid={constants.UUID_FOLDER_CAT_ENTITIES}) ; '
                            f'please contact your administrator.'
                        )

                    this.root_folder = folder = Folder.objects.filter(
                        uuid=constants.UUID_FOLDER_RELATED2ENTITIES,
                    ).first()
                    if folder is None:
                        raise ValidationError(
                            f'Populate script has not been run '
                            f'(unknown folder uuid={constants.UUID_FOLDER_RELATED2ENTITIES}) ; '
                            f'please contact your administrator'
                        )

                return cleaned_data

            def _get_relations_to_create(this):
                instance = this.instance

                return super()._get_relations_to_create().append(
                    Relation(
                        subject_entity=this.related_entity.get_real_entity(),
                        type_id=constants.REL_SUB_RELATED_2_DOC,
                        object_entity=instance,
                        user=instance.user,
                    ),
                )

            def _get_folder(this):
                entity = this.related_entity.get_real_entity()
                get_or_create_folder = partial(
                    Folder.objects.get_or_create,
                    category=this.folder_category,
                    defaults={'user': this.cleaned_data['user']},
                )
                model_folder = get_or_create_folder(
                    title=str(entity.entity_type),
                    parent_folder=this.root_folder,
                )[0]

                return get_or_create_folder(
                    title=ellipsis(
                        f'{entity.id}_{entity}',
                        length=Folder._meta.get_field('title').max_length,
                    ),  # Meh
                    parent_folder=model_folder,
                )[0]

            @atomic
            def save(this, *args, **kwargs):
                this.instance.linked_folder = this._get_folder()

                return super().save(*args, **kwargs)

        return RelatedDocumentCreationForm


class DocumentDetail(generic.EntityDetail):
    model = Document
    template_name = 'documents/view_document.html'
    pk_url_kwarg = 'document_id'


class DocumentEdition(generic.EntityEdition):
    model = Document
    form_class = custom_forms.DOCUMENT_EDITION_CFORM
    pk_url_kwarg = 'document_id'


class DocumentsList(generic.EntitiesList):
    model = Document
    default_headerfilter_id = DEFAULT_HFILTER_DOCUMENT


class DocumentCreate(LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentCreateForm
    template_name = "app_list/documents/document_create.html"
    folder = None

    def get(self, request, *args, **kwargs):
        if "f" in request.GET:
            qs = Folder.objects.for_user(request.user)
            self.folder = get_object_or_404(qs, pk=request.GET["f"])
        else:
            self.folder = None
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.setdefault("folder", self.folder)
        return super().get_context_data(**kwargs)

    def get_initial(self):
        if self.folder:
            self.initial["folder"] = self.folder
        return super().get_initial()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"folders": Folder.objects.for_user(self.request.user),
                       "storage": self.request.user.storage})
        return kwargs

    def create_document(self, **kwargs):
        document = self.model.objects.create(**kwargs)
        document.touch(self.request.user)
        if document.folder is not None:
            # if folder is not amongst anything shared it will share with no
            # users which share will no-op; perhaps not the best way?
            document.share(document.folder.shared_parent().shared_with())
        return document

    def increase_usage(self, bytes):
        # increase usage for this user based on document size
        storage_qs = UserStorage.objects.filter(pk=self.request.user.storage.pk)
        storage_qs.update(bytes_used=F("bytes_used") + bytes)

    def get_create_kwargs(self, form):
        return {
            "name": form.cleaned_data["file"].name,
            "original_filename": form.cleaned_data["file"].name,
            "folder": form.cleaned_data["folder"],
            "author": self.request.user,
            "file": form.cleaned_data["file"],
        }

    def form_valid(self, form):
        with transaction.atomic():
            kwargs = self.get_create_kwargs(form)
            self.object = self.create_document(**kwargs)
            hookset.document_created_message(self.request, self.object)
            bytes = form.cleaned_data["file"].size
            self.increase_usage(bytes)
            return HttpResponseRedirect(self.get_success_url())


class DocumentWithCustomNameCreate(DocumentCreate):

    form_class = DocumentCreateFormWithName

    def get_create_kwargs(self, form):
        return {
            "name": form.cleaned_data["name"],
            "original_filename": form.cleaned_data["file"].name,
            "folder": form.cleaned_data["folder"],
            "author": self.request.user,
            "file": form.cleaned_data["file"],
        }


class DocumentDetailApp(LoginRequiredMixin, DetailView):
    model = Document
    template_name = "app_list/documents/document_detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.for_user(self.request.user)
        return qs


class DocumentDownload(LoginRequiredMixin, DetailView):
    model = Document

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.for_user(self.request.user)
        return qs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if settings.DOCUMENTS_USE_X_ACCEL_REDIRECT:
            response = HttpResponse()
            response["X-Accel-Redirect"] = self.object.file.url
            # delete content-type to allow Gondor to determine the filetype and
            # we definitely don't want Django's crappy default :-)
            del response["content-type"]
        else:
            # Note:
            #
            # The 'django.views.static.py' docstring states:
            #
            #     Views and functions for serving static files. These are only to be used
            #     during development, and SHOULD NOT be used in a production setting.
            #
            response = static.serve(request, self.object.file.name,
                                    document_root=settings.MEDIA_ROOT)
        return response


class DocumentDelete(LoginRequiredMixin, DeleteView):
    model = Document
    success_url = reverse_lazy("documents:document_index")
    template_name = "app_list/documents/document_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        success_url = super().delete(request, *args, **kwargs)
        hookset.document_deleted_message(self.request, self.object)
        return success_url
