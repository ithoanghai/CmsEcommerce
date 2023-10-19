from django.urls import include, re_path
from django.http import HttpResponse


def dummy_view():
    return HttpResponse(content=b"", status=200)


urlpatterns = [
    re_path(r"^", include("likes.urls", namespace="likes")),
    re_path(r"^dummy_login/", dummy_view, name="login"),
]
