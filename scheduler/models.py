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

    def __str__(self):
        return "Company Profile"

class EventType(models.Model):
    """Service definitions for booking."""
    title = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField(default=30)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_model = models.CharField(
        max_length=10, 
        choices=[("PRE-PAID", "Pre-payment"), ("POST-PAID", "Post-payment")], 
        default="POST-PAID"
    )
    allow_overlap = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Booking(models.Model):
    """Individual appointments."""
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name="bookings")
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
        return f"{self.client_name} - {self.event_type.title}"

    def save(self, *args, **kwargs):
        # Auto-calculate end_time from start_time + duration
        if self.start_time and self.event_type:
            self.end_time = self.start_time + timedelta(minutes=self.event_type.duration_minutes)
        super().save(*args, **kwargs)

    def clean(self):
        """
        Validation logic: (NewStart < ExistingEnd) AND (NewEnd > ExistingStart)
        based on EventType.allow_overlap.
        """
        # First calculate end_time for the check if not set (or if start_time changed)
        if self.start_time and self.event_type:
            self.end_time = self.start_time + timedelta(minutes=self.event_type.duration_minutes)
            
            if not self.event_type.allow_overlap:
                overlapping_bookings = Booking.objects.filter(
                    start_time__lt=self.end_time,
                    end_time__gt=self.start_time
                )
                
                if self.pk:
                    overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)
                    
                if overlapping_bookings.exists():
                    raise ValidationError("This booking overlaps with an existing appointment.")
        super().clean()
