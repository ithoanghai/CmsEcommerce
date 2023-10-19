from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LeadsConfig(AppConfig):
    name = "creme.leads"
    label = 'leads'
    verbose_name = _('Leads')