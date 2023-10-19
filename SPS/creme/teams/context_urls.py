# include these urls instead of urls.py if you are using the WSGI + Django middlewares
# to set request.team, manually hooking up List/Create views as well as the accept/reject

from django.urls import re_path

from . import views

app_name = "creme.teams"


urlpatterns = [
    # team specific
    re_path(r"^detail/", views.team_detail, name="team_detail"),
    re_path(r"^join/", views.team_join, name="team_join"),
    re_path(r"^leave/", views.team_leave, name="team_leave"),
    re_path(r"^apply/", views.team_apply, name="team_apply"),
    re_path(r"^edit/", views.team_update, name="team_edit"),
    re_path(r"^manage/", views.TeamManageView.as_view(), name="team_manage"),
    re_path(r"^ac/users-to-invite/", views.autocomplete_users, name="team_autocomplete_users"),  # noqa
    re_path(r"^invite-user/", views.TeamInviteView.as_view(), name="team_invite"),
    re_path(r"^members/<int:pk>/revoke-invite/", views.team_member_revoke_invite, name="team_member_revoke_invite"),  # noqa
    re_path(r"^members/<int:pk>/resend-invite/", views.team_member_resend_invite, name="team_member_resend_invite"),  # noqa
    re_path(r"^members/<int:pk>/promote/", views.team_member_promote, name="team_member_promote"),  # noqa
    re_path(r"^members/<int:pk>/demote/", views.team_member_demote, name="team_member_demote"),  # noqa
    re_path(r"^members/<int:pk>/remove/", views.team_member_remove, name="team_member_remove"),  # noqa
]
