from django.db import models
from django.contrib.auth.models import User


class NameDay(models.Model):
    """Polish name days database"""
    name = models.CharField(max_length=100, db_index=True)
    month = models.IntegerField()
    day = models.IntegerField()

    class Meta:
        ordering = ['month', 'day']
        unique_together = ['name', 'month', 'day']
        indexes = [
            models.Index(fields=['month', 'day']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} - {self.day}/{self.month}"


class Contact(models.Model):
    """User's contacts with their name days"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    name_day = models.ForeignKey(NameDay, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class NotificationPreference(models.Model):
    """User notification preferences"""
    NOTIFICATION_TYPES = [
        ('email', 'Email'),
        ('push', 'Push Notification'),
        ('both', 'Both'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_prefs')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES, default='email')
    days_before = models.IntegerField(default=0)  # 0 = on the day
    notification_time = models.TimeField(default='08:00:00')
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.notification_type}"


class Reminder(models.Model):
    """Sent reminders log"""
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=10)
    success = models.BooleanField(default=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"Reminder for {self.contact.name} sent at {self.sent_at}"
