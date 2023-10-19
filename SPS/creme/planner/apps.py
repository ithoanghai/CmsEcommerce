from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlannerConfig(AppConfig):
    name = "creme.planner"
    label = 'planner'
    verbose_name = _('Planner')