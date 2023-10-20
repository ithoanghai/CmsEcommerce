from django.utils.translation import gettext_lazy as _

from ..creme_config.apps import CremeAppConfig as OscarConfig


class PaymentConfig(OscarConfig):
    label = 'payment'
    name = 'creme.payment'
    verbose_name = _('Payment')
