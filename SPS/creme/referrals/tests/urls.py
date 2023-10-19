from django.urls import include, path

urlpatterns = [
    path("", include("referrals.urls", namespace="referrals")),
]
