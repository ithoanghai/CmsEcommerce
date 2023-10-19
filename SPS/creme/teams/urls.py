from django.urls import re_path, path

from .views import (
    team_detail,
    team_join,
    team_leave,
    team_apply,
    team_promote,
    team_demote,
    team_accept,
    team_reject, TeamListView, TeamCreateView, TeamsListView, TeamsDetailView
)

app_name = "teams"


urlpatterns = [
    # overall
    re_path(r"^$", TeamListView.as_view(), name="team_list"),
    re_path(r"^create/", TeamCreateView.as_view(), name="team_create"),

    # team specific
    #re_path(r"^(?P<slug>[\w\-]+)/", team_detail, name="team_detail"),
    re_path(r"^(?P<slug>[\w\-]+)/join/", team_join, name="team_join"),
    re_path(r"^(?P<slug>[\w\-]+)/leave/", team_leave, name="team_leave"),
    re_path(r"^(?P<slug>[\w\-]+)/apply/", team_apply, name="team_apply"),

    # membership specific
    re_path(r"^promote/<int:pk>/", team_promote, name="team_promote"),
    re_path(r"^demote/<int:pk>/", team_demote, name="team_demote"),
    re_path(r"^accept/<int:pk>/", team_accept, name="team_accept"),
    re_path(r"^reject/<int:pk>/", team_reject, name="team_reject"),
]

urlpatterns = urlpatterns + [
    path("", TeamsListView.as_view()),
    path("<int:pk>/", TeamsDetailView.as_view()),
]
