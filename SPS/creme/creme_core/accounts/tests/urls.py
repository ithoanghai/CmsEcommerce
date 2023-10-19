from django.urls import include, re_path

urlpatterns = [
    re_path(r"^", include("creme.creme_core.accounts.urls")),
]
