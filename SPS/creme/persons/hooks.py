from django.db.models import Q
from django.urls import reverse


MESSAGE_STRINGS = {
    "joined-team": "Joined team.",
    "left-team": "Left team.",
    "applied-to-join": "Applied to join team.",
    "accepted-application": "Accepted application.",
    "rejected-application": "Rejected application.",
    "slug-exists": "Team with this name already exists",
    "on-team-blacklist": "You can not create a team by this name",
    "user-member-exists": "User already on team.",
    "invitee-member-exists": "Invite already sent.",
}


class TeamDefaultHookset(object):

    # allows the search field in the Membership admin
    # to be overridden if the custom user model does
    # not have a username field
    membership_search_fields = ["cremeuser__username"]

    def build_team_url(self, url_name, team_slug):
        return reverse(f"{url_name}", args=[team_slug])

    def get_autocomplete_result(self, cremeuser):
        return {"pk": cremeuser.pk, "email": cremeuser.email, "name": cremeuser.get_full_name()}

    def search_queryset(self, query, users):
        return users.filter(
            Q(email__icontains=query) |
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    def get_message_strings(self):
        return MESSAGE_STRINGS

    def user_is_staff(self, cremeuser):
        # @@@ consider staff users managers of any Team
        return getattr(cremeuser, "is_staff", False)


class HookProxy:

    def __getattr__(self, attr):
        from django.conf import settings
        return getattr(settings.TEAMS_HOOKSET, attr)   #original from TEAMS_HOOKSET


hookset = HookProxy()
