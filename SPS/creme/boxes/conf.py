"""
@@@ this is temporary until we have solved using AppConfig instead

    tracking: https://github.com/pinax/django-user-accounts/issues/184
"""
import importlib

from django.conf import settings  # noqa
from django.core.exceptions import ImproperlyConfigured
from ..utils import load_path_attr
from appconf import AppConf


class BoxesAppConf(AppConf):

    HOOKSET = "creme.boxes.hooks.DefaultHookSet"

    class Meta:
        prefix = "boxes"

    def configure_hookset(self, value):
        return load_path_attr(value)()
