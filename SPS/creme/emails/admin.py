from django.contrib import admin

from ..creme_core.core.loading import get_model


Email = get_model('emails', 'Email')


class EmailAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'sending_date', 'subject')


# Register your models here.
admin.site.register(Email, EmailAdmin)
