import importlib

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "creme.stripe"
    label = "stripe"
    verbose_name = _("Stripe")

    def ready(self):
        importlib.import_module("creme.stripe.webhooks")
