from django.contrib import admin

from .models import (
    MessageTooLong,
    PhoneCountryCode,
    PhoneNumber,
    PhoneConfirmation,
    SMSLog
)


class SMSLogAdmin(admin.ModelAdmin):
    list_display = ["number", "destination", "message", "mocked", "created_at", "response_code"]
    list_filter = ["mocked", "created_at", "response_code"]
    search_fields = ["number"]

    def destination(self, obj):
        if obj.payload:
            return obj.payload.get("destination", "")
        return ""

    def message(self, obj):
        if obj.payload:
            return obj.payload.get("body", "")
        return ""


class MessageTooLongAdmin(admin.ModelAdmin):

    list_display = ["notice_type", "created_at", "length"]
    search_fields = ["message"]
    list_filter = ["notice_type", "created_at"]

    def length(self, obj):
        return len(obj.message)


admin.site.register(PhoneCountryCode)
admin.site.register(PhoneNumber)
admin.site.register(PhoneConfirmation)
admin.site.register(SMSLog, SMSLogAdmin)
admin.site.register(MessageTooLong, MessageTooLongAdmin)
