from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "creme.blogs"

    def ready(self):
        import_module("creme.blogs.receivers")
