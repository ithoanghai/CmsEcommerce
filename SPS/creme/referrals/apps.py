from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "creme.referrals"
    verbose_name = _("Referrals")
    default_auto_field = "django.db.models.AutoField"
