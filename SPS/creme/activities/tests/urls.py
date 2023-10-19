from django.urls import include, re_path


urlpatterns = [
    re_path(r"^", include("activities.urls"), name="test_activities"),
]
