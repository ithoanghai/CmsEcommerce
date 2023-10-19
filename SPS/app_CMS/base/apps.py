from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_CMS.base'
    label = "CmsConfig"
    verbose_name = _("CMS")
