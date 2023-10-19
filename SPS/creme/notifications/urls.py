from django.urls import path,re_path
from .views import *

app_name = "notifications"

urlpatterns = [
    path('mark-notifications-as-read', mark_like_comment_notifications_as_read, name="mark-as-read"),
    path("list/", UserAllNotificationListView.as_view(), name="list"),
]
