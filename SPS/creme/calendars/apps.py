from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "creme.calendars"
    label = "calendars"
    verbose_name = _("Calendars")
