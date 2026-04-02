from datetime import datetime, time
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .models import BusinessHours, EventAvailability, AvailabilitySlot, Booking

def validate_booking_time(event, start_time, end_time):
    """
    Hierarchical Matrix-based validation (Priority Matrix):
    1. Event.DateOverride (Highest Priority)
    2. Event.WeeklySlot
    3. Event.DateRange
    4. Company.DateOverride
    5. Company.WeeklySlot
    6. Company.DateRange (Lowest Priority)
    """
    weekday = start_time.weekday()
    booking_date = start_time.date()
    b_start = start_time.time()
    b_end = end_time.time()

    # --- 1. Event Level Checks ---

    # 1.1 Event Date Override
    event_override = event.date_overrides.filter(date=booking_date).first()
    if event_override:
        if not event_override.is_available:
            raise ValidationError(_("Event is specifically blocked on %(date)s.") % {'date': booking_date})
        
        # If override has custom hours, they take absolute priority for this date.
        if event_override.start_time and event_override.end_time:
            if b_start >= event_override.start_time and b_end <= event_override.end_time:
                return True
            raise ValidationError(_("Booking time is outside the custom hours for this event today."))

    # 1.2 Event Weekly Slots
    # If ANY slot exists for this event, we ignore global business hours for this entity.
    event_slots = event.availability_slots.filter(weekday=weekday)
    if event_slots.exists():
        is_time_valid = any(
            b_start >= slot.start_time and b_end <= slot.end_time
            for slot in event_slots
        )
        if not is_time_valid:
            raise ValidationError(_("Booking time is outside the event's regular weekly availability."))
        
        # Now check if this valid slot is within a valid date range (if rules exist)
        event_ranges = event.availability_rules.all()
        if event_ranges.exists():
            is_in_range = any(
                (not r.start_date or booking_date >= r.start_date) and
                (not r.end_date or booking_date <= r.end_date)
                for r in event_ranges
            )
            if not is_in_range:
                raise ValidationError(_("Event is not valid for bookings on %(date)s.") % {'date': booking_date})
        return True

    # 1.3 Event Ranges (if no slots defined, just check if the date is valid)
    event_ranges = event.availability_rules.all()
    if event_ranges.exists():
        is_in_range = any(
            (not r.start_date or booking_date >= r.start_date) and
            (not r.end_date or booking_date <= r.end_date)
            for r in event_ranges
        )
        if not is_in_range:
            raise ValidationError(_("Event is not active on %(date)s.") % {'date': booking_date})

    # --- 2. Company Level Checks (Fallback) ---

    try:
        from .models import CompanyProfile
        company = CompanyProfile.objects.get()
    except CompanyProfile.DoesNotExist:
        raise ValidationError(_("Provider configuration is missing."))

    # 2.1 Company Date Override (Holidays, etc.)
    company_override = company.date_overrides.filter(date=booking_date).first()
    if company_override:
        if not company_override.is_available:
            raise ValidationError(_("Provider is closed on %(date)s.") % {'date': booking_date})
        
        if company_override.start_time and company_override.end_time:
            if b_start >= company_override.start_time and b_end <= company_override.end_time:
                return True
            raise ValidationError(_("Booking time is outside the provider's special hours for today."))

    # 2.2 Company Weekly Slots (Standard Business Hours)
    # Using the new CompanyWeekdaySlot as primary, keeping BusinessHours as second fallback for now.
    company_slots = company.weekday_slots.filter(weekday=weekday)
    if not company_slots.exists():
        # Temporary fallback to Legacy BusinessHours for data continuity
        company_slots = company.business_hours.filter(weekday=weekday)

    if company_slots.exists():
        is_time_valid = any(
            b_start >= slot.start_time and b_end <= slot.end_time
            for slot in company_slots
        )
        if not is_time_valid:
            raise ValidationError(_("Booking time is outside of standard business hours."))
        
        # Finally, check Company overall validity range
        company_ranges = company.availability_rules.all()
        if company_ranges.exists():
            is_in_range = any(
                (not r.start_date or booking_date >= r.start_date) and
                (not r.end_date or booking_date <= r.end_date)
                for r in company_ranges
            )
            if not is_in_range:
                raise ValidationError(_("Provider is not accepting bookings on %(date)s.") % {'date': booking_date})
        return True

    raise ValidationError(_("No operating hours are configured for this provider."))


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
