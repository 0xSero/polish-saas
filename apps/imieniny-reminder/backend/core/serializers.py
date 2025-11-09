from rest_framework import serializers
from .models import NameDay, Contact, NotificationPreference, Reminder


class NameDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = NameDay
        fields = ['id', 'name', 'month', 'day']


class ContactSerializer(serializers.ModelSerializer):
    name_day_details = NameDaySerializer(source='name_day', read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone', 'email', 'name_day', 'name_day_details', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ['id', 'notification_type', 'days_before', 'notification_time', 'enabled']


class ReminderSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source='contact.name', read_only=True)

    class Meta:
        model = Reminder
        fields = ['id', 'contact', 'contact_name', 'sent_at', 'notification_type', 'success']
