import os
import sys
import django
from datetime import datetime, timezone, timedelta

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django_tenants.utils import tenant_context
from companies.models import Client
from scheduler.models import EventType, Booking
from django.core.exceptions import ValidationError

def validate():
    # 1. Get the tenant
    tenant = Client.objects.get(schema_name='company1')
    
    with tenant_context(tenant):
        print(f"Validating overlap logic for tenant: {tenant.name}")
        
        # 2. Create an EventType that DOES NOT allow overlap
        event_type = EventType.objects.create(
            title="Private Lesson",
            duration_minutes=60,
            allow_overlap=False
        )
        
        # 3. Create a first booking
        start_time = datetime(2026, 5, 1, 10, 0, tzinfo=timezone.utc)
        booking1 = Booking(
            event_type=event_type,
            client_name="Client One",
            client_email="one@example.com",
            start_time=start_time
        )
        booking1.full_clean()
        booking1.save()
        print(f"Created booking1: {booking1.start_time} to {booking1.end_time}")
        
        # 4. Try to create an overlapping booking
        # Case A: Exact same time
        booking_overlap = Booking(
            event_type=event_type,
            client_name="Overlap Client",
            client_email="overlap@example.com",
            start_time=start_time
        )
        
        try:
            booking_overlap.full_clean()
            print("FAILED: Overlapping booking was NOT blocked (exact same time)")
        except ValidationError as e:
            print(f"SUCCESS: Overlapping booking blocked as expected: {e}")

        # Case B: Starts during booking1
        booking_overlap_2 = Booking(
            event_type=event_type,
            client_name="Overlap Client 2",
            client_email="overlap2@example.com",
            start_time=start_time + timedelta(minutes=30)
        )
        
        try:
            booking_overlap_2.full_clean()
            print("FAILED: Overlapping booking was NOT blocked (starts during)")
        except ValidationError as e:
            print(f"SUCCESS: Overlapping booking blocked as expected: {e}")

        # 5. Create a non-overlapping booking
        booking_ok = Booking(
            event_type=event_type,
            client_name="OK Client",
            client_email="ok@example.com",
            start_time=booking1.end_time + timedelta(minutes=1)
        )
        
        try:
            booking_ok.full_clean()
            booking_ok.save()
            print(f"SUCCESS: Non-overlapping booking created: {booking_ok.start_time}")
        except ValidationError as e:
            print(f"FAILED: Non-overlapping booking was blocked: {e}")

        # 6. Clean up test data
        Booking.objects.all().delete()
        EventType.objects.all().delete()

if __name__ == "__main__":
    validate()
