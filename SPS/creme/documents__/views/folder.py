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

import logging

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
)
from django.views.generic.detail import (
    SingleObjectMixin,
    SingleObjectTemplateResponseMixin,
)
from django.views.generic.edit import FormMixin, ProcessFormView

from ...creme_core.gui import listview  as lv_gui
from ...creme_core.auth import build_creation_perm as cperm
from ...creme_core.views import generic
from ...creme_core.views.generic import base

from .. import custom_forms, get_folder_model, gui
from ..constants import DEFAULT_HFILTER_FOLDER
from ..compat import LoginRequiredMixin
from ..forms.folder import (
    ColleagueFolderShareForm,
    FolderCreateForm,
)
from ..hooks import hookset

logger = logging.getLogger(__name__)
Folder = get_folder_model()


class FolderCreation(generic.EntityCreation):
    model = Folder
    form_class = custom_forms.FOLDER_CREATION_CFORM


class ChildFolderCreation(base.EntityRelatedMixin, generic.EntityCreation):
    model = Folder
    form_class = custom_forms.FOLDER_CREATION_CFORM
    entity_id_url_kwarg = 'parent_id'
    entity_classes = Folder
    title = _('Create a sub-folder for «{entity}»')

    def check_view_permissions(self, user):
        super().check_view_permissions(user=user)
        user.has_perm_to_link_or_die(Folder, owner=None)

    def get_form_class(self):
        form_cls = super().get_form_class()

        class ChildFolderForm(form_cls):
            def __init__(self, entity, *args, **kwargs):
                super().__init__(*args, **kwargs)
                del self.fields['parent_folder']
                self.instance.parent_folder = entity

        return ChildFolderForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.set_entity_in_form_kwargs(kwargs)

        return kwargs

    def get_title_format_data(self):
        data = super().get_title_format_data()
        data['entity'] = self.get_related_entity().allowed_str(self.request.user)

        return data


# TODO: no CHANGE credentials for parent ?
# TODO: link-popup.html ?
class ChildFolderCreationPopup(generic.AddingInstanceToEntityPopup):
    model = Folder
    form_class = custom_forms.FOLDER_CREATION_CFORM
    permissions = ['documents', cperm(Folder)]
    title = _('Create a sub-folder for «{entity}»')
    entity_id_url_kwarg = 'folder_id'
    entity_classes = Folder

    def check_view_permissions(self, user):
        super().check_view_permissions(user=user)
        user.has_perm_to_link_or_die(Folder, owner=None)

    # TODO: factorise
    def get_form_class(self):
        form_cls = super().get_form_class()

        class ChildFolderForm(form_cls):
            def __init__(self, entity, *args, **kwargs):
                super().__init__(*args, **kwargs)
                del self.fields['parent_folder']
                self.instance.parent_folder = entity

        return ChildFolderForm


class FolderDetail(generic.EntityDetail):
    model = Folder
    template_name = 'documents/view_folder.html'
    pk_url_kwarg = 'folder_id'


class FolderEdition(generic.EntityEdition):
    model = Folder
    form_class = custom_forms.FOLDER_EDITION_CFORM
    pk_url_kwarg = 'folder_id'


class FoldersList(generic.EntitiesList):
    model = Folder
    default_headerfilter_id = DEFAULT_HFILTER_FOLDER

    child_title = _('List of sub-folders for «{parent}»')

    def __init__(self):
        super().__init__()
        self.parent_folder = False  # False means 'never retrieved'

    def get_buttons(self):
        return super().get_buttons()\
                      .update_context(parent_folder=self.get_parent_folder())\
                      .insert(0, gui.ParentFolderButton)\
                      .replace(old=lv_gui.CreationButton, new=gui.FolderCreationButton)

    def get_parent_folder(self):
        parent = self.parent_folder

        if parent is False:
            # TODO: POST only for POST requests ? only GET ?
            request = self.request
            parent = None
            parent_id = request.POST.get('parent_id') or request.GET.get('parent_id')

            if parent_id is not None:
                try:
                    parent_id = int(parent_id)
                except (ValueError, TypeError):
                    logger.warning(
                        'Folder.listview(): invalid "parent_id" parameter: %s',
                        parent_id,
                    )
                else:
                    parent = get_object_or_404(Folder, pk=parent_id)
                    request.user.has_perm_to_view_or_die(parent)

        self.parent_folder = parent

        return parent

    def get_sub_title(self):
        parent = self.parent_folder

        if parent is not None:
            ancestors = parent.get_parents()

            if ancestors:
                ancestors.reverse()
                ancestors.append(parent)
                return ' > '.join(f.title for f in ancestors)

        return ''

    def get_title(self):
        parent = self.parent_folder

        return super().get_title() if parent is None else self.child_title.format(parent=parent)

    def get_internal_q(self):
        return Q(parent_folder=self.get_parent_folder())


#class of app_list
class FolderCreate(LoginRequiredMixin, CreateView):
    model = Folder
    form_class = FolderCreateForm
    template_name = "app_list/documents/folder_create.html"
    parent = None
#
    def get(self, request, *args, **kwargs):
        if "p" in request.GET:
            qs = self.model.objects.for_user(request.user)
            self.parent = get_object_or_404(qs, pk=request.GET["p"])
        else:
            self.parent = None
        return super().get(request, *args, **kwargs)
#
    def get_context_data(self, **kwargs):
        kwargs.setdefault("parent", self.parent)
        return super().get_context_data(**kwargs)
#
    def get_initial(self):
        if self.parent:
            self.initial["parent"] = self.parent
        return super().get_initial()
#
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"folders": self.model.objects.for_user(self.request.user)})
        return kwargs
#
    def create_folder(self, **kwargs):
        folder = self.model.objects.create(**kwargs)
        folder.touch(self.request.user)
        # if folder is not amongst anything shared it will share with no
        # users which share will no-op; perhaps not the best way?
        folder.share(folder.shared_parent().shared_with())
        return folder
#
    def form_valid(self, form):
        kwargs = {
            "name": form.cleaned_data["name"],
            "author": self.request.user,
            "parent": form.cleaned_data["parent"],
        }
        self.object = self.create_folder(**kwargs)
        hookset.folder_created_message(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class FolderDetail(LoginRequiredMixin, DetailView):
    model = Folder
    template_name = "app_list/documents/folder_detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.for_user(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ctx = {
            "members": self.object.members(user=self.request.user),
            "can_share": self.object.can_share(self.request.user),
        }
        context.update(ctx)
        return context


class FolderShare(LoginRequiredMixin,
                  SingleObjectTemplateResponseMixin,
                  FormMixin,
                  SingleObjectMixin,
                  ProcessFormView):
    model = Folder
    context_object_name = "folder"
    form_class = ColleagueFolderShareForm
    template_name = "app_list/documents/folder_share.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.for_user(self.request.user)
        return qs

    def get_object(self):
        folder = super().get_object()
        if not folder.can_share(self.request.user):
            raise Http404(_(f"Cannot share folder '{folder}'."))
        return folder

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        can_share_with = hookset.share_with_options(self.request.user, self.object)
        kwargs.update({"colleagues": can_share_with})
        return kwargs

    def form_valid(self, form):
        self.object.share(form.cleaned_data["participants"])
        hookset.folder_shared_message(self.request, self.request.user, self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("documents:folder_detail", args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ctx = {
            "participants": self.object.shared_with(),
        }
        context.update(ctx)
        return context


class FolderDelete(LoginRequiredMixin, DeleteView):
    model = Folder
    success_url = reverse_lazy("documents:document_index")
    template_name = "app_list/documents/folder_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        hookset.folder_pre_delete(self.request, self.get_object())
        success_url = super().delete(request, *args, **kwargs)
        hookset.folder_deleted_message(self.request, self.object)
        return success_url