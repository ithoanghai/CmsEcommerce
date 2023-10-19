import importlib

from django.conf import settings  # noqa
from django.core.exceptions import ImproperlyConfigured

from appconf import AppConf


def load_path_attr(path):
    i = path.rfind(".")
    module, attr = path[:i], path[i + 1:]
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured(f"Error importing {module}: '{e}'")
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured(f"Module '{module}' does not define a '{attr}'")
    return attr


class WikiAppConf(AppConf):

    BINDERS = [
        "creme.wiki.binders.DefaultBinder"
    ]
    IP_ADDRESS_META_FIELD = "HTTP_X_FORWARDED_FOR"
    HOOKSET = "creme.wiki.hooks.WikiDefaultHookset"
    PARSE = "creme.wiki.parsers.wiki_parse"

    class Meta:
        prefix = "wiki"

    def configure_binders(self, value):
        binders = []
        for val in value:
            binders.append(load_path_attr(val)())
        return binders

    def configure_hookset(self, value):
        return load_path_attr(value)()

    def configure_parse(self, value):
        return load_path_attr(value)
