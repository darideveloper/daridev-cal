from datetime import datetime, time
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .models import BusinessHours, EventAvailability, AvailabilitySlot, Booking

def validate_booking_time(event, start_time, end_time):
    """
    Matrix-based validation (Option C):
    1. Check if the date falls within ANY of the Event's active ranges (EventAvailability).
    2. Check if the time/weekday matches ANY of the Event's weekly slots (AvailabilitySlot).
    3. Fallback to Global Business Hours ONLY if the event has NO availability rules or slots defined?
       Wait, current logic: if event has ANY rules, use them exclusively. 
       Let's stick to: If event has slots, use them. If not, fallback to BusinessHours.
       And independent of that, if event has date ranges, date must match.
    """
    weekday = start_time.weekday()
    booking_date = start_time.date()
    b_start = start_time.time()
    b_end = end_time.time()

    # 1. Date Range Check (EventAvailability with Overrides)
    override = event.date_overrides.filter(date=booking_date).first()
    is_date_valid = False

    if override:
        if not override.is_available:
            raise ValidationError(_("Event is blocked on %(date)s.") % {'date': booking_date})
        is_date_valid = True
    else:
        availability_rules = event.availability_rules.all()
        if availability_rules.exists():
            for rule in availability_rules:
                in_range = True
                if rule.start_date and booking_date < rule.start_date:
                    in_range = False
                if rule.end_date and booking_date > rule.end_date:
                    in_range = False
                
                if in_range:
                    is_date_valid = True
                    break
        else:
            is_date_valid = True

    if not is_date_valid:
        raise ValidationError(_("Event is not available on %(date)s.") % {'date': booking_date})

    # 2. Weekly Slots Check (AvailabilitySlot)
    event_slots = event.availability_slots.filter(weekday=weekday)
    
    if event_slots.exists():
        is_time_valid = False
        for slot in event_slots:
            if b_start >= slot.start_time and b_end <= slot.end_time:
                is_time_valid = True
                break
        
        if not is_time_valid:
            raise ValidationError(_("Booking time %(start)s-%(end)s is outside allowed event availability.") % {'start': b_start, 'end': b_end})
        
        return True

    # 3. Fallback to Global Business Hours (only if no event-specific slots)
    business_hours = BusinessHours.objects.filter(
        weekday=weekday,
        start_time__lte=b_start,
        end_time__gte=b_end
    )
    
    if not business_hours.exists():
        raise ValidationError(_("Booking time %(start)s-%(end)s is outside business hours for %(day)s.") % {
            'start': b_start, 
            'end': b_end, 
            'day': start_time.strftime('%A')
        })

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
