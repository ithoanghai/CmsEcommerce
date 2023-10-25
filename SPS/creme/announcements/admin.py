from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Announcement, Dismissal
from ..creme_core.models.admin import LogicalDeleteModelAdmin


class AnnouncementAdmin(LogicalDeleteModelAdmin): #Tạo và/hoặc Đăng ký quản trị viên cho từng mô hình này bằng cách sử dụng LogicalDeleteModelAdmin
    list_display = ("title", "creator", "creation_date", "members_only")
    list_filter = ("members_only",)
    fieldsets = [
        (None, {
            "fields": [
                "title", "content", "site_wide", "members_only", "publish_start", "publish_end",
                "dismissal_type"],
        }),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            # When creating a new announcement, set the creator field.
            obj.creator = request.user
        obj.save()


class DismissalAdmin(admin.ModelAdmin):
    list_display = ("user", "announcement", "dismissed_at")

    def get_search_fields(self, request):
        CremeUser = get_user_model()
        if hasattr(CremeUser, "USERNAME_FIELD"):
            username_search = f"user__{CremeUser.USERNAME_FIELD}"
        else:
            username_search = "user__username"
        return (username_search, "announcement__title")


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Dismissal, DismissalAdmin)
