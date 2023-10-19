from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserprofileConfig(AppConfig):
    name = 'creme.userprofile'
    label = "userprofile"
    verbose_name = _("User Profile")
