# Spec Delta: `scheduler` App (Tenant Schema)

## ADDED Requirements

### Requirement: CompanyProfile Model 
The CompanyProfile model SHALL be implemented.
Each tenant will have its own profile with encrypted credentials and branding.

#### Scenario: `CompanyProfile` fields
- `stripe_public_key`: `CharField` (max_length=255, null=True, blank=True).
- `stripe_secret_key`: `EncryptedCharField` (from `django-cryptography`).
- `google_calendar_id`: `CharField` (max_length=255, null=True, blank=True).
- `logo`: `ImageField` (to be stored in tenant-specific storage if possible).

### Requirement: EventType Model 
The EventType model SHALL be implemented.
Defines scheduling services.

#### Scenario: `EventType` configuration
- `title`: `CharField` (max_length=100).
- `duration_minutes`: `PositiveIntegerField` (e.g., 30, 60).
- `price`: `DecimalField` (max_digits=10, decimal_places=2, default=0.0).
- `payment_model`: `CharField` (Choices: `PRE-PAID`, `POST-PAID`).
- `allow_overlap`: `BooleanField` (default=False).

### Requirement: Booking Model 
The Booking model SHALL be implemented.
Records appointments.

#### Scenario: `Booking` life-cycle
- `event_type`: `FK(EventType)`.
- `client_name`: `CharField`.
- `client_email`: `EmailField`.
- `start_time`: `DateTimeField`.
- `end_time`: `DateTimeField` (auto-calculated from `start_time + event_type.duration`).
- `status`: `CharField` (Choices: `PENDING`, `CONFIRMED`, `PAID`).

#### Scenario: `Booking.clean()` conflict validation
- If `event_type.allow_overlap` is `False`, perform a query to check for overlapping bookings in the same schema.
- Conflict logic: `(NewStart < ExistingEnd) AND (NewEnd > ExistingStart)`.

### Requirement: Tenant Admin Integration 
The Tenant Admin Integration SHALL be implemented.
Register models with `django-unfold`.

#### Scenario: `BookingAdmin` features
- List display with status badges (using Unfold labels).
- Filter by `start_time`, `status`.
- Search by `client_name`, `client_email`.
