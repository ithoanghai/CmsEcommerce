import importlib

from django.conf import settings  # noqa
from django.core.exceptions import ImproperlyConfigured
from ..utils import load_path_attr
from appconf import AppConf


class CommentsAppConf(AppConf):

    HOOKSET = "comments.hooks.CommentsDefaultHookSet"

    def configure_hookset(self, value):
        return load_path_attr(value)()
