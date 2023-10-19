from django.urls import re_path

from .views import (
    AddToAllView,
    AddToUserView,
    InviteStatView,
    InviteView,
    TopOffAllView,
    TopOffUserView,
)

app_name = "invitations"

urlpatterns = [
    re_path(r"^invite/", InviteView.as_view(), name="invite"),
    re_path(r"^invite-stat/<int:pk>/", InviteStatView.as_view(), name="invite_stat"),
    re_path(r"^topoff/", TopOffAllView.as_view(), name="topoff_all"),
    re_path(r"^topoff/<int:pk>/", TopOffUserView.as_view(), name="topoff_user"),
    re_path(r"^addto/", AddToAllView.as_view(), name="addto_all"),
    re_path(r"^addto/<int:pk>/", AddToUserView.as_view(), name="addto_user"),
]
