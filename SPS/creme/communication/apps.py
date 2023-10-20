from django.utils.translation import gettext_lazy as _

from ..creme_config.apps import CremeAppConfig as OscarConfig


class CommunicationConfig(OscarConfig):
    label = 'communication'
    name = 'creme.communication'
    verbose_name = _('Communication')
