from datetime import timedelta
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django_cryptography.fields import encrypt

class BaseAvailabilityRange(models.Model):
    """Abstract base for date-based availability ranges."""
    start_date = models.DateField(
        _("start date"), 
        null=True, 
        blank=True, 
        help_text=_("Defines the beginning of the validity period.")
    )
    end_date = models.DateField(
        _("end date"), 
        null=True, 
        blank=True, 
        help_text=_("Defines the end of the validity period.")
    )

    class Meta:
        abstract = True

class BaseAvailabilitySlot(models.Model):
    """Abstract base for weekly recurring time windows."""
    weekday = models.IntegerField(_("weekday"), choices=[
        (0, _("Monday")), (1, _("Tuesday")), (2, _("Wednesday")),
        (3, _("Thursday")), (4, _("Friday")), (5, _("Saturday")), (6, _("Sunday"))
    ])
    start_time = models.TimeField(_("start time"))
    end_time = models.TimeField(_("end time"))

    class Meta:
        abstract = True
        ordering = ["weekday", "start_time"]

class BaseDateOverride(models.Model):
    """Abstract base for specific date exceptions."""
    date = models.DateField(_("Date"))
    is_available = models.BooleanField(
        _("Is available"), 
        default=False, 
        help_text=_("Individual date exception. Highest priority override. If start/end times are set, they override weekly slots.")
    )
    start_time = models.TimeField(_("start time"), null=True, blank=True)
    end_time = models.TimeField(_("end time"), null=True, blank=True)

    class Meta:
        abstract = True

class CompanyProfile(models.Model):
    """Tenant-specific configuration."""
    brand_color = models.CharField(
        _("brand primary color"),
        max_length=50,
        default="oklch(0.81 0.11 236)",
        validators=[
            RegexValidator(
                regex=r"^(#[0-9a-fA-F]{3}|#[0-9a-fA-F]{6}|oklch\([\d.]+\s[\d.]+\s[\d.]+\))$",
                message=_("Enter a valid HEX code or OKLCH function (e.g. #87d1ff or oklch(0.81 0.11 236))"),
            )
        ],
        help_text=_("The main color for the booking page. Supports HEX and OKLCH format (e.g., oklch(0.8 0.1 240)).")
    )
    stripe_public_key = models.CharField(
        _("Stripe public key"), 
        max_length=255, 
        null=True, 
        blank=True,
        help_text=_("Your Stripe Publishable Key found in the Developer Dashboard.")
    )
    stripe_secret_key = encrypt(models.CharField(
        _("Stripe secret key"), 
        max_length=255, 
        blank=True, 
        null=True,
        help_text=_("Your Stripe Secret Key. This field is encrypted.")
    ))
    google_calendar_id = models.CharField(
        _("Google Calendar ID"), 
        max_length=255, 
        blank=True, 
        null=True,
        help_text=_("Calendar ID (usually an email address) for Google Calendar synchronization.")
    )
    logo = models.ImageField(
        _("logo"), 
        upload_to="logos/", 
        blank=True, 
        null=True,
        help_text=_("Recommended dimensions: 200x200 pixels.")
    )

    currency = models.CharField(
        _("currency"), 
        max_length=10, 
        choices=[("MXN", _("MXN")), ("USD", _("USD")), ("EUR", _("EUR"))],
        default="USD",
        help_text=_("Default currency for all services offered by the company.")
    )

    class Meta:
        verbose_name = _("Company Profile")
        verbose_name_plural = _("Company Profiles")

    def __str__(self):
        return str(_("Company Profile"))

class CompanyAvailability(BaseAvailabilityRange):
    """Global date-based availability ranges for a company."""
    company_profile = models.ForeignKey(
        CompanyProfile, 
        on_delete=models.CASCADE, 
        related_name="availability_rules", 
        verbose_name=_("company profile")
    )

    class Meta:
        verbose_name = _("Company Date Range")
        verbose_name_plural = _("Company Date Ranges")

    def __str__(self):
        return _("Global range for %(company)s") % {"company": "Company"}

class CompanyWeekdaySlot(BaseAvailabilitySlot):
    """Global weekly time windows for a company."""
    company_profile = models.ForeignKey(
        CompanyProfile, 
        on_delete=models.CASCADE, 
        related_name="weekday_slots", 
        verbose_name=_("company profile")
    )

    class Meta(BaseAvailabilitySlot.Meta):
        verbose_name = _("Business Hour")
        verbose_name_plural = _("Business Hours")

    def __str__(self):
        return f"{self.get_weekday_display()}: {self.start_time} - {self.end_time}"

class CompanyDateOverride(BaseDateOverride):
    """Global date-based exceptions for a company."""
    company_profile = models.ForeignKey(
        CompanyProfile, 
        on_delete=models.CASCADE, 
        related_name="date_overrides", 
        verbose_name=_("company profile")
    )

    class Meta:
        verbose_name = _("Company Date Override")
        verbose_name_plural = _("Company Date Overrides")
        unique_together = ["company_profile", "date"]

    def __str__(self):
        status = _("Available") if self.is_available else _("Blocked")
        return f"{self.date}: {status}"

class BusinessHours(models.Model):
    """Normalized storage for default weekly operating hours (Legacy - to be migrated)."""
    company_profile = models.ForeignKey(
        CompanyProfile, 
        on_delete=models.CASCADE, 
        related_name="business_hours", 
        verbose_name=_("company profile"),
        null=True,
        blank=True
    )
    weekday = models.IntegerField(_("weekday"), choices=[
        (0, _("Monday")), (1, _("Tuesday")), (2, _("Wednesday")),
        (3, _("Thursday")), (4, _("Friday")), (5, _("Saturday")), (6, _("Sunday"))
    ])
    start_time = models.TimeField(_("start time"))
    end_time = models.TimeField(_("end time"))

    class Meta:
        verbose_name = _("Operating Hour (Legacy)")
        verbose_name_plural = _("Operating Hours (Legacy)")
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
    allow_overlap = models.BooleanField(
        _("allow overlap"), 
        default=False,
        help_text=_("Allows multiple bookings for the same time slot (useful for classes or group events).")
    )

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
    price = models.DecimalField(
        _("price"), 
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text=_("The base cost of the service.")
    )
    duration_minutes = models.PositiveIntegerField(
        _("duration"), 
        default=30,
        help_text=_("Duration of the service in minutes.")
    )

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return f"{self.event_type.title}: {self.title}"

class EventAvailability(BaseAvailabilityRange):
    """Date-based availability rules (ranges) for a specific event."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="availability_rules", verbose_name=_("event"))

    class Meta:
        verbose_name = _("Date Range")
        verbose_name_plural = _("Date Ranges")

    def __str__(self):
        return _("Availability for %(event)s") % {"event": self.event.title}

class EventDateOverride(BaseDateOverride):
    """Specific dates that are either explicitly allowed or blocked for an event."""
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        related_name="date_overrides", 
        verbose_name=_("event")
    )

    class Meta:
        verbose_name = _("Date Override")
        verbose_name_plural = _("Date Overrides")
        unique_together = ["event", "date"]

    def __str__(self):
        status = _("Available") if self.is_available else _("Blocked")
        return f"{self.date}: {status}"

class AvailabilitySlot(BaseAvailabilitySlot):
    """Specific weekly time windows for an Event."""
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        related_name="availability_slots", 
        verbose_name=_("event"),
        help_text=_("Weekly pattern for this service. If any slot is defined here, the company's global 'Operating Hours' will be ignored for this event.")
    )

    weekday = models.IntegerField(_("weekday"), choices=[
        (0, _("Monday")), (1, _("Tuesday")), (2, _("Wednesday")),
        (3, _("Thursday")), (4, _("Friday")), (5, _("Saturday")), (6, _("Sunday"))
    ])
    start_time = models.TimeField(_("start time"))
    end_time = models.TimeField(_("end time"))

    class Meta:
        verbose_name = _("Bookable Slot")
        verbose_name_plural = _("Bookable Slots")
        ordering = ["weekday", "start_time"]

    def __str__(self):
        return f"{self.get_weekday_display()}: {self.start_time} - {self.end_time}"

class Booking(models.Model):
    """Individual appointments linked to specific events."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings", null=True, blank=True, verbose_name=_("event"))
    client_name = models.CharField(_("client name"), max_length=255)
    client_email = models.EmailField(_("client email"))
    start_time = models.DateTimeField(
        _("start time"),
        help_text=_("The date and time the appointment begins.")
    )
    end_time = models.DateTimeField(_("end time"), null=True, blank=True)
    status = models.CharField(
        _("status"),
        max_length=20, 
        choices=[("PENDING", _("Pending")), ("CONFIRMED", _("Confirmed")), ("PAID", _("Paid"))], 
        default="PENDING",
        help_text=_("Confirmed bookings trigger automated notifications.")
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
        Consolidated validation:
        1. All availability logic is now in `scheduler.services.validate_booking_time`.
        2. Overlap check remains here.
        """
        if not self.start_time or not self.event:
            super().clean()
            return

        # Dynamically import to avoid circular dependency: models <-> services
        from scheduler.services import validate_booking_time
        
        # Ensure end_time is calculated before validation
        self.end_time = self.start_time + timedelta(minutes=self.event.duration_minutes)
        
        # 1. Availability validation
        validate_booking_time(self.event, self.start_time, self.end_time)

        # 2. Overlap Check
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
