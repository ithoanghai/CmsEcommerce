from django.utils.translation import gettext_lazy as _

from ..creme_config.apps import CremeAppConfig as OscarConfig


class PartnerConfig(OscarConfig):
    label = 'partner'
    name = 'creme.partner'
    verbose_name = _('Partner')

    def ready(self):
        from . import receivers  # noqa
