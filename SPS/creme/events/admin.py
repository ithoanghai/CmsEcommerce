from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Event, EventAdmin)
