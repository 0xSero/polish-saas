"""
Celery tasks for background jobs
Run with: celery -A tasks worker -l info
"""
from celery import Celery
from celery.schedules import crontab
from config import settings
from database import SessionLocal
from models import City, Alert, AirQualityData, Notification, User
from api.air_quality import fetch_air_quality_from_gios
import asyncio

celery_app = Celery('airaware', broker=settings.redis_url, backend=settings.redis_url)

celery_app.conf.beat_schedule = {
    'update-air-quality-data': {
        'task': 'tasks.update_air_quality_data',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    'check-and-send-alerts': {
        'task': 'tasks.check_and_send_alerts',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
}


@celery_app.task
def update_air_quality_data():
    """Update air quality data for all cities"""
    db = SessionLocal()
    try:
        cities = db.query(City).all()
        updated = 0

        for city in cities:
            try:
                # Fetch new data
                loop = asyncio.get_event_loop()
                loop.run_until_complete(fetch_air_quality_from_gios(city, db))
                updated += 1
            except Exception as e:
                print(f"Error updating {city.name}: {e}")

        return f"Updated air quality data for {updated} cities"

    finally:
        db.close()


@celery_app.task
def check_and_send_alerts():
    """Check air quality and send alerts if thresholds exceeded"""
    db = SessionLocal()
    try:
        alerts = db.query(Alert).filter(Alert.is_active == True).all()
        notifications_sent = 0

        for alert in alerts:
            # Get latest air quality data
            latest_data = (
                db.query(AirQualityData)
                .filter(AirQualityData.city_id == alert.city_id)
                .order_by(AirQualityData.timestamp.desc())
                .first()
            )

            if latest_data and latest_data.aqi and latest_data.aqi > alert.threshold_aqi:
                # Send notification
                if alert.notify_email:
                    send_email_alert(alert, latest_data)

                if alert.notify_push:
                    send_push_alert(alert, latest_data)

                # Log notification
                notification = Notification(
                    user_id=alert.user_id,
                    alert_id=alert.id,
                    message=f"Air quality alert: AQI {latest_data.aqi} exceeds threshold {alert.threshold_aqi}",
                    notification_type="email" if alert.notify_email else "push"
                )
                db.add(notification)
                notifications_sent += 1

        db.commit()
        return f"Sent {notifications_sent} notifications"

    finally:
        db.close()


def send_email_alert(alert: Alert, data: AirQualityData):
    """Send email alert (implement with your email service)"""
    # Placeholder for email implementation
    print(f"Sending email alert to user {alert.user_id}")


def send_push_alert(alert: Alert, data: AirQualityData):
    """Send push notification (implement with FCM or similar)"""
    # Placeholder for push notification implementation
    print(f"Sending push notification to user {alert.user_id}")
