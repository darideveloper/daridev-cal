from django.conf import settings
from zoneinfo import ZoneInfo
from django_tenants.test.cases import TenantTestCase
from django_tenants.utils import schema_context
from companies.models import Client, Domain
from django.core.exceptions import ValidationError
from datetime import datetime, time, timedelta
from .models import CompanyProfile, EventType, Event, EventAvailability, AvailabilitySlot, BusinessHours, Booking, EventDateOverride
from .services import create_booking, validate_booking_time

class BookingServiceTest(TenantTestCase):
    def setUp(self):
        super().setUp()
        with schema_context(self.tenant.schema_name):
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
            self.monday = datetime(2026, 4, 6, 10, 0, tzinfo=ZoneInfo(settings.TIME_ZONE)) # A Monday

    def test_business_hours_fallback(self):
        with schema_context(self.tenant.schema_name):
            # Global business hours: Monday 9-17
            BusinessHours.objects.create(company_profile=self.company, weekday=0, start_time=time(9, 0), end_time=time(17, 0))
            
            # Valid booking at 10-11
            booking = create_booking(self.event, "John", "john@ex.com", self.monday)
            self.assertEqual(booking.client_name, "John")
            
            # Invalid booking at 8-9 (outside business hours)
            with self.assertRaises(ValidationError):
                create_booking(self.event, "Late", "late@ex.com", self.monday - timedelta(hours=2))

    def test_event_availability_override(self):
        with schema_context(self.tenant.schema_name):
            # Global business hours: Monday 9-17
            BusinessHours.objects.create(company_profile=self.company, weekday=0, start_time=time(9, 0), end_time=time(17, 0))
            
            # Event availability: Monday only 14-16
            AvailabilitySlot.objects.create(event=self.event, weekday=0, start_time=time(14, 0), end_time=time(16, 0))
            
            # Booking at 10-11 (within business hours but outside event availability)
            with self.assertRaisesRegex(ValidationError, "Booking time is outside the event's regular weekly availability."):
                create_booking(self.event, "Early", "early@ex.com", self.monday)
                
            # Booking at 14:30-15:30 (within event availability)
            booking = create_booking(self.event, "Valid", "valid@ex.com", self.monday + timedelta(hours=4.5))
            self.assertEqual(booking.client_name, "Valid")

    def test_multiple_slots_per_day(self):
        with schema_context(self.tenant.schema_name):
            # Event availability: Morning (9-11) and Afternoon (14-16)
            AvailabilitySlot.objects.create(event=self.event, weekday=0, start_time=time(9, 0), end_time=time(11, 0))
            AvailabilitySlot.objects.create(event=self.event, weekday=0, start_time=time(14, 0), end_time=time(16, 0))
            
            # Booking 10-11 (fits morning slot)
            create_booking(self.event, "Morning", "m@ex.com", self.monday)
            
            # Booking 11-12 (outside slots)
            with self.assertRaisesRegex(ValidationError, "Booking time is outside the event's regular weekly availability."):
                create_booking(self.event, "Gap", "g@ex.com", self.monday + timedelta(hours=1))

    def test_overlap_check(self):
        with schema_context(self.tenant.schema_name):
            BusinessHours.objects.create(company_profile=self.company, weekday=0, start_time=time(9, 0), end_time=time(17, 0))
            
            # Book 10-11
            create_booking(self.event, "First", "first@ex.com", self.monday)
            
            # Book 10:30-11:30 (overlaps)
            with self.assertRaisesRegex(ValidationError, "This time slot is already booked."):
                create_booking(self.event, "Second", "second@ex.com", self.monday + timedelta(minutes=30))

    def test_date_range_intersection(self):
        with schema_context(self.tenant.schema_name):
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
            with self.assertRaisesRegex(ValidationError, "Event is not available on"):
                 create_booking(self.event, "Outside", "out@ex.com", self.monday + timedelta(days=14))

    def test_date_override(self):
        with schema_context(self.tenant.schema_name):
            # Set slots for Mondays 9-17
            AvailabilitySlot.objects.create(event=self.event, weekday=0, start_time=time(9, 0), end_time=time(17, 0))
            
            # Set active range: April 1st to April 15th, 2026
            EventAvailability.objects.create(
                event=self.event, 
                start_date=datetime(2026, 4, 1).date(), 
                end_date=datetime(2026, 4, 15).date()
            )
            
            # 1. Test Blocked Date (within valid range)
            # April 6th is a Monday within range.
            EventDateOverride.objects.create(event=self.event, date=self.monday.date(), is_available=False)
            with self.assertRaisesRegex(ValidationError, "Event is blocked on"):
                create_booking(self.event, "Blocked", "b@ex.com", self.monday)
                
            # 2. Test Allowed Date (outside valid range)
            # April 20th is a Monday OUTSIDE range.
            EventDateOverride.objects.all().delete()
            outside_date = self.monday + timedelta(days=14)
            EventDateOverride.objects.create(event=self.event, date=outside_date.date(), is_available=True)
            booking = create_booking(self.event, "Forced", "f@ex.com", outside_date)
            self.assertEqual(booking.client_name, "Forced")

class RefinedAvailabilityTests(TenantTestCase):
    def setUp(self):
        super().setUp()
        with schema_context(self.tenant.schema_name):
            self.event_type = EventType.objects.create(title="Special Event", allow_overlap=False)
            self.event = Event.objects.create(event_type=self.event_type, title="Workshop", duration_minutes=60)
            self.test_date = datetime(2026, 5, 1, 12, 0, tzinfo=ZoneInfo(settings.TIME_ZONE)) # A Friday

    def test_override_with_custom_hours(self):
        """
        An override with specific times should be the only rule that applies for that day.
        """
        with schema_context(self.tenant.schema_name):
            # Define a date override with custom hours (14:00 to 16:00)
            EventDateOverride.objects.create(
                event=self.event,
                date=self.test_date.date(),
                is_available=True,
                start_time=time(14, 0),
                end_time=time(16, 0)
            )

            # This booking is outside the custom hours, should fail
            with self.assertRaisesRegex(ValidationError, "Booking time is outside the special hours for this date."):
                validate_booking_time(self.event, self.test_date, self.test_date + timedelta(minutes=60))

            # This booking is inside the custom hours, should pass
            valid_time = self.test_date.replace(hour=14, minute=30)
            result = validate_booking_time(self.event, valid_time, valid_time + timedelta(minutes=60))
            self.assertTrue(result)

    def test_blocked_override_rejects_booking(self):
        """
        An override with is_available=False should always reject a booking for that day.
        """
        with schema_context(self.tenant.schema_name):
            EventDateOverride.objects.create(
                event=self.event,
                date=self.test_date.date(),
                is_available=False
            )
            with self.assertRaisesRegex(ValidationError, "Event is blocked on"):
                validate_booking_time(self.event, self.test_date, self.test_date + timedelta(minutes=60))

    def test_booking_clean_calls_service_validation(self):
        """
        Verify that Booking.clean() uses the logic from the validation service.
        """
        with schema_context(self.tenant.schema_name):
            # Block a date using an override
            EventDateOverride.objects.create(
                event=self.event,
                date=self.test_date.date(),
                is_available=False
            )
            
            booking = Booking(
                event=self.event,
                client_name="Test Client",
                client_email="test@test.com",
                start_time=self.test_date
            )

            # Expect a validation error from the service via the model's clean method
            with self.assertRaisesRegex(ValidationError, "Event is blocked on"):
                booking.full_clean()
