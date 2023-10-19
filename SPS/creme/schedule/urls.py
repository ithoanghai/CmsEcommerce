from __future__ import unicode_literals
from django.urls import re_path

from .views import (
    schedule_conference,
    schedule_edit,
    schedule_list,
    schedule_list_csv,
    schedule_presentation_detail,
    schedule_detail,
    schedule_slot_edit,
    schedule_json,
    session_staff_email,
    session_list,
    session_detail,
)

app_name = "schedules"


urlpatterns = [
    #re_path(r"^", schedule_conference, name="schedule_conference"),
    re_path(r"^edit/", schedule_edit, name="schedule_edit"),
    re_path(r"^list/", schedule_list, name="schedule_list"),
    re_path(r"^presentations.csv", schedule_list_csv, name="schedule_list_csv"),
    re_path(r"^presentation/(\d+)/", schedule_presentation_detail, name="schedule_presentation_detail"),
    #re_path(r"^([\w\-]+)/", schedule_detail, name="schedule_detail"),
    re_path(r"^([\w\-]+)/edit/", schedule_edit, name="schedule_edit"),
    re_path(r"^([\w\-]+)/list/", schedule_list, name="schedule_list"),
    re_path(r"^([\w\-]+)/presentations.csv$", schedule_list_csv, name="schedule_list_csv"),
    re_path(r"^([\w\-]+)/edit/slot/(\d+)/", schedule_slot_edit, name="schedule_slot_edit"),
    re_path(r"^conference.json", schedule_json, name="schedule_json"),
    re_path(r"^sessions/staff.txt$", session_staff_email, name="schedule_session_staff_email"),
    re_path(r"^sessions/", session_list, name="schedule_session_list"),
    re_path(r"^session/(\d+)/", session_detail, name="schedule_session_detail"),
]
