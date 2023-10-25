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

from __future__ import annotations

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from ...creme_core.common.utils import ROLES
from ...creme_core.core.exceptions import SpecificProtectedError
from ...creme_core.models import CremeEntity, CremeUser
from ...creme_core.models.fields import PhoneField

from .. import constants, get_profile_model, get_organisation_model
from . import organisation, address

logger = logging.getLogger(__name__)


class AbstractProfile(CremeEntity):
    org = models.ForeignKey(organisation.Organisation, null=True, on_delete=models.CASCADE, blank=True, related_name="user_org").set_tags(optional=True)
    profile_image = models.ImageField(upload_to='avatars', default='avatars/guest.png').set_tags(optional=True)
    cover_image = models.ImageField(upload_to='avatars', default='avatars/cover.png').set_tags(optional=True)
    phone = PhoneField(max_length=20, blank=True, null=True,
                             unique=True).set_tags(optional=True)  # phone = models.CharField(max_length=20, blank=True)
    alternate_phone = PhoneField(max_length=20, null=True).set_tags(optional=True)
    address = models.ForeignKey(address.Address, related_name="adress_users", on_delete=models.CASCADE, blank=True, null=True, ).set_tags(optional=True)
    city = models.CharField(max_length=20, blank=True).set_tags(optional=True)
    country = models.CharField(max_length=20, blank=True).set_tags(optional=True)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True).set_tags(optional=True)
    role = models.CharField(max_length=50, choices=ROLES, default="USER").set_tags(optional=True)
    has_sales_access = models.BooleanField(default=False).set_tags(optional=True)
    has_marketing_access = models.BooleanField(default=False).set_tags(optional=True)
    is_active = models.BooleanField(default=True).set_tags(optional=True)
    is_organization_admin = models.BooleanField(default=False).set_tags(optional=True)
    date_of_joining = models.DateField(null=True, blank=True).set_tags(optional=True)

    creation_label = _('Create a profile')
    save_label     = _('Save the profile')

    class Meta:
        abstract = True
        app_label = 'persons'
        ordering = ('org', 'phone', "-date_of_joining")
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        unique_together = (("city", "org", "phone"),)
        indexes = [
            models.Index(
                fields=['org', 'phone', 'cremeentity_ptr'],
                name='persons__profile__default_lv',
            ),
        ]

    def __str__(self):
        return self.user.username

    def get_profile_image(self):
        if self.profile_image:
            return self.profile_image.url
        return settings.MEDIA_URL + self._meta.get_field('profile_image').get_default()

    def get_cover_image(self):
        if self.cover_image:
            return self.cover_image.url
        return settings.MEDIA_URL + self._meta.get_field('cover_image').get_default()

    def _check_deletion(self):
        if self.is_user is not None:
            raise SpecificProtectedError(
                _('A user is associated with this contact.'),
                [self]
            )

    def clean(self):
        if self.is_user_id:
            if not self.first_name:
                raise ValidationError({
                    'first_name': ValidationError(
                        _('This Profile is related to a user and must have a first name.'),
                        # code='TODO',
                    ),
                })

            if not self.email:
                raise ValidationError({
                    'email': ValidationError(
                        _(
                            'This Profile is related to a user and must have an email address.'
                        ),
                        # code='TODO',
                    ),
                })

            # TODO: should we limit the edition of email? (it could be used to
            #       reset the password -- but happily the History shows who
            #       changed the field).

            if get_user_model()._default_manager.filter(
                is_active=True, email=self.email,
            ).exclude(id=self.is_user_id).exists():
                raise ValidationError({
                    'email': ValidationError(
                        _(
                            'This Profile is related to a user and an active '
                            'user already uses this email address.'
                        ),
                        # code='TODO',
                    ),
                })

    def delete(self, *args, **kwargs):
        self._check_deletion()  # Should not be useful (trashing should be blocked too)
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('persons__view_profile', args=(self.id,))

    @staticmethod
    def get_create_absolute_url():
        return reverse('persons__create_profile')

    def get_edit_absolute_url(self):
        return reverse('persons__edit_profile', args=(self.id,))

    @staticmethod
    def get_lv_absolute_url():
        return reverse('persons__list_profiles')

    # TODO: use FilteredRelation ?
    def get_employers(self) -> models.QuerySet:
        return get_organisation_model().objects.filter(
            is_deleted=False,
            relations__type__in=(constants.REL_OBJ_EMPLOYED_BY, constants.REL_OBJ_MANAGES),
            relations__object_entity=self.id,
        )

    def _post_save_clone(self, source):
        self._aux_post_save_clone(source)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def trash(self):
        self._check_deletion()
        super().trash()

    @classmethod
    def _create_linked_profile(cls, user, **kwargs) -> AbstractProfile:
        # TODO: assert user is not a team + enforce non team clean() ?
        owner = user

        if user.is_staff:
            superuser = type(user)._default_manager.filter(
                is_superuser=True, is_staff=False,
            ).order_by('id').first()

            if superuser is None:
                logger.critical(
                    'No existing super-user found to assign the staff Profile '
                    '(creme_populate has not been run?!) ; you should create a '
                    'super-user & change the owner of this staff Profile in '
                    'order to avoid some broken behaviours (e.g. inner-edition '
                    'fails).'
                )
            else:
                owner = superuser

        return cls.objects.create(
            user=owner,
            is_user=user,
            last_name=user.last_name or user.username.title(),
            first_name=user.first_name or _('N/A'),
            email=user.email or _('complete@Me.com'),
            **kwargs
        )

    @property
    def is_admin(self):
        return self.is_organization_admin


class Profile(AbstractProfile):
    class Meta(AbstractProfile.Meta):
        swappable = 'PERSONS_PROFILE_MODEL'


# Manage the related User ------------------------------------------------------

def _get_linked_profile(self):
    if self.is_team:
        return None

    profile = getattr(self, '_linked_profile_cache', None)

    if profile is None:
        model = get_profile_model()
        profiles = model.objects.filter(is_user=self)[:2]

        if not profiles:
            logger.critical(
                'User "%s" has no related Profile => we create it',
                self.username,
            )
            profile = model._create_linked_profile(self)
        else:
            if len(profiles) > 1:
                # TODO: repair ? (beware to race condition)
                logger.critical(
                    'User "%s" has several related Profiles !',
                    self.username,
                )

            profile = profiles[0]

    self._linked_profile_cache = profile

    return profile


@receiver(post_save, sender=CremeUser)
def create_profile(sender, instance, created, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.create(user=kwargs['instance'])

    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.id])
        user_profile.save()