from django.db import models

from .conf import settings


class TimeZoneField(models.CharField):

    def __init__(self, *args, **kwargs):
        defaults = {
            "max_length": 100,
            "default": "",
            "choices": settings.AUTH_TIMEZONES,
            "blank": True,
        }
        defaults.update(kwargs)
        return super(TimeZoneField, self).__init__(*args, **defaults)
