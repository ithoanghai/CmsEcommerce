from django.utils.translation import gettext_lazy as _

from ..creme_config.apps import CremeAppConfig as OscarConfig


class OrderConfig(OscarConfig):
    label = 'order'
    name = 'creme.order'
    verbose_name = _('Order')
