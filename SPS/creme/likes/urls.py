from django.urls import re_path, include, path
from django.http import HttpResponse
from . import views

def dummy_view():
    return HttpResponse(content=b"", status=200)

app_name = "likes"

urlpatterns = [
    re_path(r"^dummy_login/", dummy_view, name="login"),
    re_path(r"^like/(?P<content_type_id>\d+):(?P<object_id>\d+)/",
        views.LikeToggleView.as_view(),
        name="like_toggle")
]
