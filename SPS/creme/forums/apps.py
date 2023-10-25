from importlib import import_module

from django.apps import AppConfig as BaseAppConfig
from ..utils import load_path_attr

class AppConfig(BaseAppConfig):

    name = "creme.forums"
    label = "forums"
    verbose_name = "Fourms"

    EDIT_TIMEOUT = dict(minutes=3)
    HOOKSET = "creme.forums.hooks.ForumsDefaultHookSet"

    def configure_hookset(self, value):
        return load_path_attr(value)()

    class Meta:
        prefix = "forums"

    def ready(self):
        import_module("creme.forums.receivers")

