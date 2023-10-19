from django.urls import re_path

from .views import user_list

app_name = "creme.conference"

urlpatterns = [
    re_path(r"^users/", user_list, name="user_list"),
]
