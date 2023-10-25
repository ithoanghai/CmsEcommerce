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
import itertools

from django.utils import timezone
from random import randint
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.conf import settings  # noqa

from ...creme_core.core.exceptions import SpecificProtectedError
from ...creme_core.models import CREME_REPLACE_NULL, CremeEntity
from ...creme_core.utils import truncate_str

from ..exceptions import DuplicateFolderNameError
from ..hooks import hookset
from ..managers import FolderManager, FolderQuerySet
from .. import constants

from . import other_models
from .other_models import FolderCategory

MAXINT = 100000


class AbstractFolder(CremeEntity):
    """Folder: contains Documents."""
    title = models.CharField(_('Title'), max_length=100)
    parent_folder = models.ForeignKey(
        'self',
        verbose_name=_('Parent folder'),
        blank=True, null=True,
        related_name='children',
        on_delete=models.PROTECT,
    )

    category = models.ForeignKey(
        FolderCategory,
        verbose_name=_('Category'),
        blank=True, null=True,
        on_delete=CREME_REPLACE_NULL,
        related_name='folder_category_set',
        help_text=_("The parent's category will be copied if you do not select one."),
    )

    allowed_related = CremeEntity.allowed_related | {'document'}

    not_deletable_UUIDs = {
        constants.UUID_FOLDER_RELATED2ENTITIES,
        constants.UUID_FOLDER_IMAGES,
    }

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE)
    #created = models.DateTimeField(default=timezone.now)
    #modified = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE)

    objects = FolderManager.from_queryset(FolderQuerySet)()

    kind = "folder"
    icon = "folder-open"
    shared = None

    @classmethod
    def shared_user_model(cls):
        return FolderSharedUser

    @classmethod
    def already_exists(cls, name, parent=None):
        return cls.objects.filter(name=name, parent=parent).exists()

    def save(self, **kwargs):
        if not self.pk and Folder.already_exists(self.name, self.parent):
            raise DuplicateFolderNameError(f"{self.name} already exists in this folder.")
        self.touch(self.author, commit=False)
        super().save(**kwargs)

    def get_absolute_url(self):
        return reverse("documents:folder_detail", args=[self.pk])

    def unique_id(self):
        return "f-%d" % self.id

    def members(self, **kwargs):
        return Folder.objects.members(self, **kwargs)

    def touch(self, user, commit=True):
        self.modified = timezone.now()
        self.modified_by = user
        if commit:
            if self.parent:
                self.parent.touch(user)
            self.save()

    @property
    def size(self):
        """
        Return size of this folder.
        """
        return sum([m.size for m in self.members(direct=False) if m.kind == "document"])

    def breadcrumbs(self):
        """
        Produces a list of ancestors (excluding self).
        """
        crumbs = []
        if self.parent:
            crumbs.extend(self.parent.breadcrumbs())
            crumbs.append(self.parent)
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
        """
        Returns boolean based on whether self should show any shared UI.
        """
        return self.parent_id is None and self.shared

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

    def shared_parent(self):
        """
        Returns the folder object that is the shared parent (the root of
        a shared folder hierarchy) or None if there is no shared parent.
        """
        root = self
        a, b = itertools.tee(reversed(self.breadcrumbs()))
        next(b, None)
        for folder, parent in itertools.zip_longest(a, b):
            if folder.shared:
                root = folder
            if parent is None or not parent.shared:
                break
        return root

    def can_share(self, user):
        """
        Ensures folder is top-level and `user` is the author.
        """
        return hookset.can_share_folder(user, self)

    def share(self, users):
        """
        Ensures self is shared with given users (can accept users who are
        already shared on self).
        """
        users = [u for u in users if not self.shared_with(user=u)]
        if users:
            members = [self] + self.members(direct=False)
            #FM, DM = self.shared_user_model(), Document.shared_user_model()
            fm, dm = [], []
            for member, user in itertools.product(members, users):
                if user.pk == member.author_id:
                    continue
                #if isinstance(member, Folder):
                #    fm.append(FM(**{FM.obj_attr: member, "user": user}))
                #if isinstance(member, Document):
                #    dm.append(DM(**{DM.obj_attr: member, "user": user}))
            #FM._default_manager.bulk_create(fm)
            #DM._default_manager.bulk_create(dm)

    def delete_url(self):
        return reverse(
            "documents:folder_delete",
            args=[self.pk]
        )

    creation_label = _('Create a folder')
    save_label     = _('Save the folder')

    error_messages = {
        'itself': _('«%(folder)s» cannot be its own parent'),
        'loop': _('This folder is one of the child folders of «%(folder)s»'),
    }

    class Meta:
        abstract = True
        app_label = 'Documents'
        unique_together = ('title', 'parent_folder', 'category')
        verbose_name = _('Folder')
        verbose_name_plural = _('Folders')
        ordering = ('title',)

    def __str__(self):
        return self.title

    def _check_deletion(self):
        if str(self.uuid) in self.not_deletable_UUIDs:
            raise SpecificProtectedError(_('This folder is a system folder.'), [self])

    def clean(self):
        if self.pk:
            parent_folder = self.parent_folder
            if parent_folder:
                if parent_folder == self:
                    raise ValidationError({
                        'parent_folder': ValidationError(
                            self.error_messages['itself'],
                            params={'folder': self},
                            code='itself',
                        ),
                    })

                if self.already_in_children(parent_folder.id):
                    raise ValidationError({
                        'parent_folder': ValidationError(
                            self.error_messages['loop'],
                            params={'folder': self},
                            code='loop',
                        ),
                    })

    def get_absolute_url(self):
        return reverse('documents__view_folder', args=(self.id,))

    @staticmethod
    def get_create_absolute_url():
        return reverse('documents__create_folder')

    def get_edit_absolute_url(self):
        return reverse('documents__edit_folder', args=(self.id,))

    @staticmethod
    def get_lv_absolute_url():
        return reverse('documents__list_folders')

    def _pre_save_clone(self, source):
        max_length = self._meta.get_field('title').max_length
        self.title = truncate_str(
            source.title, max_length,
            suffix=' ({} {:08x})'.format(_('Copy'), randint(0, MAXINT)),
        )

        # TODO: atomic
        while Folder.objects.filter(title=self.title).exists():
            self._pre_save_clone(source)

    def already_in_children(self, other_folder_id):
        children = self.children.all()

        for child in children:
            if child.id == other_folder_id:
                return True

        for child in children:
            if child.already_in_children(other_folder_id):
                return True

        return False

    def delete(self, *args, **kwargs):
        self._check_deletion()  # Should not be useful (trashing should be blocked too)
        super().delete(*args, **kwargs)

    def get_parents(self):
        parents = []
        parent = self.parent_folder

        if parent:
            parents.append(parent)
            parents.extend(parent.get_parents())

        return parents

    # def save(self, *args, **kwargs):
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.category and self.parent_folder:
            self.category = self.parent_folder.category
            if update_fields is not None:
                update_fields = {'category', *update_fields}

        # super().save(*args, **kwargs)
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def trash(self):
        self._check_deletion()
        super().trash()


class Folder(AbstractFolder):
    class Meta(AbstractFolder.Meta):
        swappable = 'DOCUMENTS_FOLDER_MODEL'


class FolderSharedUser(other_models.MemberSharedUser):

    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    obj_attr = "folder"

    class Meta:
        #app_label = "foldershareuser"
        unique_together = [("folder", "user")]