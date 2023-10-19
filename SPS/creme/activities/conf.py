from django.conf import settings  # noqa

from appconf import AppConf

from .utils import load_path_attr


class PinaxLmsActivitiesAppConf(AppConf):

    ACTIVITIES = {}
    HOOKSET = "activities.hooks.ActivitiesDefaultHookSet"

    class Meta:
        prefix = "lms_activities"

    def configure_hookset(self, value):
        return load_path_attr(value)()
