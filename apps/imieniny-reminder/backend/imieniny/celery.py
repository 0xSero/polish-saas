import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imieniny.settings')

app = Celery('imieniny')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'core.tasks.send_daily_name_day_reminders',
        'schedule': crontab(hour=8, minute=0),  # Every day at 8 AM
    },
}
