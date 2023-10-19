import importlib

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "creme.waitinglist"
    label = "waitinglist"
    verbose_name = _("Waiting List")

    def ready(self):
        importlib.import_module("creme.waitinglist.receivers")
