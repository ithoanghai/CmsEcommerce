from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "creme.creme_core.auth"
    label = "accounts"
    verbose_name = _("Accounts")
