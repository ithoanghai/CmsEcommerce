import re
from collections import OrderedDict

from django import forms
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.forms import AuthenticationForm

from ..models.auth import User, EmailAddress
from .conf import settings
from .hooks import hookset
from .utils import get_user_lookup_kwargs

alnum_re = re.compile(r"^[\w\-\.\+]+$")

User = get_user_model()
USER_FIELD_MAX_LENGTH = getattr(User, User.USERNAME_FIELD).field.max_length


class PasswordField(forms.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", forms.PasswordInput(render_value=False))
        self.strip = kwargs.pop("strip", True)
        super(PasswordField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return ""
        value = force_str(value)
        if self.strip:
            value = value.strip()
        return value


class SignupForm(forms.Form):

    username = forms.CharField(
        label=_("Username"),
        max_length=USER_FIELD_MAX_LENGTH,
        widget=forms.TextInput(),
        required=True
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput(), required=True
    )
    password = PasswordField(
        label=_("Password"),
        strip=settings.ACCOUNTS_PASSWORD_STRIP,
    )
    password_confirm = PasswordField(
        label=_("Password (again)"),
        strip=settings.ACCOUNTS_PASSWORD_STRIP,
    )
    code = forms.CharField(
        max_length=64,
        required=False,
        widget=forms.HiddenInput()
    )

    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(
                _("Usernames can only contain letters, numbers and the following special characters ./+/-/_")
            )
        lookup_kwargs = get_user_lookup_kwargs({
            "{username}__iexact": self.cleaned_data["username"]
        })
        qs = User.objects.filter(**lookup_kwargs)
        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))

    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))

    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data


class UserRegistrationForm(UserCreationForm):
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        #self.fields['gender'].widget.attrs.update({'placeholder': 'Enter Gender'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Repeat your password'})
        # self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label or 'email@address.nl'

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  #"gender",
                  "password1",
                  "password2")

        # widgets = {
        #     'password1': forms.TextInput(attrs={'placeholder': 'Password'}),
        #     'password2': forms.TextInput(attrs={'placeholder': 'Repeat your password'}),
        # }

    def clean_username(self):
        username = self.cleaned_data['username']
        #print(username)
        if ' ' in username:
            raise forms.ValidationError("Username can't contain spaces.")
        return username

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        # return self.cleaned_data
        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class LoginForm(forms.Form):

    password = PasswordField(
        label=_("Password"),
        strip=settings.ACCOUNTS_PASSWORD_STRIP,
    )
    remember = forms.BooleanField(
        label=_("Remember Me"),
        required=False
    )
    user = None

    def clean(self):
        if self._errors:
            return
        user = auth.authenticate(**self.user_credentials())
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_("This account is inactive."))
        else:
            raise forms.ValidationError(self.authentication_fail_message)
        return self.cleaned_data

    def user_credentials(self):
        return hookset.get_user_credentials(self, self.identifier_field)


class LoginUsernameForm(AuthenticationForm):

    username = forms.CharField(label=_("Username"), max_length=30, widget=forms.TextInput(attrs={'autofocus': True}))
    authentication_fail_message = _("The username and/or password you specified are not correct.")

    def __init__(self, *args, **kwargs):
        super(LoginUsernameForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

    error_messages = {
        'invalid_login': _(
            authentication_fail_message,
        ),
        'inactive': _("This account is inactive."),
    }


class LoginEmailForm(LoginForm):

    email = forms.EmailField(label=_("Email"))
    authentication_fail_message = _("The email address and/or password you specified are not correct.")
    identifier_field = "email"

    def __init__(self, *args, **kwargs):
        super(LoginEmailForm, self).__init__(*args, **kwargs)
        field_order = ["email", "password", "remember"]
        if hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)


from django import forms
from django.utils.translation import gettext as _


class ChangePasswordForm(forms.Form):
    password_current = forms.CharField(
        label=_("Current Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_new = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_new_confirm = forms.CharField(
        label=_("New Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password_current(self):
        password_current = self.cleaned_data.get("password_current")
        if not self.user.check_password(password_current):
            raise forms.ValidationError(_("Please type your current password."))
        return password_current

    def clean_password_new_confirm(self):
        password_new = self.cleaned_data.get("password_new")
        password_new_confirm = self.cleaned_data.get("password_new_confirm")

        if password_new and password_new_confirm and password_new != password_new_confirm:
            raise forms.ValidationError(_("The new passwords do not match."))

        return password_new_confirm


class PasswordResetForm(forms.Form):

    email = forms.EmailField(label=_("Email"), required=True)

    def clean_email(self):
        value = self.cleaned_data["email"]
        if not EmailAddress.objects.filter(email__iexact=value).exists():
            raise forms.ValidationError(_("Email address can not be found."))
        return value


class PasswordResetTokenForm(forms.Form):

    password = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_confirm = forms.CharField(
        label=_("New Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )

    def clean_password_confirm(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            password = self.cleaned_data["password"]
            password_confirm = self.cleaned_data["password_confirm"]
            return hookset.clean_password(password, password_confirm)
        return self.cleaned_data["password_confirm"]


class SettingsForm(forms.Form):

    email = forms.EmailField(label=_("Email"), required=True)
    timezone = forms.ChoiceField(
        label=_("Timezone"),
        choices=[("", "---------")] + settings.ACCOUNTS_TIMEZONES,
        required=False
    )
    if settings.USE_I18N:
        language = forms.ChoiceField(
            label=_("Language"),
            choices=settings.ACCOUNTS_LANGUAGES,
            required=False
        )

    def clean_email(self):
        value = self.cleaned_data["email"]
        if self.initial.get("email") == value:
            return value
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))
