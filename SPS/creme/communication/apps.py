from django.utils.translation import gettext_lazy as _

from ..creme_core.core.application import OscarConfig


class CommunicationConfig(OscarConfig):
    label = 'communication'
    name = 'creme.communication'
    verbose_name = _('Communication')
