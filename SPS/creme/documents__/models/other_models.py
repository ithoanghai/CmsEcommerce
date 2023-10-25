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
import math
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from ...creme_core.models import base as core_models
from ..constants import MIMETYPE_PREFIX_IMG
#from ..hooks import hookset

MAXINT = 100000

#def uuid_filename(instance, filename):
#    return hookset.file_upload_to(instance, filename)

class FolderCategory(core_models.MinionModel):
    name = models.CharField(_('Category name'), max_length=100, unique=True)

    creation_label = pgettext_lazy('documents-folder_category', 'Create a category')

    class Meta:
        app_label = 'documents'
        verbose_name = _('Folder category')
        verbose_name_plural = _('Folder categories')
        ordering = ('name',)

    def __str__(self):
        return self.name


class DocumentCategory(core_models.MinionModel):
    name = models.CharField(_('Name'), max_length=100, unique=True)

    creation_label = pgettext_lazy('documents-doc_category', 'Create a category')

    class Meta:
        app_label = 'documents'
        verbose_name = _('Document category')
        verbose_name_plural = _('Document categories')
        ordering = ('name',)

    def __str__(self):
        return self.name


class MimeType(core_models.CremeModel):
    name = models.CharField(_('Name'), max_length=100, unique=True)

    class Meta:
        app_label = 'Documents'
        verbose_name = _('MIME type')
        verbose_name_plural = _('MIME types')
        ordering = ('name',)

    def __str__(self):
        return self.name

    @property
    def is_image(self):
        return self.name.startswith(MIMETYPE_PREFIX_IMG)


class MemberSharedUser(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # @@@ privileges

    class Meta:
        #app_label = "membershareuser"
        abstract = True

    @classmethod
    def for_user(cls, user):
        qs = cls._default_manager.filter(user=user)
        return qs.values_list(cls.obj_attr, flat=True)


class UserStorage(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="storage", on_delete=models.CASCADE)
    bytes_used = models.BigIntegerField(default=0)
    bytes_total = models.BigIntegerField(default=0)

    #class Meta:
    #    app_label = "userstorage"

    @property
    def percentage(self):
        return int(math.ceil((float(self.bytes_used) / self.bytes_total) * 100))

    #@property
    #def color(self):
    #    return hookset.storage_color(self)