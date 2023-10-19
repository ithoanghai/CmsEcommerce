import importlib

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "creme.teams"
    label = "teams"
    verbose_name = _("Teams")

    def ready(self):
        importlib.import_module("creme.teams.receivers")
