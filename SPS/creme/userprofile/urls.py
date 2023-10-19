from django.urls import path
from .views import ProfileEditView, TimelineView, profile_list, FriendView


app_name = "profile"

urlpatterns = [
    path('edit-profile', ProfileEditView.as_view(), name="edit-profile"),
    path('timeline/<slug:username>', TimelineView.as_view(), name="user-timeline"),
    path("profile_list/", profile_list, name="profile_list"),
    path("friend/<slug:username>", FriendView.as_view(), name="friend"),
]
