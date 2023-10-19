from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MailerConfig(AppConfig):
    name = 'creme.mailer'
    default_auto_field = 'django.db.models.BigAutoField'
    label = 'mailer'
    verbose_name = _('Mailer')