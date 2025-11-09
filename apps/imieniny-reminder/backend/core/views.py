from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import NameDay, Contact, NotificationPreference, Reminder
from .serializers import (
    NameDaySerializer, ContactSerializer,
    NotificationPreferenceSerializer, ReminderSerializer
)


class NameDayViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Polish name days.
    Provides list and detail views, plus today's name days.
    """
    queryset = NameDay.objects.all()
    serializer_class = NameDaySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's name days"""
        today = timezone.now()
        name_days = NameDay.objects.filter(month=today.month, day=today.day)
        serializer = self.get_serializer(name_days, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming name days for the next 7 days"""
        today = timezone.now()
        upcoming_days = []

        for i in range(7):
            date = today + timezone.timedelta(days=i)
            name_days = NameDay.objects.filter(month=date.month, day=date.day)
            if name_days.exists():
                upcoming_days.append({
                    'date': date.date(),
                    'name_days': NameDaySerializer(name_days, many=True).data
                })

        return Response(upcoming_days)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search name days by name"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter "q" is required'},
                          status=status.HTTP_400_BAD_REQUEST)

        name_days = NameDay.objects.filter(name__icontains=query)
        serializer = self.get_serializer(name_days, many=True)
        return Response(serializer.data)


class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user contacts.
    """
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def upcoming_namedays(self, request):
        """Get contacts with upcoming name days"""
        today = timezone.now()
        contacts_with_upcoming = []

        for i in range(7):
            date = today + timezone.timedelta(days=i)
            contacts = self.get_queryset().filter(
                name_day__month=date.month,
                name_day__day=date.day
            )
            if contacts.exists():
                contacts_with_upcoming.append({
                    'date': date.date(),
                    'days_until': i,
                    'contacts': ContactSerializer(contacts, many=True).data
                })

        return Response(contacts_with_upcoming)


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for notification preferences.
    """
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotificationPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReminderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view sent reminders history.
    """
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(contact__user=self.request.user)
