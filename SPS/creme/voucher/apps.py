from django.utils.translation import gettext_lazy as _

from ..creme_config.apps import CremeAppConfig as OscarConfig


class VoucherConfig(OscarConfig):
    label = 'voucher'
    name = 'creme.voucher'
    verbose_name = _('Voucher')

    def ready(self):
        from . import receivers  # noqa
