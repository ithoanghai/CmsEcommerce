from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "creme.comments"
    label = "comments"
    verbose_name = _("Comments")
