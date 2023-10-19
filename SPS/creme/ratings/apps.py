from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "creme.ratings"
    label = "ratings"
    verbose_name = "Ratings"

