from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ScheduleConfig(AppConfig):
    name = "creme.schedule"
    label = "schedule"
    verbose_name = _("Schedule")
