import importlib

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "creme.invitations"
    label = "invitations"
    verbose_name = _("Invitations")

    def ready(self):
        importlib.import_module("creme.invitations.receivers")
