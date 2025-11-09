from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact, NotificationPreference, Reminder, NameDay


@shared_task
def send_daily_name_day_reminders():
    """
    Celery task to send daily name day reminders.
    Runs every morning at 8 AM.
    """
    today = timezone.now()

    # Get all name days for today
    today_name_days = NameDay.objects.filter(month=today.month, day=today.day)

    # Get all contacts celebrating name days today
    contacts = Contact.objects.filter(
        name_day__in=today_name_days,
        user__notification_prefs__enabled=True
    ).select_related('user', 'name_day', 'user__notification_prefs')

    reminders_sent = 0

    for contact in contacts:
        prefs = contact.user.notification_prefs

        # Check if we should send reminder (based on days_before preference)
        if prefs.days_before == 0:  # Send on the day
            send_reminder_notification(contact, prefs.notification_type)
            reminders_sent += 1

    return f"Sent {reminders_sent} reminders"


def send_reminder_notification(contact, notification_type):
    """
    Send a reminder notification for a contact's name day.
    """
    user = contact.user

    if notification_type in ['email', 'both']:
        send_email_reminder(contact)

    if notification_type in ['push', 'both']:
        send_push_reminder(contact)

    # Log the reminder
    Reminder.objects.create(
        contact=contact,
        notification_type=notification_type,
        success=True
    )


def send_email_reminder(contact):
    """Send email reminder"""
    subject = f"Imieniny Reminder: {contact.name}'s Name Day Today!"
    message = f"""
    Hello!

    Today is {contact.name}'s name day ({contact.name_day.name})!

    Don't forget to wish them well.

    Contact details:
    {f"Email: {contact.email}" if contact.email else ""}
    {f"Phone: {contact.phone}" if contact.phone else ""}

    Best regards,
    Imieniny Reminder
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@imieniny.pl',
        [contact.user.email],
        fail_silently=False,
    )


def send_push_reminder(contact):
    """
    Send push notification reminder.
    In production, integrate with FCM or similar service.
    """
    # Placeholder for push notification implementation
    # In production: use Firebase Cloud Messaging, OneSignal, etc.
    pass


@shared_task
def load_polish_name_days():
    """
    Task to load Polish name days into the database.
    Run this once during initial setup.
    """
    # Sample Polish name days data (this would be much larger in production)
    name_days_data = {
        1: {  # January
            1: ['Mieczysława', 'Mieszka'],
            2: ['Bazylego', 'Grzegorza'],
            3: ['Danuty', 'Genowefy'],
            4: ['Anieli', 'Eugeniusza'],
            5: ['Edwarda', 'Emilii'],
            6: ['Kacpra', 'Melchiora', 'Baltazara'],
            # ... more days
        },
        2: {  # February
            1: ['Brygidy', 'Ignacego'],
            2: ['Marii', 'Miłosława'],
            3: ['Błażeja', 'Oskara'],
            # ... more days
        },
        # ... more months
    }

    created_count = 0

    for month, days in name_days_data.items():
        for day, names in days.items():
            for name in names:
                _, created = NameDay.objects.get_or_create(
                    name=name,
                    month=month,
                    day=day
                )
                if created:
                    created_count += 1

    return f"Loaded {created_count} name days"
