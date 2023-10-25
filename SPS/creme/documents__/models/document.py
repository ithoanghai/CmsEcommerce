################################################################################
#    Creme is a free/open-source Customer Relationship Management software
#    Copyright (C) 2009-2023  Hybird
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
import time
import arrow
from mimetypes import guess_type
from os.path import basename

from django.utils import timezone
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django.db.models import F
from django.contrib.auth import get_user_model

from ...creme_core.models import CremeEntity
from ...creme_core.models.utils import assign_2_charfield
from ...creme_core.common.templatetags.common_tags import (is_document_file_audio,
                                             is_document_file_code,
                                             is_document_file_image,
                                             is_document_file_pdf,
                                             is_document_file_sheet,
                                             is_document_file_text,
                                             is_document_file_video,
                                             is_document_file_zip)
from ...persons.models import Profile, Organisation, Teams
from ..managers import DocumentQuerySet
from ..exceptions import DuplicateDocumentNameError
from ..hooks import hookset
from . import other_models

def uuid_filename(instance, filename):
    return hookset.file_upload_to(instance, filename)

def document_path(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("docs", hash_, filename)


class AbstractDocument(CremeEntity):
    title = models.CharField(_('Name'), max_length=100, blank=True)
    filedata = models.FileField(
        _('File'), max_length=500, upload_to='documents',
    )
    linked_folder = models.ForeignKey(
        settings.DOCUMENTS_FOLDER_MODEL, verbose_name=_('Folder'), on_delete=models.PROTECT,
    )
    mime_type = models.ForeignKey(
        other_models.MimeType,
        verbose_name=_('MIME type'), editable=False, on_delete=models.PROTECT, null=True,
    )
    categories = models.ManyToManyField(
        other_models.DocumentCategory, verbose_name=_('Categories'), blank=True,
    ).set_tags(optional=True)

    DOCUMENT_STATUS_CHOICE = (("active", "active"), ("inactive", "inactive"))

    document_file = models.FileField(upload_to=document_path, max_length=5000)
    created_by = models.ForeignKey( Profile, related_name="document_uploaded",on_delete=models.SET_NULL,null=True,blank=True,)
    created_on = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=DOCUMENT_STATUS_CHOICE, max_length=64, default="active")
    shared_to = models.ManyToManyField(Profile, related_name="document_shared_to")
    teams = models.ManyToManyField(settings.PERSONS_TEAM_MODEL, related_name="document_teams")
    org = models.ForeignKey(settings.PERSONS_ORGANISATION_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="document_org",)

    name = models.CharField(max_length=255)
    #folder = models.ForeignKey(Folder, null=True, blank=True, on_delete=models.CASCADE,related_name="document_folder",)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE)
    #created = models.DateTimeField(default=timezone.now)
    #modified = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE)
    file = models.FileField(upload_to=uuid_filename)
    original_filename = models.CharField(max_length=500)

    objects = DocumentQuerySet.as_manager()

    kind = "document"
    icon = "file"
    shared = None

    def file_type(self):
        name_ext_list = self.document_file.url.split(".")
        if len(name_ext_list) > 1:
            ext = name_ext_list[int(len(name_ext_list) - 1)]
            if is_document_file_audio(ext):
                return ("audio", "fa fa-file-audio")
            if is_document_file_video(ext):
                return ("video", "fa fa-file-video")
            if is_document_file_image(ext):
                return ("image", "fa fa-file-image")
            if is_document_file_pdf(ext):
                return ("pdf", "fa fa-file-pdf")
            if is_document_file_code(ext):
                return ("code", "fa fa-file-code")
            if is_document_file_text(ext):
                return ("text", "fa fa-file-alt")
            if is_document_file_sheet(ext):
                return ("sheet", "fa fa-file-excel")
            if is_document_file_zip(ext):
                return ("zip", "fa fa-file-archive")
            return ("file", "fa fa-file")
        return ("file", "fa fa-file")

    @property
    def get_team_users(self):
        team_user_ids = list(self.teams.values_list("users__id", flat=True))
        return Profile.objects.filter(id__in=team_user_ids)

    @property
    def get_team_and_assigned_users(self):
        team_user_ids = list(self.teams.values_list("users__id", flat=True))
        assigned_user_ids = list(self.shared_to.values_list("id", flat=True))
        user_ids = team_user_ids + assigned_user_ids
        return Profile.objects.filter(id__in=user_ids)

    @property
    def get_assigned_users_not_in_teams(self):
        team_user_ids = list(self.teams.values_list("users__id", flat=True))
        assigned_user_ids = list(self.shared_to.values_list("id", flat=True))
        user_ids = set(assigned_user_ids) - set(team_user_ids)
        return Profile.objects.filter(id__in=list(user_ids))

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    def delete(self, *args, **kwargs):
        bytes_to_free = self.size
        super().delete(*args, **kwargs)
        storage_qs = settings.AUTH_USER_MODEL.objects.filter(pk=self.author.storage.pk)
        storage_qs.update(bytes_used=F("bytes_used") - bytes_to_free)

    @classmethod
    def shared_user_model(cls):
        return DocumentSharedUser

    @classmethod
    def already_exists(cls, name, folder=None):
        return cls.objects.filter(name=name, folder=folder).exists()

    def save(self, **kwargs):
        if not self.pk and Document.already_exists(self.name, self.folder):
            raise DuplicateDocumentNameError(f"{self.name} already exists in this folder.")
        self.touch(self.author, commit=False)
        super().save(**kwargs)

    def get_absolute_url(self):
        return reverse("documents:document_detail", args=[self.pk])

    def unique_id(self):
        return "d-%d" % self.id

    def touch(self, user, commit=True):
        self.modified = timezone.now()
        self.modified_by = user
        if commit:
            if self.folder:
                self.folder.touch(user)
            self.save()

    @property
    def size(self):
        return self.file.size

    def breadcrumbs(self):
        crumbs = []
        if self.folder:
            crumbs.extend(self.folder.breadcrumbs())
            crumbs.append(self.folder)
        return crumbs

    def shared_queryset(self):
        """
        Returns queryset of this folder mapped into the shared user model.
        The queryset should only consist of zero or one instances (aka shared
        or not shared.) This method is mostly used for convenience.
        """
        model = self.shared_user_model()
        return model._default_manager.filter(**{model.obj_attr: self})

    @property
    def shared(self):
        """
        Determines if self is shared. This checks the denormalization and
        does not return whether self SHOULD be shared (based on parents.)
        """
        return self.shared_queryset().exists()

    def shared_ui(self):
        return False

    def shared_with(self, user=None):
        """
        Returns a User queryset of users shared on this folder, or, if user
        is given optimizes the check and returns boolean.
        """
        CremeUser = get_user_model()
        qs = self.shared_queryset()
        if user is not None:
            return qs.filter(user=user).exists()
        if not qs.exists():
            return CremeUser.objects.none()
        return CremeUser.objects.filter(pk__in=qs.values("user"))

    def share(self, users):
        users = [u for u in users if not self.shared_with(user=u)]
        if users:
            model = self.shared_user_model()
            objs = []
            for user in users:
                objs.append(self.shared_user_model()(**{model.obj_attr: self, "user": user}))
            model._default_manager.bulk_create(objs)

    def download_url(self):
        return reverse(
            "documents:document_download",
            args=[self.pk]
        )

    def delete_url(self):
        return reverse(
            "documents:document_delete",
            args=[self.pk]
        )


    creation_label = _('Create a document')
    save_label     = _('Save the document')

    class Meta:
        abstract = True
        app_label = 'Documents'
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ('title', "-created_on",)

    def __str__(self):
        return f'{self.linked_folder} - {self.title}'

    def get_absolute_url(self):
        return reverse('documents__view_document', args=(self.id,))

    @staticmethod
    def get_create_absolute_url():
        return reverse('documents__create_document')

    def get_edit_absolute_url(self):
        return reverse('documents__edit_document', args=(self.id,))

    @staticmethod
    def get_lv_absolute_url():
        return reverse('documents__list_documents')

    def get_download_absolute_url(self):
        return reverse(
            'creme_core__download',
            args=(
                self.entity_type_id,
                self.id,
                'filedata',
            )
        )

    def get_entity_summary(self, user):
        if not user.has_perm_to_view(self):
            return self.allowed_str(user)

        if self.mime_type.is_image:
            return format_html(
                '<img class="entity-summary" src="{url}" alt="{name}" title="{name}"/>',
                url=self.get_download_absolute_url(),
                name=self.title,
            )

        return super().get_entity_summary(user)

    def save(self, *args, **kwargs):
        if not self.pk:  # Creation
            mime_name = guess_type(self.filedata.name)[0]

            if mime_name is not None:
                self.mime_type = other_models.MimeType.objects.get_or_create(name=mime_name)[0]

        if not self.title:
            # TODO: manage argument "update_fields"? (title set as creation anyway)
            # TODO: truncate but keep extension if possible ?
            assign_2_charfield(self, 'title', basename(self.filedata.path))

        super().save(*args, **kwargs)


class Document(AbstractDocument):
    class Meta(AbstractDocument.Meta):
        swappable = 'DOCUMENTS_DOCUMENT_MODEL'

class DocumentSharedUser(other_models.MemberSharedUser):

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    obj_attr = "document"

    class Meta:
        #app_label = "documentshareuser"
        unique_together = [("document", "user")]