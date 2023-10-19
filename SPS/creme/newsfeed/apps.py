from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NewsfeedConfig(AppConfig):
    name = 'creme.newsfeed'
    label = 'newsfeed'
    verbose_name = _('Newsfeed')