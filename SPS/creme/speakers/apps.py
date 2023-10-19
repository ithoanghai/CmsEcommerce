from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SpeakersConfig(AppConfig):
    name = "creme.speakers"
    label = "speakers"
    verbose_name = _("Speakers")
