from django.utils.translation import gettext_lazy as _

from ..creme_core.core.application import OscarConfig


class OrderConfig(OscarConfig):
    label = 'order'
    name = 'creme.order'
    verbose_name = _('Order')
