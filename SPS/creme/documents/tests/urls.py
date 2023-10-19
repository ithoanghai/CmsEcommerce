from django.urls import include, re_path

urlpatterns = [
    re_path(r"^", include("documents.urls", namespace="documents")),
]
