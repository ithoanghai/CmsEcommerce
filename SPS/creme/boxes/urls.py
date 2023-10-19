from django.urls import re_path

from .views import box_edit

app_name = "boxes"


urlpatterns = [
    re_path(r"^([-\w]+)/edit/", box_edit, name="box_edit"),
]
