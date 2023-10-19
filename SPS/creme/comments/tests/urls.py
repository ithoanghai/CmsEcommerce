from django.urls import include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    re_path(r"^comment/", include("comments.urls", namespace="comments")),
    re_path(r"^demo/", TemplateView.as_view(), name="demo_detail"),
]
