from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import InvitationStat, JoinInvitation
from ..creme_core.models import Account, CremeUser

CremeUser = get_user_model()


class InvitationStatAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]
    readonly_fields = ["invites_sent", "invites_accepted"]
    list_display = [
        "user",
        "invites_sent",
        "invites_accepted",
        "invites_allocated",
        "invites_remaining",
        "can_send"
    ]
    list_filter = ["invites_sent", "invites_accepted"]


@admin.register(JoinInvitation)
class JoinInvitationAdmin(admin.ModelAdmin):
    list_display = ["from_user", "to_user", "sent", "status", "to_user_email"]
    list_filter = ["sent", "status"]
    search_fields = [f"from_user__{CremeUser.USERNAME_FIELD}"]


@admin.register(InvitationStat)
class InvitationStatAdmin(admin.ModelAdmin):
    pass  # Bổ sung các trường và cấu hình admin tại đây nếu cần

# admin.site.register(
#     JoinInvitation,
#     list_display=["from_user", "to_user", "sent", "status", "to_user_email"],
#     list_filter=["sent", "status"],
#     search_fields=[f"from_user__{Account.USERNAME_FIELD}"]
# )
# admin.site.register(InvitationStat, InvitationStatAdmin)
