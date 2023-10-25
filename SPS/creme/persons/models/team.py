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
import logging
import arrow
import uuid
import os

from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import Permission

from reversion import revisions as reversion

from ...creme_core.models import CREME_REPLACE_NULL, CremeEntity, Language
from ...invitations.models import JoinInvitation
from .. hooks import hookset
from .. import signals
from .. import constants, get_team_model, get_organisation_model
from . import profile, address, organisation

logger = logging.getLogger(__name__)

def avatar_upload(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), "avatars", filename)

def create_slug(name):
    return slugify(name)[:50]
    #return slugify(name)[:50]


MEMBER_ACCESS_OPEN = "open"
MEMBER_ACCESS_APPLICATION = "application"
MEMBER_ACCESS_INVITATION = "invitation"

MANAGER_ACCESS_ADD = "add someone"
MANAGER_ACCESS_INVITE = "invite someone"

MEMBER_ACCESS_CHOICES = [
    (MEMBER_ACCESS_OPEN, _("open")),
    (MEMBER_ACCESS_APPLICATION, _("by application")),
    (MEMBER_ACCESS_INVITATION, _("by invitation"))
]

MANAGER_ACCESS_CHOICES = [
    (MANAGER_ACCESS_ADD, _("add someone")),
    (MANAGER_ACCESS_INVITE, _("invite someone"))
]

TEAM_ACCESS_CHOICES = [
    ("open", _("open")),
    ("application", _("by application")),
    ("invitation", _("by invitation"))
]

MEMBERSHIP_STATE_CHOICES = [
    ("applied", _("applied")),
    ("invited", _("invited")),
    ("declined", _("declined")),
    ("rejected", _("rejected")),
    ("member", _("member")),
    ("manager", _("manager")),
]


class AbstractTeams(CremeEntity):
    name = models.CharField(max_length=100).set_tags(optional=True)
    users = models.ManyToManyField(settings.PERSONS_PROFILE_MODEL, related_name="user_teams").set_tags(optional=True)
    created_on = models.DateTimeField(_("Created on"), auto_now=True).set_tags(optional=True)
    created_by = models.ForeignKey(
        settings.PERSONS_PROFILE_MODEL,
        related_name="teams_created",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    ).set_tags(optional=True)
    org = models.ForeignKey(organisation.Organisation, on_delete=models.SET_NULL, null=True, blank=True).set_tags(optional=True)

    creation_label = _('Create a team')
    save_label     = _('Save the team')

    class Meta:
        abstract = True
        app_label = 'persons'
        ordering = ('name', 'user', "-created_on")
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')
        indexes = [
            models.Index(
                fields=['name', 'org'],
                name='persons__team__default_lv',
            ),
        ]

    def __str__(self):
        org = self.org

        if org and org.shortcut:
            return _('{org} {name} {user}').format(
                org=org.shortcut,
                name=self.name,
                user=self.user,
            )

        if self.name:
            return _('{name} {user}').format(
                name=self.name,
                user=self.user,
            )

        return self.name or ''


    def get_absolute_url(self):
        return reverse('persons__view_team', args=(self.id,))

    @staticmethod
    def get_create_absolute_url():
        return reverse('persons__create_team')

    def get_edit_absolute_url(self):
        return reverse('persons__edit_team', args=(self.id,))

    @staticmethod
    def get_lv_absolute_url():
        return reverse('persons__list_teams')

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


    @classmethod
    def _create_linked_team(cls, user, **kwargs) -> AbstractTeams:
        # TODO: assert user is not a team + enforce non team clean() ?
        owner = user

        if user.is_staff:
            superuser = type(user)._default_manager.filter(
                is_superuser=True, is_staff=False,
            ).order_by('id').first()

            if superuser is None:
                logger.critical(
                    'No existing super-user found to assign the staff Team '
                    '(creme_populate has not been run?!) ; you should create a '
                    'super-user & change the owner of this staff Team in '
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
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    def get_users(self):
        return ",".join(
            [str(_id) for _id in list(self.users.values_list("id", flat=True))]
        )
        # return ','.join(list(self.users.values_list('id', flat=True)))


class Teams(AbstractTeams):
    class Meta(AbstractTeams.Meta):
        swappable = 'PERSONS_TEAM_MODEL'


class AbstractBaseTeam(CremeEntity):
    member_access = models.CharField(max_length=20, choices=MEMBER_ACCESS_CHOICES, verbose_name=_("member access")).set_tags(optional=True)
    manager_access = models.CharField(max_length=20, choices=MANAGER_ACCESS_CHOICES, verbose_name=_("manager access")).set_tags(optional=True)
    team_access = models.CharField(max_length=20, choices=TEAM_ACCESS_CHOICES, verbose_name=_("Team Access")).set_tags(optional=True)

    creation_label = _('Create a base team')
    save_label     = _('Save the base team')

    class Meta:
        abstract = True
        app_label = 'persons'
        ordering = ('member_access', 'manager_access', "team_access")
        verbose_name = _('Base Team')
        verbose_name_plural = _('Base Teams')
        indexes = [
            models.Index(
                fields=['member_access', 'manager_access', "team_access"],
                name='persons__baseteam__default_lv',
            ),
        ]

    def members_count(obj):
        return obj.memberships.count()

    members_count.short_description = _("Members Count")

    def get_absolute_url(self):
        return reverse('persons__view_baseteam', args=(self.id,))

    @staticmethod
    def get_create_absolute_url():
        return reverse('persons__create_baseteam')

    def get_edit_absolute_url(self):
        return reverse('persons__edit_baseteam', args=(self.id,))

    @staticmethod
    def get_lv_absolute_url():
        return reverse('persons__list_baseteams')

    def _post_save_clone(self, source):
        self._aux_post_save_clone(source)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    @classmethod
    def _create_linked_team(cls, user, **kwargs) -> AbstractBaseTeam:
        # TODO: assert user is not a team + enforce non team clean() ?
        owner = user

        if user.is_staff:
            superuser = type(user)._default_manager.filter(
                is_superuser=True, is_staff=False,
            ).order_by('id').first()

            if superuser is None:
                logger.critical(
                    'No existing super-user found to assign the staff Team '
                    '(creme_populate has not been run?!) ; you should create a '
                    'super-user & change the owner of this staff Team in '
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
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    def get_users(self):
        return ",".join(
            [str(_id) for _id in list(self.users.values_list("id", flat=True))]
        )
        # return ','.join(list(self.users.values_list('id', flat=True)))

    def can_join(self, user):
        state = self.state_for(user)
        if self.member_access == AbstractBaseTeam.MEMBER_ACCESS_OPEN and state is None:
            return True
        elif state == AbstractBaseMembership.STATE_INVITED:
            return True
        else:
            return False

    def can_leave(self, user):
        # managers can't leave at the moment
        role = self.role_for(user)
        return role == AbstractBaseMembership.ROLE_MEMBER

    def can_apply(self, user):
        state = self.state_for(user)
        return self.member_access == AbstractBaseTeam.MEMBER_ACCESS_APPLICATION and state is None

    @property
    def applicants(self):
        return self.memberships.filter(state=AbstractBaseMembership.STATE_APPLIED)

    @property
    def invitees(self):
        return self.memberships.filter(state=AbstractBaseMembership.STATE_INVITED)

    @property
    def declines(self):
        return self.memberships.filter(state=AbstractBaseMembership.STATE_DECLINED)

    @property
    def rejections(self):
        return self.memberships.filter(state=AbstractBaseMembership.STATE_REJECTED)

    @property
    def waitlisted(self):
        return self.memberships.filter(state=AbstractBaseMembership.STATE_WAITLISTED)

    @property
    def acceptances(self):
        return self.memberships.filter(state__in=[
            AbstractBaseMembership.STATE_ACCEPTED,
            AbstractBaseMembership.STATE_AUTO_JOINED]
        )

    @property
    def members(self):
        return self.acceptances.filter(role=AbstractBaseMembership.ROLE_MEMBER)

    @property
    def managers(self):
        return self.acceptances.filter(role=AbstractBaseMembership.ROLE_MANAGER)

    @property
    def teams(self):
        return self.acceptances.filter(role=AbstractBaseMembership.RO)

    @property
    def owners(self):
        return self.acceptances.filter(role=AbstractBaseMembership.ROLE_OWNER)

    def is_owner_or_manager(self, user):
        return self.acceptances.filter(
            role__in=[
                AbstractBaseMembership.ROLE_OWNER,
                AbstractBaseMembership.ROLE_MANAGER
            ],
            user=user
        ).exists()

    def is_member(self, user):
        return self.members.filter(user=user).exists()

    def is_manager(self, user):
        return self.managers.filter(user=user).exists()

    def is_owner(self, user):
        return self.owners.filter(user=user).exists()

    def is_on_team(self, user):
        return self.acceptances.filter(user=user).exists()

    def add_member(self, user, role=None, state=None, by=None):
        # we do this, rather than put the BaseMembership constants in declaration
        # because BaseMembership is not yet defined
        if role is None:
            role = AbstractBaseMembership.ROLE_MEMBER
        if state is None:
            state = AbstractBaseMembership.STATE_AUTO_JOINED

        membership, created = self.memberships.get_or_create(
            team=self,
            user=user,
            defaults={"role": role, "state": state},
        )
        signals.added_member.send(sender=self, membership=membership, by=by)
        return membership

    def add_user(self, user, role, by=None):
        state = AbstractBaseMembership.STATE_AUTO_JOINED
        if self.manager_access == MANAGER_ACCESS_INVITE:
            state = AbstractBaseMembership.STATE_INVITED
        membership, _ = self.memberships.get_or_create(
            user=user,
            defaults={"role": role, "state": state}
        )
        signals.added_member.send(sender=self, membership=membership, by=by)
        return membership

    def invite_user(self, from_user, to_email, role, message=None):
        if not JoinInvitation.objects.filter(signup_code__email=to_email).exists():
            invite = JoinInvitation.invite(from_user, to_email, message, send=False)
            membership, _ = self.memberships.get_or_create(
                invite=invite,
                defaults={"role": role, "state": AbstractBaseMembership.STATE_INVITED}
            )
            invite.send_invite()
            signals.invited_user.send(sender=self, membership=membership, by=from_user)
            return membership

    def for_user(self, user):
        try:
            return self.memberships.get(user=user)
        except ObjectDoesNotExist:
            pass

    def state_for(self, user):
        membership = self.for_user(user=user)
        if membership:
            return membership.state

    # def role_for(self, user):
    #     if hookset.user_is_staff(user):
    #         return Membership.ROLE_MANAGER
    #
    #     membership = self.for_user(user)
    #     if membership:
    #         return membership.role


class SimpleTeam(AbstractBaseTeam):
    class Meta(AbstractBaseTeam.Meta):
        swappable = 'PERSONS_BASETEAM_MODEL'


@deconstructible
class Team(AbstractBaseTeam):

    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    avatar = models.ImageField(upload_to=avatar_upload, blank=True, verbose_name=_("avatar"))
    #description = models.TextField(blank=True, verbose_name=_("Description"))
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="teams_created", verbose_name=_("creator"), on_delete=models.CASCADE)
    #created = models.DateTimeField(default=timezone.now, editable=False, verbose_name=_("Created"))

    # member permissions
    permissions = models.ManyToManyField(Permission, blank=True,
                                         related_name="member_teams",
                                         verbose_name=_("Permissions"))

    # manager permissions
    manager_permissions = models.ManyToManyField(Permission, blank=True,
                                                 related_name="manager_teams",
                                                 verbose_name=_("Manager permissions"))

    # team permissions
    team_permissions = models.ManyToManyField(Permission, blank=True,
                                                 related_name="team_teams",
                                                 verbose_name=_("Team in team permissions"))

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")
        ordering = ("name", "creator",)

    @property
    def get_absolute_url(self):
        return reverse("teams:team_detail", args=[self.slug])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = create_slug(self.name)
        self.full_clean()
        super().save(*args, **kwargs)

    def get_state_for_user(self, user):
        try:
            return self.memberships.get(user=user).state
        except Membership.DoesNotExist:
            return None

    def applicants(self):
        return self.memberships.filter(state="applied")

    def invitees(self):
        return self.memberships.filter(state="invited")

    def members(self):
        return self.memberships.filter(state="member")

    def managers(self):
        return self.memberships.filter(state="manager")

    def teams(self):
        return self.memberships.filter(state="team")


class AbstractBaseMembership(CremeEntity):

    STATE_APPLIED = "applied"
    STATE_INVITED = "invited"
    STATE_DECLINED = "declined"
    STATE_REJECTED = "rejected"
    STATE_ACCEPTED = "accepted"
    STATE_WAITLISTED = "waitlisted"
    STATE_AUTO_JOINED = "auto-joined"
    STATE_MEMBER = "member"

    ROLE_MEMBER = "member"
    ROLE_MANAGER = "manager"
    ROLE_TEAM = "team"
    ROLE_OWNER = "owner"

    STATE_CHOICES = [
        (STATE_APPLIED, _("applied")),
        (STATE_INVITED, _("invited")),
        (STATE_DECLINED, _("declined")),
        (STATE_REJECTED, _("rejected")),
        (STATE_ACCEPTED, _("accepted")),
        (STATE_WAITLISTED, _("waitlisted")),
        (STATE_AUTO_JOINED, _("auto joined"))
    ]

    ROLE_CHOICES = [
        (ROLE_MEMBER, _("member")),
        (ROLE_MANAGER, _("manager")),
        (ROLE_TEAM, _("team")),
        (ROLE_OWNER, _("owner"))
    ]

    state = models.CharField(max_length=20, choices=STATE_CHOICES, verbose_name=_("state"))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER, verbose_name=_("role"))

    class Meta:
        abstract = True

    def is_owner(self):
        return self.role == AbstractBaseMembership.ROLE_OWNER

    def is_manager(self):
        return self.role == AbstractBaseMembership.ROLE_MANAGER

    def is_team(self):
        return self.role == AbstractBaseMembership.ROLE_TEAM

    def is_member(self):
        return self.role == AbstractBaseMembership.ROLE_MEMBER

    def promote(self, by):
        role = self.team.role_for(by)
        if role in [AbstractBaseMembership.ROLE_MANAGER, AbstractBaseMembership.ROLE_OWNER]:
            if self.role == Membership.ROLE_MEMBER:
                self.role = Membership.ROLE_MANAGER
                self.save()
                signals.promoted_member.send(sender=self, membership=self, by=by)
                return True
        return False

    def demote(self, by):
        role = self.team.role_for(by)
        if role in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
            if self.role == Membership.ROLE_MANAGER:
                self.role = Membership.ROLE_MEMBER
                self.role = Membership.ROLE_TEAM
                self.save()
                signals.demoted_member.send(sender=self, membership=self, by=by)
                return True
        return False

    def accept(self, by):
        role = self.team.role_for(by)
        if role in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
            if self.state == Membership.STATE_APPLIED:
                self.state = Membership.STATE_ACCEPTED
                self.save()
                signals.accepted_membership.send(sender=self, membership=self)
                return True
        return False

    def reject(self, by):
        role = self.team.role_for(by)
        if role in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
            if self.state == Membership.STATE_APPLIED:
                self.state = Membership.STATE_REJECTED
                self.save()
                signals.rejected_membership.send(sender=self, membership=self)
                return True
        return False

    def joined(self):
        self.user = self.invite.to_user
        if self.team.manager_access == Team.MANAGER_ACCESS_ADD:
            self.state = Membership.STATE_AUTO_JOINED
        else:
            self.state = Membership.STATE_INVITED
        self.save()

    def status(self):
        if self.user:
            return self.get_state_display()
        if self.invite:
            return self.invite.get_status_display()
        return "Unknown"

    def resend_invite(self, by=None):
        if self.invite is not None:
            code = self.invite.signup_code
            code.expiry = timezone.now() + datetime.timedelta(days=5)
            code.save()
            code.send()
            signals.resent_invite.send(sender=self, membership=self, by=by)

    def remove(self, by=None):
        if self.invite is not None:
            self.invite.signup_code.delete()
            self.invite.delete()
        self.delete()
        signals.removed_membership.send(sender=Membership, team=self.team, user=self.user, invitee=self.invitee, by=by)

    @property
    def invitee(self):
        return self.user or self.invite.to_user_email()


class SimpleMembership(AbstractBaseMembership):

    #team = models.ForeignKey(SimpleTeam, related_name="memberships", verbose_name=_("team"), on_delete=models.CASCADE)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="simple_memberships", null=True, blank=True, verbose_name=_("user"), on_delete=models.SET_NULL)
    #invite = models.ForeignKey(JoinInvitation, related_name="simple_memberships", null=True, blank=True, verbose_name=_("invite"), on_delete=models.SET_NULL)

    #def __str__(self):
    #    return f"{self.user} in {self.invite}"

    class Meta:
        #unique_together = [("invite")]
        verbose_name = _("Simple Membership")
        verbose_name_plural = _("Simple Memberships")
        ordering = ("state",)


class Membership(AbstractBaseMembership):

    #user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="memberships", null=True, blank=True, verbose_name=_("User"), on_delete=models.SET_NULL)
    #team = models.ForeignKey(Team, related_name="memberships", verbose_name=_("Team"), on_delete=models.CASCADE)
    #invite = models.ForeignKey(JoinInvitation, related_name="memberships", null=True, blank=True, verbose_name=_("invite"), on_delete=models.SET_NULL)
    state = models.CharField(max_length=20, choices=MEMBERSHIP_STATE_CHOICES, verbose_name=_("State"))
    message = models.TextField(blank=True, verbose_name=_("Message"))

    def __str__(self):
        return f"{self.message} in {self.state}"

    class Meta:
        #unique_together = [("invite")]
        verbose_name = _("Membership")
        verbose_name_plural = _("Memberships")
        ordering    =   ("state",)


# Manage the related User ------------------------------------------------------

def _get_linked_team(self):
    if self.is_team:
        return None

    team = getattr(self, '_linked_team_cache', None)

    if team is None:
        model = get_team_model()
        teams = model.objects.filter(is_user=self)[:2]

        if not teams:
            logger.critical(
                'User "%s" has no related Team => we create it',
                self.username,
            )
            team = model._create_linked_team(self)
        else:
            if len(teams) > 1:
                # TODO: repair ? (beware to race condition)
                logger.critical(
                    'User "%s" has several related Teams !',
                    self.username,
                )

            team = teams[0]

    self._linked_team_cache = team

    return team


reversion.register(SimpleMembership)
reversion.register(Membership)