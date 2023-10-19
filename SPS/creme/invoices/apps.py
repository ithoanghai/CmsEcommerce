from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InvoicesConfig(AppConfig):
    name = "creme.invoices"
    label = 'invoices'
    verbose_name = _('Invoices')
