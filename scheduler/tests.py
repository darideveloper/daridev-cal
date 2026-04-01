from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime, time, timedelta
from .models import CompanyProfile, EventType, Event, EventAvailability, AvailabilitySlot, BusinessHours, Booking
from .services import create_booking, validate_booking_time

class BookingServiceTest(TestCase):
    def setUp(self):
        # 1. Company and Event Setup
        self.company = CompanyProfile.objects.create()
        self.event_type = EventType.objects.create(title="Consultations", allow_overlap=False)
        self.event = Event.objects.create(
            event_type=self.event_type,
            title="General Checkup",
            duration_minutes=60,
            price=100.00
        )
        
        # 2. Weekday definition (Monday, 2026-04-06)
        self.monday = datetime(2026, 4, 6, 10, 0) # A Monday

    def test_business_hours_fallback(self):
        # Global business hours: Monday 9-17
        BusinessHours.objects.create(weekday=0, start_time=time(9, 0), end_time=time(17, 0))
        
        # Valid booking at 10-11
        booking = create_booking(self.event, "John", "john@ex.com", self.monday)
        self.assertEqual(booking.client_name, "John")
        
        # Invalid booking at 8-9 (outside business hours)
        with self.assertRaises(ValidationError):
            create_booking(self.event, "Late", "late@ex.com", self.monday - timedelta(hours=2))

    def test_event_availability_override(self):
        # Global business hours: Monday 9-17
        BusinessHours.objects.create(weekday=0, start_time=time(9, 0), end_time=time(17, 0))
        
        # Event availability: Monday only 14-16
        AvailabilitySlot.objects.create(event=self.event, weekday=0, start_time=time(14, 0), end_time=time(16, 0))
        
        # Booking at 10-11 (within business hours but outside event availability)
        with self.assertRaisesRegex(ValidationError, "outside allowed event availability"):
            create_booking(self.event, "Early", "early@ex.com", self.monday)
            
        # Booking at 14:30-15:30 (within event availability)
        booking = create_booking(self.event, "Valid", "valid@ex.com", self.monday + timedelta(hours=4.5))
        self.assertEqual(booking.client_name, "Valid")

    def test_multiple_slots_per_day(self):
        # Event availability: Morning (9-11) and Afternoon (14-16)
        AvailabilitySlot.objects.create(event=self.event, weekday=0, start_time=time(9, 0), end_time=time(11, 0))
        AvailabilitySlot.objects.create(event=self.event, weekday=0, start_time=time(14, 0), end_time=time(16, 0))
        
        # Booking 10-11 (fits morning slot)
        create_booking(self.event, "Morning", "m@ex.com", self.monday)
        
        # Booking 11-12 (outside slots)
        with self.assertRaises(ValidationError):
            create_booking(self.event, "Gap", "g@ex.com", self.monday + timedelta(hours=1))

    def test_overlap_check(self):
        BusinessHours.objects.create(weekday=0, start_time=time(9, 0), end_time=time(17, 0))
        
        # Book 10-11
        create_booking(self.event, "First", "first@ex.com", self.monday)
        
        # Book 10:30-11:30 (overlaps)
        with self.assertRaisesRegex(ValidationError, "time slot is already booked"):
            create_booking(self.event, "Second", "second@ex.com", self.monday + timedelta(minutes=30))

    def test_date_range_intersection(self):
        # Set slots for Mondays 9-17
        AvailabilitySlot.objects.create(event=self.event, weekday=0, start_time=time(9, 0), end_time=time(17, 0))
        
        # Set active range: April 1st to April 15th, 2026
        EventAvailability.objects.create(
            event=self.event, 
            start_date=datetime(2026, 4, 1).date(), 
            end_date=datetime(2026, 4, 15).date()
        )
        
        # Valid: Monday April 6th (within range)
        create_booking(self.event, "Inside", "in@ex.com", self.monday)
        
        # Invalid: Monday April 20th (outside range)
        with self.assertRaisesRegex(ValidationError, "outside the event's availability ranges"):
             create_booking(self.event, "Outside", "out@ex.com", self.monday + timedelta(days=14))
