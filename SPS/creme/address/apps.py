from django.utils.translation import gettext_lazy as _

from ..creme_core.core.application import OscarConfig


class AddressConfig(OscarConfig):
    label = 'address'
    name = 'creme.address'
    verbose_name = _('Address')
