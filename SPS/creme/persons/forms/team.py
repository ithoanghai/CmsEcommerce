from __future__ import unicode_literals
from django import forms
from django.contrib.auth import get_user_model
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from ...creme_core.auth.forms import SignupForm
from ...creme_core.models import Account, CremeUser

from django.conf import settings
from ..hooks import hookset
from ..models import Membership, Team, create_slug

#MESSAGE_STRINGS = hookset.get_message_strings()
MESSAGE_STRINGS = ''


class TeamSignupForm(SignupForm):

    team = forms.CharField(label=_("Team"), max_length=50, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.keyOrder = [
            "team",
            "username",
            "password",
            "password_confirm",
            "email",
            "code"
        ]


class TeamForm(forms.ModelForm):

    def clean_name(self):
        slug = create_slug(self.cleaned_data["name"])
        if self.instance.pk is None and Team.objects.filter(slug=slug).exists():
            raise forms.ValidationError(MESSAGE_STRINGS["slug-exists"])
        if self.cleaned_data["name"].lower() in settings.TEAMS_NAME_BLACKLIST:
            raise forms.ValidationError(MESSAGE_STRINGS["on-team-blacklist"])
        return self.cleaned_data["name"]

    class Meta:
        model = Team
        fields = [
            "name",
            "avatar",
            "description",
            "member_access",
            "manager_access"
        ]


class TeamInviteUserForm(forms.Form):

    invitee = forms.CharField(label="Person to invite")
    role = forms.ChoiceField(choices=Membership.ROLE_CHOICES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop("team")
        super().__init__(*args, **kwargs)
        self.fields["invitee"].widget.attrs["data-autocomplete-url"] = hookset.build_team_url(
            "team_autocomplete_users",
            self.team.slug
        )
        self.fields["invitee"].widget.attrs["placeholder"] = "email address"

    def clean_invitee(self):
        CremeUser = get_user_model()
        try:
            invitee = CremeUser.objects.get(email=self.cleaned_data["invitee"])
            if self.team.is_on_team(invitee):
                raise forms.ValidationError(MESSAGE_STRINGS["user-member-exists"])
        except CremeUser.DoesNotExist:
            try:
                # search by USERNAME_FIELD
                params = {CremeUser.USERNAME_FIELD: self.cleaned_data["invitee"]}
                invitee = CremeUser.objects.get(**params)
                if self.team.is_on_team(invitee):
                    raise forms.ValidationError(MESSAGE_STRINGS["user-member-exists"])
            except CremeUser.DoesNotExist:
                invitee = self.cleaned_data["invitee"]
                if self.team.memberships.filter(invite__signup_code__email=invitee).exists():
                    raise forms.ValidationError(MESSAGE_STRINGS["invitee-member-exists"])
        return invitee


class TeamInvitationForm(forms.Form):

    email = forms.EmailField(label=_("Email"),
                             help_text=_("email address must be that of an account on this "
                                         "conference site"))

    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop("team")
        super(TeamInvitationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(TeamInvitationForm, self).clean()
        email = cleaned_data.get("email")

        if email is None:
            raise forms.ValidationError(_("valid email address required"))

        try:
            user = CremeUser.objects.get(email=email)
        except CremeUser.DoesNotExist:
            # eventually we can invite them but for now assume they are
            # already on the site
            raise forms.ValidationError(
                mark_safe(_("no account with email address <b>%s</b> found on this conference "
                          "site") % escape(email)))

        state = self.team.get_state_for_user(user)

        if state in ["member", "manager"]:
            raise forms.ValidationError(_("user already in team"))

        if state in ["invited"]:
            raise forms.ValidationError(_("user already invited to team"))

        self.user = user
        self.state = state

        return cleaned_data

    def invite(self):
        if self.state is None:
            Membership.objects.create(team=self.team, user=self.user, state="invited")
        elif self.state == "applied":
            # if they applied we shortcut invitation process
            membership = Membership.objects.filter(team=self.team, user=self.user)
            membership.update(state="member")
