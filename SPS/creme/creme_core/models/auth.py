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

import datetime
import time
import arrow
import pytz
import functools
import operator
import logging
import uuid

from collections import OrderedDict, defaultdict
from functools import reduce
from operator import or_ as or_op
from typing import TYPE_CHECKING

# import pytz
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    _user_has_perm,
    AbstractUser, AnonymousUser, PermissionsMixin, UserManager,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models
from django.db.models import Q, QuerySet
from django.utils.functional import partition
from django.utils.timezone import now, zoneinfo
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as trans
from django.utils.text import slugify
from django import forms
from django.db import models, transaction
from django.utils import timezone, translation
from django.urls import reverse
from django.contrib.sites.models import Site
from urllib.parse import urlencode

from ..auth import EntityCredentials
from ..core.setting_key import UserSettingValueManager
from ..utils.unicode_collation import collator
from .entity import CremeEntity
from .fields import EntityCTypeForeignKey

from ..accounts.signals import signup_code_sent, signup_code_used
from ..accounts.conf import settings
from ..accounts.fields import TimeZoneField
from ..accounts.languages import DEFAULT_LANGUAGE
from ..accounts.managers import EmailAddressManager, EmailConfirmationManager
from ..accounts.hooks import hookset
from ..accounts import signals

if TYPE_CHECKING:
    from typing import DefaultDict, Iterable, Sequence, Type, Union

    from ..core.sandbox import SandboxType

    EntityInstanceOrClass = Union[Type[CremeEntity], CremeEntity]

logger = logging.getLogger(__name__)


def img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("profile_pics", hash_, filename)


class CremeUserManager(BaseUserManager):
    def create_user(self,
                    username,
                    first_name,
                    last_name,
                    email,
                    password=None,
                    **extra_fields):
        "Creates and saves a (Creme)User instance."
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(
            username=username,
            first_name=first_name, last_name=last_name,
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.clean()
        user.save()

        return user

    def create_superuser(self,
                         username,
                         first_name,
                         last_name,
                         email,
                         password=None,
                         **extra_fields):
        "Creates and saves a superuser."
        extra_fields['is_superuser'] = True

        return self.create_user(
            username=username,
            first_name=first_name, last_name=last_name,
            email=email,
            password=password,
            **extra_fields
        )

    # TODO: create_staff_user ??

    def get_admin(self):
        user_qs = self.get_queryset().order_by('id')

        return (
            user_qs.filter(is_superuser=True, is_staff=False).first()
            or user_qs.filter(is_superuser=True).first()
            or user_qs[0]
        )


class UserRole(models.Model):
    name = models.CharField(gettext('Name'), max_length=100, unique=True)
    # superior = ForeignKey('self', verbose_name=_('Superior'), null=True)
    # TODO: CTypeManyToManyField ?
    creatable_ctypes = models.ManyToManyField(
        ContentType, verbose_name=gettext('Creatable resources'),
        related_name='roles_allowing_creation',  # TODO: '+' ?
    )
    exportable_ctypes = models.ManyToManyField(
        ContentType, verbose_name=gettext('Exportable resources'),
        related_name='roles_allowing_export',  # TODO: '+' ?
    )
    raw_allowed_apps = models.TextField(default='')  # Use 'allowed_apps' property
    raw_admin_4_apps = models.TextField(default='')  # Use 'admin_4_apps' property

    creation_label = gettext('Create a role')
    save_label     = gettext('Save the role')

    class Meta:
        app_label = 'creme_core'
        verbose_name = gettext('Role')
        verbose_name_plural = gettext('Roles')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._allowed_apps: set[str] | None = None
        self._extended_allowed_apps: set[str] | None = None

        self._admin_4_apps: set[str] | None = None
        self._extended_admin_4_apps: set[str] | None = None

        self._creatable_ctypes_set: frozenset[int] | None = None
        self._exportable_ctypes_set: frozenset[int] | None = None

        self._setcredentials: list[SetCredentials] | None = None

    def __str__(self):
        return self.name

    @property
    def admin_4_apps(self) -> set[str]:
        if self._admin_4_apps is None:
            self._admin_4_apps = {
                app_name
                for app_name in self.raw_admin_4_apps.split('\n')
                if app_name
            }

        return self._admin_4_apps

    @admin_4_apps.setter
    def admin_4_apps(self, apps: Sequence[str]) -> None:
        """@param apps: Sequence of app labels (strings)."""
        self._admin_4_apps = {*apps}
        self.raw_admin_4_apps = '\n'.join(apps)

    @property
    def allowed_apps(self) -> set[str]:
        if self._allowed_apps is None:
            self._allowed_apps = {
                app_name
                for app_name in self.raw_allowed_apps.split('\n')
                if app_name
            }

        # TODO: FrozenSet to avoid modifications ?
        return self._allowed_apps

    @allowed_apps.setter
    def allowed_apps(self, apps: Sequence[str]) -> None:
        """@param apps: Sequence of app labels (strings)."""
        self._allowed_apps = {*apps}
        self.raw_allowed_apps = '\n'.join(apps)

    @staticmethod
    def _build_extended_apps(apps: Iterable[str]) -> set[str]:
        from ..apps import extended_app_configs

        return {app_config.label for app_config in extended_app_configs(apps)}

    @property
    def extended_admin_4_apps(self) -> set[str]:
        if self._extended_admin_4_apps is None:
            self._extended_admin_4_apps = self._build_extended_apps(self.admin_4_apps)

        return self._extended_admin_4_apps

    @property
    def extended_allowed_apps(self) -> set[str]:
        if self._extended_allowed_apps is None:
            self._extended_allowed_apps = self._build_extended_apps(self.allowed_apps)

        return self._extended_allowed_apps

    def is_app_administrable(self, app_name: str) -> bool:  # TODO: rename "app_label"
        return app_name in self.extended_admin_4_apps

    # TODO: rename "app_label"
    def is_app_allowed_or_administrable(self, app_name: str) -> bool:
        return (app_name in self.extended_allowed_apps) or self.is_app_administrable(app_name)

    # TODO: rename app_labels
    def _build_apps_verbose(self, app_names: Iterable[str]) -> list[str]:
        verbose_names = []
        get_app = apps.get_app_config

        for app_label in app_names:
            try:
                app = get_app(app_label)
            except LookupError:
                logger.warning(
                    'The app "%s" seems not registered (from UserRole "%s").',
                    app_label, self,
                )
            else:
                verbose_names.append(app.verbose_name)  # TODO: str() ??

        verbose_names.sort(key=collator.sort_key)

        return verbose_names

    def get_admin_4_apps_verbose(self) -> list[str]:  # For templates
        return self._build_apps_verbose(self.admin_4_apps)

    def get_allowed_apps_verbose(self) -> list[str]:  # For templates
        return self._build_apps_verbose(self.allowed_apps)

    def can_create(self, app_name: str, model_name: str) -> bool:
        """@return True if a model with ContentType(app_name, model_name) can be created."""
        ct = ContentType.objects.get_by_natural_key(app_name, model_name)

        if self._creatable_ctypes_set is None:
            self._creatable_ctypes_set = frozenset(
                self.creatable_ctypes.values_list('id', flat=True)
            )

        return ct.id in self._creatable_ctypes_set

    # TODO: factorise with can_create() ??
    def can_export(self, app_name: str, model_name: str) -> bool:
        """@return True if a model with ContentType(app_name, model_name) can be exported."""
        ct = ContentType.objects.get_by_natural_key(app_name, model_name)

        if self._exportable_ctypes_set is None:
            self._exportable_ctypes_set = frozenset(
                self.exportable_ctypes.values_list('id', flat=True)
            )

        return ct.id in self._exportable_ctypes_set

    def can_do_on_model(self, user, model: CremeEntity, owner, perm: int) -> bool:
        """Can the given user execute an action (VIEW, CHANGE etc..) on this model.
        @param user: User instance ; user that try to do something.
        @param model: Class inheriting CremeEntity
        @param owner: User instance; owner of the not-yet-existing instance of 'model'.
               None means any user that would be allowed to perform the action
               (if it exists of course).
        @param perm: See <EntityCredentials.{VIEW, CHANGE, ...}> .
        """
        return SetCredentials._can_do(self._get_setcredentials(), user, model, owner, perm)

    def _get_setcredentials(self) -> list[SetCredentials]:
        setcredentials = self._setcredentials

        if setcredentials is None:
            logger.debug('UserRole.get_credentials(): Cache MISS for id=%s', self.id)
            self._setcredentials = setcredentials = [*self.credentials.all()]
        else:
            logger.debug('UserRole.get_credentials(): Cache HIT for id=%s', self.id)

        return setcredentials

    def get_perms(self, user, entity: CremeEntity) -> int:
        """@return (can_view, can_change, can_delete, can_link, can_unlink) 5 boolean tuple."""
        real_entity_class = entity.entity_type.model_class()

        if self.is_app_allowed_or_administrable(real_entity_class._meta.app_label):
            perms = SetCredentials.get_perms(self._get_setcredentials(), user, entity)
        else:
            perms = EntityCredentials.NONE

        return perms

    # TODO: factorise
    def filter(self,
               user,
               queryset: QuerySet,
               perm: int,
               ) -> QuerySet:
        """Filter a QuerySet of CremeEntities by the credentials related to this role.
        Beware, the model class must be a child class of CremeEntity,
        but cannot be CremeEntity itself.

        @param user: A <django.contrib.auth.get_user_model()> instance (e.g. CremeUser) ;
                     should be related to the UserRole instance.
        @param queryset: A Queryset on a child class of CremeEntity.
        @param perm: A combination of values in (EntityCredentials.{VIEW, CHANGE} etc...).
               Eg: 'EntityCredentials.DELETE'
                   'EntityCredentials.VIEW | EntityCredentials.CHANGE'
        @return: A new (filtered) queryset on the same model.
        """
        model = queryset.model
        assert issubclass(model, CremeEntity)
        assert model is not CremeEntity

        if self.is_app_allowed_or_administrable(model._meta.app_label):
            queryset = SetCredentials.filter(self._get_setcredentials(), user, queryset, perm)
        else:
            queryset = queryset.none()

        return queryset

    def filter_entities(self,
                        user,
                        queryset: QuerySet,
                        perm: int,
                        as_model: type[CremeEntity] | None = None,
                        ) -> QuerySet:
        """Filter a QuerySet of CremeEntities by the credentials related to this role.
        Beware, model class must be CremeEntity ; it cannot be a child class
        of CremeEntity.

        @param user: A django.contrib.auth.get_user_model() instance (e.g. CremeUser) ;
               should be related to the UserRole instance.
        @param queryset: A Queryset with model=CremeEntity.
        @param perm: A value in EntityCredentials.{VIEW, CHANGE, ...}.
               If the argument "as_model" is not None, you can use a combination
               of values like 'EntityCredentials.VIEW | EntityCredentials.CHANGE'.
        @param as_model: A model inheriting CremeEntity, or None.
               If a model is given, all the entities in the queryset are
               filtered with the credentials for this model.
               BEWARE: you should probably use this feature only if the queryset
               is already filtered by its field 'entity_type' (to keep only
               entities of the right model, & so do not make mistakes with credentials).
        @return: A new (filtered) queryset on the same model.
        @raise: EntityCredentials.FilteringError if there is an EntityFilter,
                which cannot be used on CremeEntity, in the SetCredentials
                concerning the models of the allowed apps.
        """
        assert queryset.model is CremeEntity

        from ..registry import creme_registry

        is_app_allowed = self.is_app_allowed_or_administrable

        return SetCredentials.filter_entities(
            sc_sequence=self._get_setcredentials(),
            user=user, queryset=queryset,
            perm=perm,
            models=[
                model
                for model in creme_registry.iter_entity_models()
                if is_app_allowed(model._meta.app_label)
            ],
            as_model=as_model,
        )


class User(AbstractUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    file_prepend = "users/profile_pics"
    # NB: auth.models.AbstractUser.username max_length == 150 (since django 1.10) => increase too ?
    username = models.CharField(
        gettext('Username'), max_length=30, unique=True,
        help_text=gettext(
            'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': gettext('A user with that username already exists.'),
        },
    )
    first_name = models.CharField(
        gettext('First name'), max_length=100, blank=True,
    ).set_tags(viewable=False)  # NB: blank=True for teams
    last_name = models.CharField(gettext('Last name'), max_length=100, blank=True)
    email = models.EmailField(gettext('Email address'), max_length=150, unique=True, blank=False, error_messages={'unique': "A user with that email already exists.",})
    alternate_email = models.EmailField(max_length=150, null=True)
    gender = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=False)
    about = models.TextField(blank=True)

    displayed_name = models.CharField(
        gettext('Displayed name'),
        max_length=50, blank=True,
        help_text=gettext(
            'If you do not fill this field, an automatic name will be used '
            '(«John Doe» will be displayed as «John D.»).'
        ),
    ).set_tags(viewable=False)

    is_active = models.BooleanField(
        gettext('Active?'), default=True,
    ).set_tags(viewable=False)
    is_staff = models.BooleanField(
        gettext('Is staff?'), default=False
    ).set_tags(viewable=False)
    is_superuser = models.BooleanField(
        gettext('Is a superuser?'), default=False,
    ).set_tags(viewable=False)
    role = models.ForeignKey(
        UserRole, verbose_name=gettext('Role'), null=True, on_delete=models.PROTECT,
    ).set_tags(viewable=False)
    is_team = models.BooleanField(
        verbose_name=gettext('Is a team?'), default=False,
    ).set_tags(viewable=False)
    teammates_set = models.ManyToManyField(
        'self', verbose_name=gettext('Teammates'), symmetrical=False, related_name='teams_set',
    ).set_tags(viewable=False)
    time_zone = models.CharField(
        gettext('Time zone'), max_length=50, default=settings.TIME_ZONE,
        # choices=[(tz, tz) for tz in pytz.common_timezones],
        # TODO: (note from Python's doc)
        #   These values are not designed to be exposed to end-users; for user facing elements,
        #   applications should use something like CLDR (the Unicode Common Locale Data Repository)
        #   to get more user-friendly strings
        choices=[(tz, tz) for tz in zoneinfo.available_timezones()],
    ).set_tags(viewable=False)

    date_joined = models.DateTimeField(
        gettext('Date joined'), auto_now=True,
    ).set_tags(viewable=False)
    theme = models.CharField(
        gettext('Theme'),
        max_length=50, default=settings.THEMES[0][0], choices=settings.THEMES,
    ).set_tags(viewable=False)
    language = models.CharField(
        gettext('Language'), max_length=10,
        default='', blank=True,
        choices=[('', gettext('Language of your browser')), *settings.LANGUAGES],
    ).set_tags(viewable=False)

    profile_pic = models.FileField(max_length=1000, upload_to=img_url, null=True, blank=True )
    activation_key = models.CharField(max_length=150, null=True, blank=True)
    key_expires = models.DateTimeField(null=True, blank=True)
    skype_ID = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True, null=True)


    # NB: do not use directly ; use the property 'settings'
    # TODO: JSONField ?
    json_settings = models.TextField(
        editable=False, default='{}'
    ).set_tags(viewable=False)

    error_messages = {
        'used_email': gettext('An active user with the same email address already exists.'),
    }

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    #USERNAME_FIELD = "email"
    #REQUIRED_FIELDS = ["username"]
    #REQUIRED_FIELDS = ["username", "gender"]

    creation_label = gettext('Create a user')
    save_label = gettext('Save the user')

    _settings: UserSettingValueManager | None = None
    _teams: list[User] | None = None
    _teammates: dict[int, User] | None = None

    objects = CremeUserManager()

    def __unicode__(self):
        return self.email

    class Meta:
        # abstract = True TODO: class AbstractCremeUser ?
        ordering = ('username', "-is_active")
        verbose_name = gettext('User')
        verbose_name_plural = gettext('Users')
        app_label = 'creme_core'

    def __str__(self):
        return self.get_full_name()

    def get_short_name(self):
        return self.username

    def documents(self):
        return self.document_uploaded.all()

    def get_full_name(self):
        if self.is_team:
            return gettext('{user} (team)').format(user=self.username)

        displayed_name = self.displayed_name
        if displayed_name:
            return displayed_name

        # TODO: we could also check related contact to find first_name, last_name
        first_name = self.first_name
        last_name = self.last_name

        if first_name and last_name:
            return gettext('{first_name} {last_name}.').format(
                first_name=first_name,
                last_name=last_name[0],
            )
        else:
            return self.username

    @property
    def created_on_arrow(self):
        return arrow.get(self.date_joined).humanize()

    def save(self, *args, **kwargs):
        """by default the expiration time is set to 2 hours"""
        self.key_expires = timezone.now() + datetime.timedelta(hours=2)
        super().save(*args, **kwargs)

    def clean(self):
        # TODO: split in sub methods?
        # TODO: check is_staff too?
        if self.is_team:
            if self.role_id:
                raise ValidationError('A team cannot have a role.')

            if self.is_superuser:
                raise ValidationError('A team cannot be marked as superuser.')

            if self.last_name:
                raise ValidationError('A team cannot have a last name.')

            if self.first_name:
                raise ValidationError('A team cannot have a first name.')

            if self.displayed_name:
                raise ValidationError('A team cannot have a displayed name.')
        else:
            if self.is_superuser and self.role_id:
                raise ValidationError('A superuser cannot have a role.')

            # ---
            email = self.email
            qs = type(self)._default_manager.filter(is_active=True, email=email)

            if self.id:
                qs = qs.exclude(id=self.id)

            if qs.exists():
                raise ValidationError({
                    'email': ValidationError(
                        self.error_messages['used_email'],
                        code='used_email',
                    ),
                })

    @property
    def settings(self) -> UserSettingValueManager:
        """Get a manager to read or write extra settings stored in the user instance.

        Example:
            # NB: 'sk' in an instance of <creme_core.core.setting_key.UserSettingKey>

            # Read
            value = my_user.settings.get(sk)

            # Write - we use the manager as a context manager
            with my_user.settings as settings:
                settings[sk] = value
        """
        settings = self._settings

        if settings is None:
            settings = self._settings = UserSettingValueManager(
                user_class=self.__class__,
                user_id=self.id,
                json_settings=self.json_settings,
            )

        return settings

    @property
    def theme_info(self) -> tuple[str, str]:
        THEMES = settings.THEMES
        theme_name = self.theme

        for theme_info in settings.THEMES:
            if theme_name == theme_info[0]:
                return theme_info

        return THEMES[0]

    @property  # NB notice that a cache is built
    def teams(self) -> list[User]:
        assert not self.is_team

        teams = self._teams
        if teams is None:
            self._teams = teams = [*self.teams_set.all()]

        return teams

    @property  # NB notice that cache and credentials are well updated when using this property
    def teammates(self) -> dict[int, User]:
        """Dictionary of teammates users
            key: user ID.
            value CremeUser instance.
        """
        assert self.is_team

        teammates = self._teammates

        if teammates is None:
            logger.debug('User.teammates: Cache MISS for user_id=%s', self.id)
            self._teammates = teammates = self.teammates_set.in_bulk()
        else:
            logger.debug('User.teammates: Cache HIT for user_id=%s', self.id)

        return teammates

    @teammates.setter
    def teammates(self, users: Sequence[User]):
        assert self.is_team
        assert not any(user.is_team for user in users)

        self.teammates_set.set(users)
        self._teammates = None  # Clear cache (we could rebuild it but ...)

    def _get_credentials(self, entity: CremeEntity) -> EntityCredentials:
        creds_map = getattr(entity, '_credentials_map', None)

        if creds_map is None:
            entity._credentials_map = creds_map = {}
            creds = None
        else:
            creds = creds_map.get(self.id)

        if creds is None:
            logger.debug(
                'CremeUser._get_credentials(): Cache MISS for id=%s user=%s',
                entity.id, self,
            )
            creds_map[self.id] = creds = EntityCredentials(self, entity)
        else:
            logger.debug(
                'CremeUser._get_credentials(): Cache HIT for id=%s user=%s',
                entity.id, self,
            )

        return creds

    def has_perm(self, perm: str, obj=None) -> bool:
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """
        # Check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list: Iterable[str], obj=None) -> bool:
        has_perm = self.has_perm

        return all(has_perm(perm, obj) for perm in perm_list)

    def has_perm_to_access(self, app_name: str) -> bool:  # TODO: rename "app_label"
        return self.is_superuser or self.role.is_app_allowed_or_administrable(app_name)

    @staticmethod  # TODO: move in utils ?
    def _get_app_verbose_name(app_label: str) -> str:
        try:
            return apps.get_app_config(app_label).verbose_name
        except LookupError:
            return gettext('Invalid app "{}"').format(app_label)

    def has_perm_to_access_or_die(self, app_label: str) -> None:
        if not self.has_perm_to_access(app_label):
            raise PermissionDenied(
                gettext('You are not allowed to access to the app: {}').format(
                    self._get_app_verbose_name(app_label),
                )
            )

    # TODO: rename "app_label"
    def has_perm_to_admin(self, app_name: str) -> bool:
        return self.is_superuser or self.role.is_app_administrable(app_name)

    # TODO: rename 'app_label'
    def has_perm_to_admin_or_die(self, app_name: str) -> None:
        if not self.has_perm_to_admin(app_name):
            raise PermissionDenied(
                gettext('You are not allowed to configure this app: {}').format(
                    self._get_app_verbose_name(app_name),
                )
            )

    def has_perm_to_change(self, entity: CremeEntity) -> bool:
        if entity.is_deleted:
            return False

        main_entity = (
            entity.get_real_entity().get_related_entity()
            if hasattr(entity.entity_type.model_class(), 'get_related_entity')
            else entity
        )

        return self._get_credentials(main_entity).can_change()

    def has_perm_to_change_or_die(self, entity: CremeEntity) -> None:
        if not self.has_perm_to_change(entity):
            raise PermissionDenied(
                gettext('You are not allowed to edit this entity: {}').format(
                    entity.allowed_str(self),
                )
            )

    def has_perm_to_create(self, model_or_entity: EntityInstanceOrClass) -> bool:
        """Helper for has_perm() method.
        Example: user.has_perm('myapp.add_mymodel') => user.has_perm_to_create(MyModel)
        """
        meta = model_or_entity._meta
        return self.has_perm(f'{meta.app_label}.add_{meta.object_name.lower()}')

    def has_perm_to_create_or_die(self, model_or_entity: EntityInstanceOrClass) -> None:
        if not self.has_perm_to_create(model_or_entity):
            raise PermissionDenied(
                gettext('You are not allowed to create: {}').format(
                    model_or_entity._meta.verbose_name,
                )
            )

    def has_perm_to_delete(self, entity: CremeEntity) -> bool:
        if hasattr(entity.entity_type.model_class(), 'get_related_entity'):  # TODO: factorise
            return self._get_credentials(
                entity.get_real_entity().get_related_entity(),
            ).can_change()

        return self._get_credentials(entity).can_delete()

    def has_perm_to_delete_or_die(self, entity: CremeEntity) -> None:
        if not self.has_perm_to_delete(entity):
            raise PermissionDenied(
                gettext('You are not allowed to delete this entity: {}').format(
                    entity.allowed_str(self),
                )
            )

    # TODO: factorise with has_perm_to_create() ??
    def has_perm_to_export(self, model_or_entity: EntityInstanceOrClass) -> bool:
        """Helper for has_perm() method.
        Example: user.has_perm('myapp.export_mymodel') => user.has_perm_to_export(MyModel)
        """
        meta = model_or_entity._meta
        return self.has_perm(f'{meta.app_label}.export_{meta.object_name.lower()}')

    def has_perm_to_export_or_die(self,
                                  model_or_entity: type[CremeEntity] | CremeEntity,
                                  ) -> None:
        if not self.has_perm_to_export(model_or_entity):
            raise PermissionDenied(
                gettext('You are not allowed to export: {}').format(
                    model_or_entity._meta.verbose_name
                )
            )

    def has_perm_to_link(self,
                         entity_or_model: EntityInstanceOrClass,
                         owner: User | None = None,
                         ) -> bool:
        """Can the user link a future entity of a given class ?
        @param entity_or_model: {Instance of} class inheriting CremeEntity.
        @param owner: (only used when 1rst param is a class) Instance of CremeUser ;
                      owner of the (future) entity. 'None' means: is there an
                      owner (at least) that allows linking.
        """
        assert not self.is_team  # Teams can not be logged, it has no sense

        if isinstance(entity_or_model, CremeEntity):
            # TODO: what about related_entity ?
            return (
                False if entity_or_model.is_deleted else
                self._get_credentials(entity_or_model).can_link()
            )

        assert issubclass(entity_or_model, CremeEntity)

        return (
            True if self.is_superuser else
            self.role.can_do_on_model(self, entity_or_model, owner, EntityCredentials.LINK)
        )

    # TODO: factorise ??
    def has_perm_to_link_or_die(self,
                                entity_or_model: EntityInstanceOrClass,
                                owner: User | None = None,
                                ) -> None:
        if not self.has_perm_to_link(entity_or_model, owner):
            if isinstance(entity_or_model, CremeEntity):
                msg = gettext('You are not allowed to link this entity: {}').format(
                    entity_or_model.allowed_str(self)
                )
            else:
                msg = gettext('You are not allowed to link: {}').format(
                    entity_or_model._meta.verbose_name
                )

            raise PermissionDenied(msg)

    def has_perm_to_unlink(self, entity: CremeEntity) -> bool:
        # TODO: what about related_entity ?
        return self._get_credentials(entity).can_unlink()

    def has_perm_to_unlink_or_die(self, entity: CremeEntity) -> None:
        if not self.has_perm_to_unlink(entity):
            raise PermissionDenied(
                gettext('You are not allowed to unlink this entity: {}').format(
                    entity.allowed_str(self),
                )
            )

    def has_perm_to_view(self, entity: CremeEntity) -> bool:
        # TODO: what about related_entity ?
        return self._get_credentials(entity).can_view()

    def has_perm_to_view_or_die(self, entity: CremeEntity) -> None:
        if not self.has_perm_to_view(entity):
            raise PermissionDenied(
                gettext('You are not allowed to view this entity: {}').format(
                    entity.allowed_str(self),
                )
            )



class Tags(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Account(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="account",
        verbose_name=gettext("user"),
        on_delete=models.CASCADE,
    )
    timezone = TimeZoneField(gettext("timezone"))
    language = models.CharField(
        gettext("language"),
        max_length=10,
        choices=settings.ACCOUNTS_LANGUAGES,
        default=DEFAULT_LANGUAGE,
    )

    @classmethod
    def for_request(cls, request):
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            account = user.account
            if account:
                return account
        return AnonymousAccount(request)

    @classmethod
    def create(cls, request=None, **kwargs):
        create_email = kwargs.pop("create_email", True)
        confirm_email = kwargs.pop("confirm_email", None)
        account = cls(**kwargs)
        if "language" not in kwargs:
            if request is None:
                account.languages = DEFAULT_LANGUAGE
            else:
                account.languages = translation.get_language_from_request(request, check_path=True)
        account.save()
        if create_email and account.user.email:
            kwargs = {"primary": True}
            if confirm_email is not None:
                kwargs["confirm"] = confirm_email
            EmailAddress.objects.add_email(account.user, account.user.email, **kwargs)
        return account

    def __str__(self):
        return str(self.user)

    def now(self):
        """
        Returns a timezone aware datetime localized to the account's timezone.
        """
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))
        tz = settings.TIME_ZONE if not self.timezone else self.timezone
        return now.astimezone(pytz.timezone(tz))

    def localtime(self, value):
        """
        Given a datetime object as value convert it to the timezone of
        the account.
        """
        tz = settings.TIME_ZONE if not self.timezone else self.timezone
        if value.tzinfo is None:
            value = pytz.timezone(settings.TIME_ZONE).localize(value)
        return value.astimezone(pytz.timezone(tz))


class AnonymousAccount:

    def __init__(self, request=None):
        self.user = AnonymousUser()
        self.timezone = settings.TIME_ZONE
        if request is None:
            self.language = DEFAULT_LANGUAGE
        else:
            self.language = translation.get_language_from_request(request, check_path=True)

    def __str__(self):
        return "AnonymousAccount"


class EmailAddress(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, unique=settings.ACCOUNT_EMAIL_UNIQUE)
    verified = models.BooleanField(gettext("verified"), default=False)
    primary = models.BooleanField(gettext("primary"), default=False)

    objects = EmailAddressManager()

    class Meta:
        verbose_name = gettext("email address")
        verbose_name_plural = gettext("email addresses")
        if not settings.ACCOUNT_EMAIL_UNIQUE:
            unique_together = [("user", "email")]

    def __str__(self):
        return "{0} ({1})".format(self.email, self.user)

    def set_as_primary(self, conditional=False):
        old_primary = EmailAddress.objects.get_primary(self.user)
        if old_primary:
            if conditional:
                return False
            old_primary.primary = False
            old_primary.save()
        self.primary = True
        self.save()
        self.user.email = self.email
        self.user.save()
        return True

    def send_confirmation(self, **kwargs):
        confirmation = EmailConfirmation.create(self)
        confirmation.send(**kwargs)
        return confirmation

    def change(self, new_email, confirm=True):
        """
        Given a new email address, change self and re-confirm.
        """
        with transaction.atomic():
            self.user.email = new_email
            self.user.save()
            self.email = new_email
            self.verified = False
            self.save()
            if confirm:
                self.send_confirmation()

    def validate_unique(self, exclude=None):
        super(EmailAddress, self).validate_unique(exclude=exclude)

        qs = EmailAddress.objects.filter(email__iexact=self.email)

        if qs.exists() and settings.ACCOUNT_EMAIL_UNIQUE:
            raise forms.ValidationError({
                "email": gettext("A user is registered with this email address."),
            })


class EmailConfirmation(models.Model):

    email_address = models.ForeignKey(EmailAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    sent = models.DateTimeField(null=True)
    key = models.CharField(max_length=64, unique=True)

    objects = EmailConfirmationManager()

    class Meta:
        verbose_name = gettext("email confirmation")
        verbose_name_plural = gettext("email confirmations")

    def __str__(self):
        return "confirmation for {0}".format(self.email_address)

    @classmethod
    def create(cls, email_address):
        key = hookset.generate_email_confirmation_token(email_address.email)
        return cls._default_manager.create(email_address=email_address, key=key)

    def key_expired(self):
        expiration_date = self.sent + datetime.timedelta(days=settings.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS)
        return expiration_date <= timezone.now()
    key_expired.boolean = True

    def confirm(self):
        if not self.key_expired() and not self.email_address.verified:
            email_address = self.email_address
            email_address.verified = True
            email_address.set_as_primary(conditional=True)
            email_address.save()
            signals.email_confirmed.send(sender=self.__class__, email_address=email_address)
            return email_address

    def send(self, **kwargs):
        current_site = kwargs["site"] if "site" in kwargs else Site.objects.get_current()
        protocol = settings.DEFAULT_HTTP_PROTOCOL
        activate_url = "{0}://{1}{2}".format(
            protocol,
            current_site.domain,
            reverse(settings.ACCOUNT_EMAIL_CONFIRMATION_URL, args=[self.key])
        )
        ctx = {
            "email_address": self.email_address,
            "user": self.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": self.key,
        }
        hookset.send_confirmation_email([self.email_address.email], ctx)
        self.sent = timezone.now()
        self.save()
        signals.email_confirmation_sent.send(sender=self.__class__, confirmation=self)


class SignupCode(models.Model):

    class AlreadyExists(Exception):
        pass

    class InvalidCode(Exception):
        pass

    code = models.CharField(gettext("code"), max_length=64, unique=True)
    max_uses = models.PositiveIntegerField(gettext("max uses"), default=1)
    expiry = models.DateTimeField(gettext("expiry"), null=True, blank=True)
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, blank=True)
    notes = models.TextField(gettext("notes"), blank=True)
    sent = models.DateTimeField(gettext("sent"), null=True, blank=True)
    created = models.DateTimeField(gettext("created"), default=timezone.now, editable=False)
    use_count = models.PositiveIntegerField(gettext("use count"), editable=False, default=0)

    class Meta:
        verbose_name = gettext("signup code")
        verbose_name_plural = gettext("signup codes")

    def __str__(self):
        if self.email:
            return "{0} [{1}]".format(self.email, self.code)
        else:
            return self.code

    @classmethod
    def exists(cls, code=None, email=None):
        checks = []
        if code:
            checks.append(Q(code=code))
        if email:
            checks.append(Q(email=email))
        if not checks:
            return False
        return cls._default_manager.filter(functools.reduce(operator.or_, checks)).exists()

    @classmethod
    def create(cls, **kwargs):
        email, code = kwargs.get("email"), kwargs.get("code")
        if kwargs.get("check_exists", True) and cls.exists(code=code, email=email):
            raise cls.AlreadyExists()
        expiry = timezone.now() + datetime.timedelta(hours=kwargs.get("expiry", 24))
        if not code:
            code = hookset.generate_signup_code_token(email)
        params = {
            "code": code,
            "max_uses": kwargs.get("max_uses", 0),
            "expiry": expiry,
            "inviter": kwargs.get("inviter"),
            "notes": kwargs.get("notes", "")
        }
        if email:
            params["email"] = email
        return cls(**params)

    @classmethod
    def check_code(cls, code):
        try:
            signup_code = cls._default_manager.get(code=code)
        except cls.DoesNotExist:
            raise cls.InvalidCode()
        else:
            if signup_code.max_uses and signup_code.max_uses <= signup_code.use_count:
                raise cls.InvalidCode()
            else:
                if signup_code.expiry and timezone.now() > signup_code.expiry:
                    raise cls.InvalidCode()
                else:
                    return signup_code

    def calculate_use_count(self):
        self.use_count = self.signupcoderesult_set.count()
        self.save()

    def use(self, user):
        """
        Add a SignupCode result attached to the given user.
        """
        result = SignupCodeResult()
        result.signup_code = self
        result.user = user
        result.save()
        signup_code_used.send(sender=result.__class__, signup_code_result=result)

    def send(self, **kwargs):
        protocol = settings.DEFAULT_HTTP_PROTOCOL
        current_site = kwargs["site"] if "site" in kwargs else Site.objects.get_current()
        if "signup_url" not in kwargs:
            signup_url = "{0}://{1}{2}?{3}".format(
                protocol,
                current_site.domain,
                reverse("account_signup"),
                urlencode({"code": self.code})
            )
        else:
            signup_url = kwargs["signup_url"]
        ctx = {
            "signup_code": self,
            "current_site": current_site,
            "signup_url": signup_url,
        }
        ctx.update(kwargs.get("extra_ctx", {}))
        hookset.send_invitation_email([self.email], ctx)
        self.sent = timezone.now()
        self.save()
        signup_code_sent.send(sender=SignupCode, signup_code=self)


class SignupCodeResult(models.Model):

    signup_code = models.ForeignKey(SignupCode, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, **kwargs):
        super(SignupCodeResult, self).save(**kwargs)
        self.signup_code.calculate_use_count()


class AccountDeletion(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField(max_length=254)
    date_requested = models.DateTimeField(gettext("date requested"), default=timezone.now)
    date_expunged = models.DateTimeField(gettext("date expunged"), null=True, blank=True)

    class Meta:
        verbose_name = gettext("account deletion")
        verbose_name_plural = gettext("account deletions")

    @classmethod
    def expunge(cls, hours_ago=None):
        if hours_ago is None:
            hours_ago = settings.ACCOUNT_DELETION_EXPUNGE_HOURS
        before = timezone.now() - datetime.timedelta(hours=hours_ago)
        count = 0
        for account_deletion in cls.objects.filter(date_requested__lt=before, user__isnull=False):
            hookset.account_delete_expunge(account_deletion)
            account_deletion.date_expunged = timezone.now()
            account_deletion.save()
            count += 1
        return count

    @classmethod
    def mark(cls, user):
        account_deletion, created = cls.objects.get_or_create(user=user)
        account_deletion.email = user.email
        account_deletion.save()
        hookset.account_delete_mark(account_deletion)
        return account_deletion


class PasswordHistory(models.Model):
    """
    Contains single password history for user.
    """
    class Meta:
        verbose_name = gettext("password history")
        verbose_name_plural = gettext("password histories")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="password_history", on_delete=models.CASCADE)
    password = models.CharField(max_length=255)  # encrypted password
    timestamp = models.DateTimeField(default=timezone.now)  # password creation time


class PasswordExpiry(models.Model):
    """
    Holds the password expiration period for a single user.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="password_expiry",
        verbose_name=gettext("user"),
        on_delete=models.CASCADE,
    )
    expiry = models.PositiveIntegerField(default=0)

#BEGIN FOR CREME MODEL
class SetCredentials(models.Model):
    # 'ESET' means 'Entities SET'
    ESET_ALL    = 1  # => all entities
    ESET_OWN    = 2  # => his own entities
    ESET_FILTER = 3  # => use an EntityFilter

    ESETS_MAP = OrderedDict([
        (ESET_ALL,    gettext('All entities')),
        (ESET_OWN,    gettext("User's own entities")),
        (ESET_FILTER, gettext('Filtered entities')),
    ])  # TODO: inline ?

    role = models.ForeignKey(
        UserRole,
        related_name='credentials', verbose_name=gettext('Role'), null=True, on_delete=models.CASCADE, editable=False,
    ).set_tags(viewable=False)

    # See EntityCredentials.VIEW|CHANGE|DELETE|LINK|UNLINK
    value = models.PositiveSmallIntegerField()
    set_type = models.PositiveIntegerField(
        verbose_name=gettext('Type of entities set'),
        choices=ESETS_MAP.items(),
        default=ESET_ALL,
        help_text=gettext(
            'The choice «Filtered entities» allows to configure credentials '
            'based on values of fields or relationships for example.'
        ),
    )
    ctype = EntityCTypeForeignKey(
        verbose_name=gettext('Apply to a specific type'),
        # NB: NULL means "No specific type" (i.e. any kind of CremeEntity)
        null=True, blank=True,
    )
    # entity  = models.ForeignKey(CremeEntity, null=True) ??
    forbidden = models.BooleanField(
        verbose_name=gettext('Allow or forbid?'),
        default=False,
        choices=[
            (False, gettext('The users are allowed to perform the selected actions')),
            (True,  gettext('The users are NOT allowed to perform the selected actions')),
        ],
        help_text=gettext(
            'Notice that actions which are forbidden & allowed at '
            'the same time are considered as forbidden when final '
            'permissions are computed.'
        ),
    )
    efilter = models.ForeignKey(
        'EntityFilter', editable=False, null=True, on_delete=models.PROTECT,
    )

    class Meta:
        app_label = 'creme_core'

    def __str__(self):
        value = self.value
        forbidden = self.forbidden
        perms = []
        append = perms.append

        if value is not None:
            if value & EntityCredentials.VIEW:
                append(gettext('view'))

            if value & EntityCredentials.CHANGE:
                append(gettext('change'))

            if value & EntityCredentials.DELETE:
                append(gettext('delete'))

            if value & EntityCredentials.LINK:
                append(gettext('link'))

            if value & EntityCredentials.UNLINK:
                append(gettext('unlink'))

        if not perms:
            append(
                gettext('nothing forbidden') if forbidden else
                gettext('nothing allowed')
            )

        args = {
            'set':   self.get_set_type_display(),
            'perms': ', '.join(perms),
        }

        if self.ctype:
            args['type'] = self.ctype
            format_str = (
                gettext('For “{set}“ of type “{type}” it is forbidden to: {perms}')
                if forbidden else
                gettext('For “{set}“ of type “{type}” it is allowed to: {perms}')
            )
        else:
            format_str = (
                gettext('For “{set}“ it is forbidden to: {perms}')
                if forbidden else
                gettext('For “{set}“ it is allowed to: {perms}')
            )

        return format_str.format(**args)

    def _get_perms(self, user, entity: CremeEntity) -> int:
        """@return An integer with binary flags for permissions."""
        ctype_id = self.ctype_id

        if not ctype_id or ctype_id == entity.entity_type_id:
            set_type = self.set_type

            if set_type == SetCredentials.ESET_ALL:
                return self.value
            elif set_type == SetCredentials.ESET_OWN:
                user_id = entity.user_id
                if user.id == user_id or any(user_id == t.id for t in user.teams):
                    return self.value
            else:  # SetCredentials.ESET_FILTER
                if self.efilter.accept(entity=entity.get_real_entity(), user=user):
                    return self.value

        return EntityCredentials.NONE

    @staticmethod
    def get_perms(sc_sequence: Sequence[SetCredentials],
                  user,
                  entity: CremeEntity,
                  ) -> int:
        """@param sc_sequence: Sequence of SetCredentials instances."""
        perms = reduce(
            or_op,
            (sc._get_perms(user, entity) for sc in sc_sequence if not sc.forbidden),
            EntityCredentials.NONE
        )

        for sc in sc_sequence:
            if sc.forbidden:
                perms &= ~sc._get_perms(user, entity)

        return perms

    @classmethod
    def _can_do(cls,
                sc_sequence: Sequence[SetCredentials],
                user,
                model: type[CremeEntity],
                owner=None,
                perm: int = EntityCredentials.VIEW,
                ) -> bool:
        if owner is None:
            def user_is_concerned(sc):
                return not sc.forbidden
        else:
            def user_is_concerned(sc):
                return user.id in owner.teammates if owner.is_team else user == owner

        ESET_ALL = cls.ESET_ALL
        ESET_OWN = cls.ESET_OWN
        allowed_ctype_ids = (None, ContentType.objects.get_for_model(model).id)  # TODO: factorise
        allowed_found = False

        for sc in sc_sequence:
            if sc.ctype_id in allowed_ctype_ids and sc.value & perm:
                set_type = sc.set_type

                # NB: it's hard to manage ESET_FILTER in a satisfactory way,
                #     so we ignore this type of credentials when checking models
                #     (so LINK credentials + filter == no relationships adding at entity creation).
                if set_type == ESET_ALL or (set_type == ESET_OWN and user_is_concerned(sc)):
                    if sc.forbidden:
                        return False
                    else:
                        allowed_found = True

        return allowed_found

    @classmethod
    def _aux_filter(cls,
                    model: type[CremeEntity],
                    sc_sequence: Sequence[SetCredentials],
                    user,
                    queryset: QuerySet,
                    perm: int,
                    ) -> QuerySet:
        allowed_ctype_ids = {None, ContentType.objects.get_for_model(model).id}
        ESET_ALL = cls.ESET_ALL
        ESET_OWN = cls.ESET_OWN

        filtered_qs = queryset

        # TODO: _PERMS_MAP public ?
        for single_perm in EntityCredentials._PERMS_MAP.values():
            if not single_perm & perm:
                continue

            allowed, forbidden = partition(
                lambda sc: sc.forbidden,
                sorted(
                    (
                        sc
                        for sc in sc_sequence
                        if sc.ctype_id in allowed_ctype_ids and sc.value & single_perm
                    ),
                    # NB: we sort to get ESET_ALL creds before ESET_OWN ones,
                    #     then ESET_FILTER ones.
                    key=lambda sc: sc.set_type,
                )
            )

            if not allowed:
                return queryset.none()

            if any(f.set_type == ESET_ALL for f in forbidden):
                return queryset.none()

            def user_filtering_kwargs():  # TODO: cache/lazy
                teams = user.teams
                return {'user__in': [user, *teams]} if teams else {'user': user}

            q = Q()
            for cred in allowed:
                set_type = cred.set_type

                if set_type == ESET_ALL:
                    break

                if set_type == ESET_OWN:
                    q |= Q(**user_filtering_kwargs())
                else:  # SetCredentials.ESET_FILTER
                    # TODO: distinct ? (see EntityFilter.filter())
                    q |= cred.efilter.get_q(user=user)
            else:
                filtered_qs = filtered_qs.filter(q)

            for cred in forbidden:
                if cred.set_type == ESET_OWN:
                    filtered_qs = filtered_qs.exclude(**user_filtering_kwargs())
                else:  # SetCredentials.ESET_FILTER
                    filtered_qs = filtered_qs.exclude(cred.efilter.get_q(user=user))

        return filtered_qs

    @classmethod
    def filter(cls,
               sc_sequence: Sequence[SetCredentials],
               user,
               queryset: QuerySet,
               perm: int,
               ) -> QuerySet:
        """Filter a queryset of entities with the given credentials.
        Beware, the model class must be a child class of CremeEntity,
        but cannot be CremeEntity itself.

        @param sc_sequence: A sequence of SetCredentials instances.
        @param user: A <django.contrib.auth.get_user_model()> instance (e.g. CremeUser).
        @param queryset: A Queryset on a child class of CremeEntity.
        @param perm: A combination of values in EntityCredentials.{VIEW, CHANGE, ...}.
               Eg: 'EntityCredentials.DELETE'
                   'EntityCredentials.VIEW | EntityCredentials.CHANGE'
        @return: A new queryset on the same model.
        """
        model = queryset.model
        assert issubclass(model, CremeEntity)
        assert model is not CremeEntity

        return cls._aux_filter(
            model=model, sc_sequence=sc_sequence, user=user,
            queryset=queryset, perm=perm,
        )

    @classmethod
    def filter_entities(cls,
                        sc_sequence: Sequence[SetCredentials],
                        user,
                        queryset: QuerySet,
                        perm: int,
                        models: Iterable[type[CremeEntity]],
                        as_model=None,
                        ) -> QuerySet:
        """Filter a queryset of entities with the given credentials.
        Beware, model class must be CremeEntity ; it cannot be a child class
        of CremeEntity.

        @param sc_sequence: A sequence of SetCredentials instances.
        @param user: A django.contrib.auth.get_user_model() instance (e.g. CremeUser).
        @param queryset: Queryset with model=CremeEntity.
        @param perm: A value in EntityCredentials.{VIEW, CHANGE, ...}.
               If the argument "as_model" is not None, you can use a combination
               of values like 'EntityCredentials.VIEW | EntityCredentials.CHANGE'.
        @param models: An iterable of CremeEntity-child-classes, corresponding
               to allowed models.
        @param as_model: A model inheriting CremeEntity, or None. If a model is
               given, all the entities in the queryset are filtered with the
               credentials for this model.
               BEWARE: you should probably use this feature only if the queryset
               is already filtered by its field 'entity_type' (to keep only
               entities of the right model, & so do not make mistakes with credentials).
        @return: A new queryset on CremeEntity.
        @raise: EntityCredentials.FilteringError if an EntityFilter which cannot
                be used on CremeEntity is found in <sc_sequence>.
        """
        assert queryset.model is CremeEntity

        get_for_model = ContentType.objects.get_for_model

        def _check_efilters(sc_seq):
            if any(sc.efilter_id and not sc.efilter.applicable_on_entity_base for sc in sc_seq):
                raise EntityCredentials.FilteringError(
                    "An EntityFilter (not targeting CremeEntity) is used by a "
                    "{cls} instance so it's not possible to use "
                    "{cls}.filter_entities().".format(cls=cls.__name__)
                )

        if as_model is not None:
            assert issubclass(as_model, CremeEntity)

            narrowed_ct_ids = {None, get_for_model(as_model).id}
            narrowed_sc = [sc for sc in sc_sequence if sc.ctype_id in narrowed_ct_ids]
            _check_efilters(narrowed_sc)

            return cls._aux_filter(
                model=as_model, sc_sequence=narrowed_sc, user=user,
                queryset=queryset, perm=perm,
            )

        # TODO: use int.bit_count() with Python 3.10
        if bin(perm).count('1') > 1:
            raise ValueError(
                'filter_entities() does not (yet) manage permissions '
                'combination when the argument "as_model" is None.',
            )

        all_ct_ids = {
            None,
            *(get_for_model(model).id for model in models),
        }
        sorted_sc = sorted(
            (sc for sc in sc_sequence if sc.ctype_id in all_ct_ids),
            # NB: we sort to get ESET_ALL creds before ESET_OWN/ESET_FILTER ones.
            key=lambda sc: sc.set_type,
        )
        _check_efilters(sorted_sc)

        # NB: some explanations on the algorithm :
        #  we try to regroup ContentTypes (corresponding to CremeEntity sub_classes)
        #  which have the same filtering rules ; so we can generate a Query which looks like
        #    entity_type__in=[...] OR (entity_type__in=[...] AND user__exact=current-user) OR
        #    (entity_type__in=[...] AND field1__startswith='foo')

        OWN_FILTER_ID = 0  # Fake EntityFilter ID corresponding to ESET_OWN.

        ESET_ALL = cls.ESET_ALL
        ESET_OWN = cls.ESET_OWN
        ESET_FILTER = cls.ESET_FILTER

        def _extract_filter_ids(set_creds):
            for sc in set_creds:
                if sc.set_type == ESET_OWN:
                    yield OWN_FILTER_ID
                    break  # Avoid several OWN_FILTER_ID (should not happen)

            for sc in set_creds:
                if sc.set_type == ESET_FILTER:
                    yield sc.efilter_id

        # Map of EntityFilters to apply on ContentTypes groups
        #   key = tuple containing 2 tuples of filter IDs: forbidden rules & allowed ones.
        #   value = list of ContentType IDs.
        #  Note: special values for EntityFilter ID:
        #    None: means ESET_ALL (no filtering)
        #    OWN_FILTER_ID: means ESET_OWN (a virtual EntityFilter on "user" field).
        ctypes_filtering: DefaultDict[tuple, list[int]] = defaultdict(list)

        efilters_per_id = {sc.efilter_id: sc.efilter for sc in sc_sequence}

        for model in models:
            ct_id = get_for_model(model).id
            model_ct_ids = {None, ct_id}   # <None> means <CremeEntity>

            # forbidden, allowed = split_filter(
            allowed, forbidden = partition(
                lambda sc: sc.forbidden,
                (
                    sc for sc in sorted_sc
                    if sc.ctype_id in model_ct_ids and sc.value & perm
                )
            )

            if allowed:
                if forbidden and forbidden[0].set_type == ESET_ALL:
                    continue

                allowed_filter_ids = (
                    [None]
                    if allowed[0].set_type == ESET_ALL else
                    [*_extract_filter_ids(allowed)]
                )
                forbidden_filter_ids = [*_extract_filter_ids(forbidden)]

                ctypes_filtering[(
                    tuple(forbidden_filter_ids),
                    tuple(allowed_filter_ids),
                )].append(ct_id)

        if not ctypes_filtering:
            queryset = queryset.none()
        else:
            def _user_filtering_q():  # TODO: cached/lazy ?
                teams = user.teams
                return Q(**{'user__in': [user, *teams]} if teams else {'user': user})

            def _efilter_ids_to_Q(efilter_ids):
                filters_q = Q()

                for filter_id in efilter_ids:
                    # TODO: condexpr
                    if filter_id is not None:  # None == ESET_ALL
                        if filter_id == OWN_FILTER_ID:
                            filter_q = _user_filtering_q()
                        else:
                            # TODO: distinct ??
                            filter_q = efilters_per_id[filter_id].get_q(user=user)

                        filters_q |= filter_q

                return filters_q

            q = Q()
            for (forbidden_filter_ids, allowed_filter_ids), ct_ids in ctypes_filtering.items():
                q |= (
                    (
                        Q(entity_type_id=ct_ids[0])
                        if len(ct_ids) == 1 else
                        Q(entity_type_id__in=ct_ids)
                    )
                    & _efilter_ids_to_Q(allowed_filter_ids)
                    & ~_efilter_ids_to_Q(forbidden_filter_ids)
                )

            queryset = queryset.filter(q)

        return queryset

    def save(self, *args, **kwargs):
        ct = self.ctype
        if ct is None:
            model = CremeEntity
        else:
            model = ct.model_class()
            if model is CremeEntity:
                raise ValueError(
                    f'{type(self).__name__}: '
                    f'<ctype> cannot be <CremeEntity> (use <None> instead).'
                )

        if self.set_type == self.ESET_FILTER:
            if not self.efilter_id:
                raise ValueError(
                    f'{type(self).__name__} with <set_type == ESET_FILTER> must have a filter.'
                )

            filter_model = self.efilter.entity_type.model_class()

            if filter_model != model:
                raise ValueError(
                    f'{type(self).__name__} must have a filter related to the '
                    f'same type: {model} != {filter_model}'
                )
        elif self.efilter_id:
            raise ValueError(
                f'Only {type(self).__name__} with <set_type == ESET_FILTER> '
                f'can have a filter.'
            )

        super().save(*args, **kwargs)

    def set_value(self, *,
                  can_view: bool,
                  can_change: bool,
                  can_delete: bool,
                  can_link: bool,
                  can_unlink: bool,
                  ) -> None:
        """Set the 'value' attribute from 5 booleans."""
        value = EntityCredentials.NONE

        if can_view:
            value |= EntityCredentials.VIEW

        if can_change:
            value |= EntityCredentials.CHANGE

        if can_delete:
            value |= EntityCredentials.DELETE

        if can_link:
            value |= EntityCredentials.LINK

        if can_unlink:
            value |= EntityCredentials.UNLINK

        self.value = value


get_user_field = User._meta.get_field
for fname in ('password', 'last_login'):
    get_user_field(fname).set_tags(viewable=False)

del get_user_field


class Sandbox(models.Model):
    """When a CremeEntity is associated to a sandbox, only the user related to this sandbox
    can have its regular permission on this entity.
    A Sandbox can be related to a UserRole ; in these case all users with this
    role can access to this entity.

    Notice that superusers ignore the Sandboxes ; so if a SandBox has no related
    user/role, the entities in this sandbox are only accessible to the superusers
    (like the Sandbox built in creme_core.populate.py)
    """
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    type_id = models.CharField('Type of sandbox', max_length=48, editable=False)
    role = models.ForeignKey(
        UserRole, verbose_name='Related role', null=True,
        default=None, on_delete=models.CASCADE, editable=False,
    )
    # superuser = BooleanField('related to superusers', default=False, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Related user',
        null=True, default=None, on_delete=models.CASCADE, editable=False,
    )

    class Meta:
        app_label = 'creme_core'

    @property
    def type(self) -> SandboxType | None:
        # TODO: pass registry as argument
        from ..core.sandbox import sandbox_type_registry

        return sandbox_type_registry.get(self)

