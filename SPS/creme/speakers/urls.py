from __future__ import unicode_literals
from django.urls import re_path

from .views import (
    speaker_create,
    speaker_create_token,
    speaker_edit,
    speaker_profile,
    speaker_create_staff
)

app_name = "speaker"

urlpatterns = [
    re_path(r"^create/", speaker_create, name="speaker_create"),
    re_path(r"^create/(\w+)/", speaker_create_token, name="speaker_create_token"),
    re_path(r"^edit/(?:<int:pk>/)?$", speaker_edit, name="speaker_edit"),
    re_path(r"^profile/<int:pk>/", speaker_profile, name="speaker_profile"),
    re_path(r"^staff/create/(\d+)/", speaker_create_staff, name="speaker_create_staff"),
]
