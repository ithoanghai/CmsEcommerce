from django.urls import re_path
from django.views.generic import View

urlpatterns = [
    re_path(r"^(?P<year>\d{4})/(?P<month>\d{1,2})/", View.as_view(), name="monthly"),
    re_path(r"^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/", View.as_view(), name="daily"),
]
