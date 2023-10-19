import importlib

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "creme.wiki"
    label = "wiki"
    verbose_name = _("Wiki")

    def ready(self):
        importlib.import_module("creme.wiki.receivers")
