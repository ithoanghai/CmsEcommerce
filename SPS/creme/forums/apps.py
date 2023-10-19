from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "creme.forums"
    label = "forums"
    verbose_name = "Fourms"

    def ready(self):
        import_module("creme.forums.receivers")
