# Capability: Scheduler i18n and Field Descriptions

## MODIFIED Requirements
### Requirement: Model and Service Localization
The project SHALL provide translated names for models, fields, choices, and validation messages in the `scheduler` app.

#### Scenario: Translatable Metadata and Choices
- **Given** I am in `scheduler/models.py`
- **When** I check the models and their choices (e.g., Weekday, Status)
- **Then** they SHALL be wrapped in `gettext_lazy`.
- **AND** their `verbose_name` and `help_text` SHALL be translatable.
- **AND** `CompanyProfile.brand_color` SHALL have verbose_name = _("brand primary color") and help_text = _("The main color for the booking page. Supports HEX and OKLCH format (e.g., oklch(0.8 0.1 240)).")
- **AND** `CompanyProfile.stripe_public_key` SHALL have help_text = _("Your Stripe Publishable Key found in the Developer Dashboard.")
- **AND** `CompanyProfile.stripe_secret_key` SHALL have help_text = _("Your Stripe Secret Key. This field is encrypted.")
- **AND** `CompanyProfile.google_calendar_id` SHALL have help_text = _("Calendar ID (usually an email address) for Google Calendar synchronization.")
- **AND** `CompanyProfile.logo` SHALL have help_text = _("Recommended dimensions: 200x200 pixels.")
- **AND** `CompanyProfile.currency` SHALL have help_text = _("Default currency for all services offered by the company.")
- **AND** `Event.duration_minutes` SHALL have verbose_name = _("duration") and help_text = _("Duration of the service in minutes.")
- **AND** `Event.price` SHALL have help_text = _("The base cost of the service.")
- **AND** `EventType.allow_overlap` SHALL have help_text = _("Allows multiple bookings for the same time slot (useful for classes or group events).")
- **AND** `Booking.status` SHALL have help_text = _("Confirmed bookings trigger automated notifications.")
- **AND** `Booking.start_time` SHALL have help_text = _("The date and time the appointment begins.")
