from django.utils.translation import gettext_lazy as _

from ..creme_config.apps import CremeAppConfig as OscarConfig


class AnalyticsConfig(OscarConfig):
    label = 'analytics'
    name = 'creme.analytics'
    verbose_name = _('Analytics')

    def ready(self):
        from . import receivers  # noqa
