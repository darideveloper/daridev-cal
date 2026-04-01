from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import datetime, time, timedelta
from scheduler.models import Event, EventType, BusinessHours, Booking

class BookingAPITest(APITestCase):
    def setUp(self):
        self.et = EventType.objects.create(title="API Test Group", allow_overlap=False)
        self.event = Event.objects.create(
            event_type=self.et,
            title="API Event",
            duration_minutes=30,
            price=50.00
        )
        # Monday 9-17
        BusinessHours.objects.create(weekday=0, start_time=time(9, 0), end_time=time(17, 0))
        self.valid_start = datetime(2026, 4, 6, 12, 0) # A Monday at 12:00

    def test_create_booking_api(self):
        url = reverse("booking-list")
        data = {
            "event": self.event.id,
            "client_name": "API Client",
            "client_email": "api@test.com",
            "start_time": self.valid_start.isoformat()
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().client_name, "API Client")

    def test_create_invalid_booking_api(self):
        url = reverse("booking-list")
        # Sunday (outside business hours)
        sunday = datetime(2026, 4, 5, 12, 0)
        data = {
            "event": self.event.id,
            "client_name": "Invalid",
            "client_email": "inv@test.com",
            "start_time": sunday.isoformat()
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("outside business hours", response.data["detail"])
