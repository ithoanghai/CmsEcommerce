from django.urls import re_path, include, path

from creme.creme_core.accounts.forms import SignupForm, ChangePasswordForm, SettingsForm, PasswordResetForm, \
    PasswordResetTokenForm, LoginUsernameForm
from django.utils.http import int_to_base36

from .base import ViewConfig

patch = "http://pinaxproject.com/pinax-design/patches/django-user-accounts.svg"
label = "dua"
title = "Django User Accounts"
views = [
    ViewConfig(pattern="accounts/signup/", template="app_list/accounts/signup.html", name="signup", pattern_kwargs={}, form=SignupForm()),
    ViewConfig(pattern="accounts/login/", template="app_list/accounts/login.html", name="login", pattern_kwargs={}, form=LoginUsernameForm(), ACCOUNT_OPEN_SIGNUP=True),
    ViewConfig(pattern="accounts/logout/", template="app_list/accounts/logout.html", name="logout", pattern_kwargs={}),
    ViewConfig(pattern="accounts/confirm_email/<key>/", template="app_list/accounts/email_confirm.html", name="confirm_email", pattern_kwargs={"key": "foo"}, confirmation={"key": "foo", "email_address": {"email": "example@sample.com"}}),
    ViewConfig(pattern="accounts/password/", template="app_list/accounts/password_change.html", name="password", pattern_kwargs={}, form=ChangePasswordForm(user=None)),
    ViewConfig(pattern="accounts/password/reset/", template="app_list/accounts/password_reset.html", name="password_reset", pattern_kwargs={}, form=PasswordResetForm()),
    #ViewConfig(pattern="accounts/password/reset/<uid>/<token>/", template="app_list/accounts/password_reset_token.html", name="password_reset_token", pattern_kwargs={"uidb36": int_to_base36(100),"token": "notoken"}, form=PasswordResetTokenForm()),
    ViewConfig(pattern="accounts/settings/", template="app_list/accounts/settings.html", name="account_settings", pattern_kwargs={}, form=SettingsForm()),
    ViewConfig(pattern="accounts/delete/", template="app_list/accounts/delete.html", name="account_delete", pattern_kwargs={}),
]
urlpatterns = [
    view.url()
    for view in views
]
url = path("", include("SaleSystemPortal.configs.dua"))
