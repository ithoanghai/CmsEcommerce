from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OpportunityConfig(AppConfig):
    name = "creme.opportunity"
    label = 'opportunity'
    verbose_name = _('Opportunity')
