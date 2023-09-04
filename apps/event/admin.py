from django.contrib import admin
from apps.event.models import EventImage, Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_date')
    list_filter = ('created_date', )
    search_fields = ('user', 'title')
    list_display_links = list_display


admin.site.register(EventImage)
admin.site.register(Event, EventAdmin)
