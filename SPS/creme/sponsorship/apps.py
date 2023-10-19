from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SponsorshipConfig(AppConfig):
    name = "creme.sponsorship"
    label = "sponsorship"
    verbose_name = _("Sponsorship")
