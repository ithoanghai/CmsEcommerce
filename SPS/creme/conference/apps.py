from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ConferenceConfig(AppConfig):
    name = "creme.conference"
    label = "conference"
    verbose_name = _("Conference")
