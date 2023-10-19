from django.urls import include, re_path

urlpatterns = [
    re_path(r"^", include("creme.reviews.urls", namespace="reviews")),
]
