from django.urls import re_path

from .views import badge_detail, badge_list

app_name = "badges"

urlpatterns = [
    re_path(r"^$", badge_list, name="badge_list"),
    re_path(r"^(\w+)/(\d+)/", badge_detail, name="badge_detail"),
]
