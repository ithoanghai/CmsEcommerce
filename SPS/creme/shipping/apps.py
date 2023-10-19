from django.utils.translation import gettext_lazy as _

from ..creme_core.core.application import OscarConfig


class ShippingConfig(OscarConfig):
    label = 'shipping'
    name = 'creme.shipping'
    verbose_name = _('Shipping')
