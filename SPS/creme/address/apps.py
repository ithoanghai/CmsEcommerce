from django.utils.translation import gettext_lazy as _

from ..creme_config.apps import CremeAppConfig as OscarConfig


class AddressConfig(OscarConfig):
    label = 'address'
    name = 'creme.address'
    verbose_name = _('Address')
