from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "creme.phoneconfirm"
    label = "phoneconfirm"
    verbose_name = _("Phoneconfirm")
