# flake8: noqa
from django.urls import re_path
from django.views.generic import TemplateView

from .views import flag

app_name = "flag"

urlpatterns = [
    re_path(r"^$", flag, name="flag"),
    re_path(r'^thank_you', TemplateView.as_view(template_name="flag/thank_you.html"), name='flag-reported'),
]
