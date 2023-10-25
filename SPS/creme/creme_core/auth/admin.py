from django.contrib import admin

from ..models import (
    CremeUser,
    Account,
    AccountDeletion,
    EmailAddress,
    PasswordExpiry,
    PasswordHistory,
    SignupCode,
)


# Đăng ký admin cho model User
@admin.register(CremeUser)
class UserAdmin(admin.ModelAdmin):
    model = CremeUser
    # Only display the "username" field
    fields = ["username"]

    search_fields = ["user__first_name", "user__last_name", "user__email", "user__username", "gender", "about"]


class SignupCodeAdmin(admin.ModelAdmin):

    list_display = ["code", "max_uses", "use_count", "expiry", "created"]
    search_fields = ["code", "email"]
    list_filter = ["created"]
    raw_id_fields = ["inviter"]


class AccountAdmin(admin.ModelAdmin):

    raw_id_fields = ["user"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


class AccountDeletionAdmin(AccountAdmin):

    list_display = ["email", "date_requested", "date_expunged"]


class EmailAddressAdmin(AccountAdmin):

    list_display = ["user", "email", "verified", "primary"]
    search_fields = ["email", "user__username"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


class PasswordExpiryAdmin(admin.ModelAdmin):

    raw_id_fields = ["user"]


class PasswordHistoryAdmin(admin.ModelAdmin):

    raw_id_fields = ["user"]
    list_display = ["user", "timestamp"]
    list_filter = ["user"]
    ordering = ["user__username", "-timestamp"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


#admin.site.register(User)
#admin.site.unregister(User)  # Hủy đăng ký User mặc định
#admin.site.register(CremeUser, UserAdmin) # Thêm cài đặt admin cho model User vào trang quản trị
#admin.site.register(Group)

admin.site.register(Account, AccountAdmin)
admin.site.register(SignupCode, SignupCodeAdmin)
admin.site.register(AccountDeletion, AccountDeletionAdmin)
admin.site.register(EmailAddress, EmailAddressAdmin)
admin.site.register(PasswordExpiry, PasswordExpiryAdmin)
admin.site.register(PasswordHistory, PasswordHistoryAdmin)
