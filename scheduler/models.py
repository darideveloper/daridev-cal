from datetime import timedelta
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django_cryptography.fields import encrypt

class CompanyProfile(models.Model):
    """Tenant-specific configuration."""
    brand_color = models.CharField(
        _("brand color"),
        max_length=50,
        default="oklch(0.81 0.11 236)",
        validators=[
            RegexValidator(
                regex=r"^(#[0-9a-fA-F]{3}|#[0-9a-fA-F]{6}|oklch\([\d.]+\s[\d.]+\s[\d.]+\))$",
                message=_("Enter a valid HEX code or OKLCH function (e.g. #87d1ff or oklch(0.81 0.11 236))"),
            )
        ],
    )
    stripe_public_key = models.CharField(_("Stripe public key"), max_length=255, null=True, blank=True)
    stripe_secret_key = encrypt(models.CharField(_("Stripe secret key"), max_length=255, blank=True, null=True))
    google_calendar_id = models.CharField(_("Google Calendar ID"), max_length=255, blank=True, null=True)
    logo = models.ImageField(_("logo"), upload_to="logos/", blank=True, null=True)

    currency = models.CharField(
        _("currency"), 
        max_length=10, 
        choices=[("MXN", _("MXN")), ("USD", _("USD")), ("EUR", _("EUR"))],
        default="USD",
        help_text=_("The brand's operating currency.")
    )

    class Meta:
        verbose_name = _("Company Profile")
        verbose_name_plural = _("Company Profiles")

    def __str__(self):
        return str(_("Company Profile"))

class BusinessHours(models.Model):
    """Normalized storage for default weekly operating hours."""
    company_profile = models.ForeignKey(
        CompanyProfile, 
        on_delete=models.CASCADE, 
        related_name="business_hours", 
        verbose_name=_("company profile"),
        null=True, # For migration safety with existing data
        blank=True
    )
    weekday = models.IntegerField(_("weekday"), choices=[
        (0, _("Monday")), (1, _("Tuesday")), (2, _("Wednesday")),
        (3, _("Thursday")), (4, _("Friday")), (5, _("Saturday")), (6, _("Sunday"))
    ])
    start_time = models.TimeField(_("start time"))
    end_time = models.TimeField(_("end time"))

    class Meta:
        verbose_name = _("Business Hour")
        verbose_name_plural = _("Business Hours")
        ordering = ["weekday", "start_time"]

    def __str__(self):
        return f"{self.get_weekday_display()}: {self.start_time} - {self.end_time}"

class EventType(models.Model):
    """Service categories for grouping events."""
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"), blank=True, null=True)
    payment_model = models.CharField(
        _("payment model"),
        max_length=10, 
        choices=[("PRE-PAID", _("Pre-payment")), ("POST-PAID", _("Post-payment"))], 
        default="POST-PAID"
    )
    allow_overlap = models.BooleanField(_("allow overlap"), default=False)

    class Meta:
        verbose_name = _("Event Type")
        verbose_name_plural = _("Event Types")

    def __str__(self):
        return self.title

class Event(models.Model):
    """A specific bookable service."""
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name="events", verbose_name=_("event type"))
    title = models.CharField(_("title"), max_length=100)
    image = models.ImageField(_("image"), upload_to="events/", blank=True, null=True)
    description = models.CharField(_("description"), max_length=255, blank=True, null=True)
    detailed_description = models.TextField(_("detailed description"), blank=True, null=True)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(_("duration (minutes)"), default=30)
    currency = models.CharField(
        _("currency"), 
        max_length=10, 
        choices=[("MXN", _("MXN")), ("USD", _("USD")), ("EUR", _("EUR"))],
        default="USD"
    )

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return f"{self.event_type.title}: {self.title}"

class EventAvailability(models.Model):
    """Date-based availability rules (ranges) for a specific event."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="availability_rules", verbose_name=_("event"))
    start_date = models.DateField(_("start date"), null=True, blank=True, help_text=_("Start of the rule's validity."))
    end_date = models.DateField(_("end date"), null=True, blank=True, help_text=_("End of the rule's validity."))

    class Meta:
        verbose_name = _("Date Range")
        verbose_name_plural = _("Date Ranges")

    def __str__(self):
        return f"{_('Availability for')} {self.event.title}"

class AvailabilitySlot(models.Model):
    """Specific weekly time windows for an Event."""
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        related_name="availability_slots", 
        verbose_name=_("event")
    )
    weekday = models.IntegerField(_("weekday"), choices=[
        (0, _("Monday")), (1, _("Tuesday")), (2, _("Wednesday")),
        (3, _("Thursday")), (4, _("Friday")), (5, _("Saturday")), (6, _("Sunday"))
    ])
    start_time = models.TimeField(_("start time"))
    end_time = models.TimeField(_("end time"))

    class Meta:
        verbose_name = _("Week Day")
        verbose_name_plural = _("Week Days")
        ordering = ["weekday", "start_time"]

    def __str__(self):
        return f"{self.get_weekday_display()}: {self.start_time} - {self.end_time}"

class Booking(models.Model):
    """Individual appointments linked to specific events."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings", null=True, blank=True, verbose_name=_("event"))
    client_name = models.CharField(_("client name"), max_length=255)
    client_email = models.EmailField(_("client email"))
    start_time = models.DateTimeField(_("start time"))
    end_time = models.DateTimeField(_("end time"), null=True, blank=True)
    status = models.CharField(
        _("status"),
        max_length=20, 
        choices=[("PENDING", _("Pending")), ("CONFIRMED", _("Confirmed")), ("PAID", _("Paid"))], 
        default="PENDING"
    )

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")

    def __str__(self):
        return f"{self.client_name} - {self.event.title}"

    def save(self, *args, **kwargs):
        # Auto-calculate end_time from start_time + event duration
        if self.start_time and self.event:
            self.end_time = self.start_time + timedelta(minutes=self.event.duration_minutes)
        super().save(*args, **kwargs)

    def clean(self):
        """
        Matrix-based validation:
        1. Date must fall within an EventAvailability range (if any exist).
        2. Time/Weekday must match an AvailabilitySlot record.
        3. Check for overlapping bookings (unless event type allows it).
        """
        if not self.start_time or not self.event:
            super().clean()
            return

        self.end_time = self.start_time + timedelta(minutes=self.event.duration_minutes)
        booking_date = self.start_time.date()
        booking_weekday = self.start_time.weekday()
        booking_start_time = self.start_time.time()
        booking_end_time = self.end_time.time()

        # 1. Date Validity (Intersection Rule)
        date_ranges = self.event.availability_rules.all()
        if date_ranges.exists():
            is_date_valid = False
            for rule in date_ranges:
                in_range = True
                if rule.start_date and booking_date < rule.start_date:
                    in_range = False
                if rule.end_date and booking_date > rule.end_date:
                    in_range = False
                
                if in_range:
                    is_date_valid = True
                    break
            
            if not is_date_valid:
                raise ValidationError(_("This date is outside the event's availability ranges."))

        # 2. Time Validity (Weekly Slots)
        slots = self.event.availability_slots.filter(weekday=booking_weekday)
        if not slots.exists():
            raise ValidationError(_("No availability slots defined for this weekday."))
        
        is_time_valid = False
        for slot in slots:
            # Check if booking fits within slot
            if booking_start_time >= slot.start_time and booking_end_time <= slot.end_time:
                is_time_valid = True
                break
        
        if not is_time_valid:
            raise ValidationError(_("The requested time is outside the defined availability slots for this day."))

        # 3. Overlap Check
        if not self.event.event_type.allow_overlap:
            overlapping_bookings = Booking.objects.filter(
                event=self.event,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(pk=self.pk) if self.pk else Booking.objects.filter(
                event=self.event,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )
                
            if overlapping_bookings.exists():
                raise ValidationError(_("This booking overlaps with an existing appointment."))
        
        super().clean()
