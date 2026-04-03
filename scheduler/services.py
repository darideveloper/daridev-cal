import calendar
from datetime import datetime, time, date, timedelta
import pytz
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from project import settings
from .models import BusinessHours, EventAvailability, AvailabilitySlot, Booking

def get_available_ranges(event, date_obj):
    """
    Returns a list of (start_time, end_time) that represent available ranges 
    for a given event and date, respecting the priority matrix.
    """
    weekday = date_obj.weekday()
    
    # 1. Event Level Checks
    # 1.1 Event Date Override (Highest priority)
    event_override = event.date_overrides.filter(date=date_obj).first()
    if event_override:
        if not event_override.is_available:
            return []
        if event_override.start_time and event_override.end_time:
            return [(event_override.start_time, event_override.end_time)]

    # 1.2 Event Weekly Slots
    event_slots = event.availability_slots.filter(weekday=weekday)
    if event_slots.exists():
        # Check Event Ranges (validity period)
        event_ranges = event.availability_rules.all()
        if event_ranges.exists():
            is_in_range = any(
                (not r.start_date or date_obj >= r.start_date) and
                (not r.end_date or date_obj <= r.end_date)
                for r in event_ranges
            )
            if not is_in_range:
                return []
        return [(slot.start_time, slot.end_time) for slot in event_slots]

    # 1.3 Event Ranges (if no slots, is the date active?)
    event_ranges = event.availability_rules.all()
    if event_ranges.exists():
        is_in_range = any(
            (not r.start_date or date_obj >= r.start_date) and
            (not r.end_date or date_obj <= r.end_date)
            for r in event_ranges
        )
        if not is_in_range:
            return []

    # 2. Company Level Fallback
    from .models import CompanyProfile
    try:
        company = CompanyProfile.objects.get()
    except CompanyProfile.DoesNotExist:
        return []

    # 2.1 Company Date Override
    company_override = company.date_overrides.filter(date=date_obj).first()
    if company_override:
        if not company_override.is_available:
            return []
        if company_override.start_time and company_override.end_time:
            return [(company_override.start_time, company_override.end_time)]

    # 2.2 Company Weekly Slots
    company_slots = company.weekday_slots.filter(weekday=weekday)
    if not company_slots.exists():
        company_slots = company.business_hours.filter(weekday=weekday)

    if company_slots.exists():
        # Company ranges
        company_ranges = company.availability_rules.all()
        if company_ranges.exists():
            is_in_range = any(
                (not r.start_date or date_obj >= r.start_date) and
                (not r.end_date or date_obj <= r.end_date)
                for r in company_ranges
            )
            if not is_in_range:
                return []
        return [(slot.start_time, slot.end_time) for slot in company_slots]

    return []

def get_available_slots(event, date_obj):
    """
    Returns a list of ISO 8601 strings representing available start times for a given date.
    """
    ranges = get_available_ranges(event, date_obj)
    if not ranges:
        return []
    
    tz = pytz.timezone(settings.TIME_ZONE)
    potential_slots = []
    duration = timedelta(minutes=event.duration_minutes)
    
    for start_t, end_t in ranges:
        curr_dt = tz.localize(datetime.combine(date_obj, start_t))
        end_dt = tz.localize(datetime.combine(date_obj, end_t))
        
        while curr_dt + duration <= end_dt:
            potential_slots.append((curr_dt, curr_dt + duration))
            curr_dt += duration

    if not potential_slots:
        return []

    if event.event_type.allow_overlap:
        return [s[0].isoformat() for s in potential_slots]

    # Filter out busy ones
    confirmed_bookings = Booking.objects.filter(
        event=event,
        start_time__date=date_obj,
        status__in=["CONFIRMED", "PAID"]
    )
    
    available_slots = []
    for s_start, s_end in potential_slots:
        is_busy = False
        for booking in confirmed_bookings:
            if s_start < booking.end_time and s_end > booking.start_time:
                is_busy = True
                break
        if not is_busy:
            available_slots.append(s_start.isoformat())
            
    return available_slots

def get_monthly_availability(event, year, month):
    """
    Returns a dict mapping ISO date strings to boolean availability.
    """
    num_days = calendar.monthrange(year, month)[1]
    availability = {}
    
    for day in range(1, num_days + 1):
        d = date(year, month, day)
        slots = get_available_slots(event, d)
        availability[d.isoformat()] = len(slots) > 0
        
    return availability

def validate_booking_time(event, start_time, end_time):
    """
    Validates if a specific time range is available for a booking.
    """
    booking_date = start_time.date()
    b_start = start_time.time()
    b_end = end_time.time()

    ranges = get_available_ranges(event, booking_date)
    
    if not ranges:
        # Check if it was blocked by a specific override to give better error message
        event_override = event.date_overrides.filter(date=booking_date).first()
        if event_override and not event_override.is_available:
             raise ValidationError(_("Event is specifically blocked on %(date)s.") % {'date': booking_date})
        
        from .models import CompanyProfile
        try:
            company = CompanyProfile.objects.get()
            company_override = company.date_overrides.filter(date=booking_date).first()
            if company_override and not company_override.is_available:
                raise ValidationError(_("Provider is closed on %(date)s.") % {'date': booking_date})
        except CompanyProfile.DoesNotExist:
            pass
            
        raise ValidationError(_("No operating hours are configured for this provider on %(date)s.") % {'date': booking_date})

    is_time_valid = any(
        b_start >= start_t and b_end <= end_t
        for start_t, end_t in ranges
    )
    
    if not is_time_valid:
        raise ValidationError(_("Booking time is outside the available hours for this service today."))
    
    return True

def create_booking(event, client_name, client_email, start_time, end_time=None, client_phone=None):
    """
    Service to create a booking with full validation.
    """
    if end_time is None:
        end_time = start_time + timedelta(minutes=event.duration_minutes)

    # 1. Availability Check
    validate_booking_time(event, start_time, end_time)

    # 2. Overlap Check
    if not event.event_type.allow_overlap:
        overlapping = Booking.objects.filter(
            event=event,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exclude(status="CANCELLED").exists()
        
        if overlapping:
            raise ValidationError(_("This time slot is already booked."))

    # 3. Create Booking
    booking = Booking(
        event=event,
        client_name=client_name,
        client_email=client_email,
        client_phone=client_phone,
        start_time=start_time,
        end_time=end_time
    )
    booking.full_clean()
    booking.save()
    return booking
