from datetime import datetime, time
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .models import BusinessHours, EventAvailability, AvailabilitySlot, Booking

def validate_booking_time(event, start_time, end_time):
    """
    Matrix-based validation:
    1. Check EventDateOverride for specific date blocking or custom hours.
    2. Check EventAvailability date ranges if no override or override has no custom hours.
    3. Check Event-specific AvailabilitySlot if no override with custom hours.
    4. Fallback to Global Business Hours if no event-specific slots and no override with custom hours.
    """
    weekday = start_time.weekday()
    booking_date = start_time.date()
    b_start = start_time.time()
    b_end = end_time.time()

    # 1. Check EventDateOverride
    override = event.date_overrides.filter(date=booking_date).first()

    if override:
        if not override.is_available:
            raise ValidationError(_("Event is blocked on %(date)s.") % {'date': booking_date})
        
        # If override has custom hours, this is the only rule that applies.
        if override.start_time and override.end_time:
            if b_start >= override.start_time and b_end <= override.end_time:
                return True  # Valid within override hours
            else:
                raise ValidationError(_("Booking time is outside the special hours for this date."))

    # 2. Date Range Check (EventAvailability)
    # Ignored if an override exists, otherwise check if date is valid.
    if not override:
        availability_rules = event.availability_rules.all()
        if availability_rules.exists():
            is_date_in_range = any(
                (not r.start_date or booking_date >= r.start_date) and
                (not r.end_date or booking_date <= r.end_date)
                for r in availability_rules
            )
            if not is_date_in_range:
                raise ValidationError(_("Event is not available on %(date)s.") % {'date': booking_date})

    # 3. Weekly Slots Check (AvailabilitySlot)
    # These have priority over global BusinessHours.
    event_slots = event.availability_slots.filter(weekday=weekday)
    if event_slots.exists():
        is_time_valid = any(
            b_start >= slot.start_time and b_end <= slot.end_time
            for slot in event_slots
        )
        if not is_time_valid:
            raise ValidationError(_("Booking time is outside the event's regular weekly availability."))
        return True

    # 4. Fallback to Global Business Hours
    try:
        # Since we are in a tenant schema, there should be only one CompanyProfile.
        from .models import CompanyProfile
        company_profile = CompanyProfile.objects.get()
    except CompanyProfile.DoesNotExist:
        # If no profile, then no business hours exist.
        raise ValidationError(_("No business hours are configured for this provider."))

    business_hours_exist = BusinessHours.objects.filter(
        company_profile=company_profile,
        weekday=weekday,
        start_time__lte=b_start,
        end_time__gte=b_end
    ).exists()
    
    if not business_hours_exist:
        raise ValidationError(_("Booking time is outside of business hours."))

    return True

def create_booking(event, client_name, client_email, start_time, end_time=None):
    """
    Service to create a booking with full validation.
    """
    from datetime import timedelta
    
    if end_time is None:
        end_time = start_time + timedelta(minutes=event.duration_minutes)

    # 1. Availability Check (Hierarchical/Matrix logic)
    validate_booking_time(event, start_time, end_time)

    # 2. Overlap Check (if overlap not allowed)
    if not event.event_type.allow_overlap:
        overlapping = Booking.objects.filter(
            event=event,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exclude(status="CANCELLED").exists() # Assuming status check might be needed later
        
        if overlapping:
            raise ValidationError(_("This time slot is already booked."))

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
