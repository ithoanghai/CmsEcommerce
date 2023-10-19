from django.urls import re_path

from .views import (
    AnnouncementCreateView,
    AnnouncementDeleteView,
    AnnouncementDetailView,
    AnnouncementDismissView,
    AnnouncementListView,
    AnnouncementUpdateView,
)

app_name = "announcement"

urlpatterns = [
    re_path(r"^", AnnouncementListView.as_view(), name="announcement_list"),
    re_path(r"^create/", AnnouncementCreateView.as_view(), name="announcement_create"),
    re_path(r"^<int:pk>/", AnnouncementDetailView.as_view(), name="announcement_detail"),
    re_path(r"^<int:pk>/hide/", AnnouncementDismissView.as_view(), name="announcement_dismiss"),
    re_path(r"^<int:pk>/update/", AnnouncementUpdateView.as_view(), name="announcement_update"),
    re_path(r"^<int:pk>/delete/", AnnouncementDeleteView.as_view(), name="announcement_delete"),
]
