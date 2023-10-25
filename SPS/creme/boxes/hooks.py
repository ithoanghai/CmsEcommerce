class DefaultHookSet(object):

    def parse_content(self, content):
        return content


class HookProxy:

    def __getattr__(self, attr):
        from .conf import settings  # if put globally there is a race condition
        return getattr(settings.BOXES_HOOKSET, attr)


hookset = HookProxy()
