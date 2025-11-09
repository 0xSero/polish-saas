from django.contrib import admin
from .models import NameDay, Contact, NotificationPreference, Reminder


@admin.register(NameDay)
class NameDayAdmin(admin.ModelAdmin):
    list_display = ['name', 'day', 'month']
    list_filter = ['month']
    search_fields = ['name']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'name_day', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'user__username']
    raw_id_fields = ['user', 'name_day']


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'days_before', 'enabled']
    list_filter = ['notification_type', 'enabled']
    search_fields = ['user__username']


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['contact', 'sent_at', 'notification_type', 'success']
    list_filter = ['sent_at', 'notification_type', 'success']
    search_fields = ['contact__name']
    date_hierarchy = 'sent_at'
