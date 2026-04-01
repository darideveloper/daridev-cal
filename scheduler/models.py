from datetime import timedelta
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django_cryptography.fields import encrypt

class CompanyProfile(models.Model):
    """Tenant-specific configuration."""
    brand_color = models.CharField(
        max_length=50,
        default="oklch(0.81 0.11 236)",
        validators=[
            RegexValidator(
                regex=r"^(#[0-9a-fA-F]{3}|#[0-9a-fA-F]{6}|oklch\([\d.]+\s[\d.]+\s[\d.]+\))$",
                message="Enter a valid HEX code or OKLCH function (e.g. #87d1ff or oklch(0.81 0.11 236))",
            )
        ],
    )
    stripe_public_key = models.CharField(max_length=255, null=True, blank=True)
    stripe_secret_key = encrypt(models.CharField(max_length=255, blank=True, null=True))
    google_calendar_id = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    currency = models.CharField(max_length=10, default="USD", help_text="The brand's operating currency.")

    def __str__(self):
        return "Company Profile"

class BusinessHours(models.Model):
    """Normalized storage for default weekly operating hours."""
    weekday = models.IntegerField(choices=[
        (0, "Monday"), (1, "Tuesday"), (2, "Wednesday"),
        (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday")
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name_plural = "Business Hours"
        ordering = ["weekday", "start_time"]

    def __str__(self):
        return f"{self.get_weekday_display()}: {self.start_time} - {self.end_time}"

class EventType(models.Model):
    """Service categories for grouping events."""
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    payment_model = models.CharField(
        max_length=10, 
        choices=[("PRE-PAID", "Pre-payment"), ("POST-PAID", "Post-payment")], 
        default="POST-PAID"
    )
    allow_overlap = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Event(models.Model):
    """A specific bookable service."""
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    detailed_description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    format_category = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.event_type.title}: {self.title}"

class EventAvailability(models.Model):
    """Date-based availability rules for a specific event."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="availability_rules")
    start_date = models.DateField(null=True, blank=True, help_text="Start of the rule's validity.")
    end_date = models.DateField(null=True, blank=True, help_text="End of the rule's validity.")

    def __str__(self):
        return f"Availability for {self.event.title}"

class AvailabilitySlot(models.Model):
    """Specific time windows for an EventAvailability set."""
    event_availability = models.ForeignKey(EventAvailability, on_delete=models.CASCADE, related_name="slots")
    weekday = models.IntegerField(choices=[
        (0, "Monday"), (1, "Tuesday"), (2, "Wednesday"),
        (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday")
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["weekday", "start_time"]

class Booking(models.Model):
    """Individual appointments linked to specific events."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings", null=True, blank=True)
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=[("PENDING", "Pending"), ("CONFIRMED", "Confirmed"), ("PAID", "Paid")], 
        default="PENDING"
    )

    def __str__(self):
        return f"{self.client_name} - {self.event.title}"

    def save(self, *args, **kwargs):
        # Auto-calculate end_time from start_time + event duration
        if self.start_time and self.event:
            self.end_time = self.start_time + timedelta(minutes=self.event.duration_minutes)
        super().save(*args, **kwargs)

    def clean(self):
        """
        Delegates validation to the service layer.
        For backwards compatibility during refactor, skeletal check remains.
        """
        if self.start_time and self.event:
            self.end_time = self.start_time + timedelta(minutes=self.event.duration_minutes)
            
            if not self.event.event_type.allow_overlap:
                overlapping_bookings = Booking.objects.filter(
                    start_time__lt=self.end_time,
                    end_time__gt=self.start_time
                ).exclude(pk=self.pk) if self.pk else Booking.objects.filter(
                    start_time__lt=self.end_time,
                    end_time__gt=self.start_time
                )
                    
                if overlapping_bookings.exists():
                    raise ValidationError("This booking overlaps with an existing appointment.")
        super().clean()
