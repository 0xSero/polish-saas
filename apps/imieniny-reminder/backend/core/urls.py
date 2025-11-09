from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NameDayViewSet, ContactViewSet, NotificationPreferenceViewSet, ReminderViewSet

router = DefaultRouter()
router.register(r'namedays', NameDayViewSet, basename='nameday')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'preferences', NotificationPreferenceViewSet, basename='preference')
router.register(r'reminders', ReminderViewSet, basename='reminder')

urlpatterns = [
    path('', include(router.urls)),
]
