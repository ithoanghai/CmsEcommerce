from django.utils.translation import gettext_lazy as _

from ..creme_config.apps import CremeAppConfig as OscarConfig


class ShippingConfig(OscarConfig):
    label = 'shipping'
    name = 'creme.shipping'
    verbose_name = _('Shipping')
