import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class DefaultHookSet(object):

    def __init__(self):
        from .conf import settings  # if put globally there is a race condition
        self.settings = settings

    def parse_content(self, content):
        return self.settings.PAGES_MARKUP_RENDERER(content)

    def validate_path(self, path):
        if not re.match(self.settings.PAGES_PAGE_REGEX, path):
            raise ValidationError({
                "path": [
                    _("Path can only contain letters, numbers and hyphens and end with /")
                ]
            })


class HookProxy:

    def __getattr__(self, attr):
        from .conf import settings  # if put globally there is a race condition
        return getattr(settings.PAGES_HOOKSET, attr)


hookset = HookProxy()
