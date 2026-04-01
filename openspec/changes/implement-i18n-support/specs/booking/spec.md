# Spec: Booking App

## MODIFIED Requirements

### Requirement: Translatable App Name

The application's display name in the admin interface MUST be translatable.

#### Scenario: Admin Sidebar
- **GIVEN** the `BookingConfig` in `booking/apps.py`
- **WHEN** the admin sidebar is rendered
- **THEN** the `verbose_name` attribute must be set to a translatable string using `gettext_lazy`.
