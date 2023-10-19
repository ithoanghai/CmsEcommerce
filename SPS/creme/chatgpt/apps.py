from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ChatgptConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'creme.chatgpt'
    label = "chatgpt"
    verbose_name = _("Chatgpt")
