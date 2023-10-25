from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from reversion.admin import VersionAdmin

from ..persons.hooks import hookset
from ..persons.models import Membership, Team, Profile, Contact


admin.site.register(
    Team,
    list_display=["name", "member_access", "manager_access", "members_count", "creator"],
    fields=[
        "name",
        "slug",
        "avatar",
        "description",
        "member_access",
        "manager_access",
        "creator"
    ],
    prepopulated_fields={"slug": ("name",)},
    raw_id_fields=["creator"]
)


class MembershipAdmin(VersionAdmin):
    raw_id_fields = ["user"]
    list_display = ["user", "state", "role"]
    list_filter = ["state", "role"]
    #search_fields = ["user__username"]
    #search_fields = hookset.membership_search_fields


#admin.site.register(CremeUser)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Profile)
admin.site.register(Contact)
