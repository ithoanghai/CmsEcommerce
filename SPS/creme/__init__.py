# Use 'alpha', 'beta', 'rc' or 'final' as the 4th element to indicate release type.
VERSION = (1, 0, 0, 'alpha')


def get_short_version():
    return '%s.%s' % (VERSION[0], VERSION[1])


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    # Append 3rd digit if > 0
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    elif VERSION[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        version = '%s%s' % (version, mapping[VERSION[3]])
        if len(VERSION) == 5:
            version = '%s%s' % (version, VERSION[4])
    return version


# App registry hooking ---------------------------------------------------------

try:
    from django.apps.config import AppConfig
    from django.apps.registry import Apps
except ImportError:
    # This error may appear with old versions of setuptools during installation
    import sys

    sys.stderr.write(
        'Django is not installed ; '
        'ignore this message if you are installing SPS.'
    )
else:
    AppConfig.all_apps_ready = lambda self: None

    _original_populate = Apps.populate

    def _hooked_populate(self, installed_apps=None):
        if self.ready:
            return

        if getattr(self, '_all_apps_ready', False):
            return
        _original_populate(self, installed_apps)

        with self._lock:
            if getattr(self, '_all_apps_ready', False):
                return

            for app_config in self.get_app_configs():
                app_config.all_apps_ready()

            self._all_apps_ready = True

    Apps.populate = _hooked_populate
