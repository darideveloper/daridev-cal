from datetime import datetime, time
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import BusinessHours, EventAvailability, AvailabilitySlot, Booking

def validate_booking_time(event, start_time, end_time):
    """
    Validates if a booking's time range is allowed by hierarchical rules:
    1. Event-specific Availability rules.
    2. Global Business Hours fallback.
    """
    weekday = start_time.weekday()
    b_start = start_time.time()
    b_end = end_time.time()

    # 1. Check Event-specific Availability
    availability_rules = EventAvailability.objects.filter(event=event)
    
    if availability_rules.exists():
        # Check for rules that cover the booking date
        date_query = Q(start_date__lte=start_time.date()) | Q(start_date__isnull=True)
        date_query &= Q(end_date__gte=start_time.date()) | Q(end_date__isnull=True)
        
        active_rules = availability_rules.filter(date_query)
        
        if not active_rules.exists():
            raise ValidationError(f"Event is not available on {start_time.date()}.")

        # Check for slots within these active rules
        slots = AvailabilitySlot.objects.filter(
            event_availability__in=active_rules,
            weekday=weekday,
            start_time__lte=b_start,
            end_time__gte=b_end
        )
        
        if not slots.exists():
            raise ValidationError(f"Booking time {b_start}-{b_end} is outside allowed event availability.")
        
        return True

    # 2. Global Business Hours Fallback
    business_hours = BusinessHours.objects.filter(
        weekday=weekday,
        start_time__lte=b_start,
        end_time__gte=b_end
    )
    
    if not business_hours.exists():
        raise ValidationError(f"Booking time {b_start}-{b_end} is outside business hours for {start_time.strftime('%A')}.")

    return True

def create_booking(event, client_name, client_email, start_time, end_time=None):
    """
    Service to create a booking with full validation.
    """
    from datetime import timedelta
    
    if end_time is None:
        end_time = start_time + timedelta(minutes=event.duration_minutes)

    # 1. Overlap Check (if overlap not allowed)
    if not event.event_type.allow_overlap:
        overlapping = Booking.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()
        if overlapping:
            raise ValidationError("This time slot is already booked.")

    # 2. Availability Check
    validate_booking_time(event, start_time, end_time)

    # 3. Create Booking
    booking = Booking(
        event=event,
        client_name=client_name,
        client_email=client_email,
        start_time=start_time,
        end_time=end_time
    )
    booking.full_clean()
    booking.save()
    return booking
