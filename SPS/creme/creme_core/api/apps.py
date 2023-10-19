from __future__ import unicode_literals

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "creme.api"
    label = "api"
    verbose_name = _("Api")
