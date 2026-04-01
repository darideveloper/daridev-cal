# scheduler Specification

## Purpose
TBD - created by archiving change register-multi-tenant-models. Update Purpose after archive.
## Requirements
### Requirement: CompanyProfile Model 
The CompanyProfile model SHALL be implemented.
Each tenant will have its own profile with encrypted credentials and branding.

#### Scenario: `CompanyProfile` fields
- `stripe_public_key`: `CharField` (max_length=255, null=True, blank=True).
- `stripe_secret_key`: `EncryptedCharField` (from `django-cryptography`).
- `google_calendar_id`: `CharField` (max_length=255, null=True, blank=True).
- `logo`: `ImageField` (to be stored in tenant-specific storage if possible).
- **BRAND_COLOR**: `CharField` (max_length=50, default="oklch(0.81 0.11 236)") with `RegexValidator` for OKLCH/HEX formats.

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

### Requirement: Model and Service Localization
The project SHALL provide translated names for models, fields, choices, and validation messages in the `scheduler` app.

#### Scenario: Translatable Metadata and Choices
- **Given** I am in `scheduler/models.py`
- **When** I check the models and their choices (e.g., Weekday, Status)
- **Then** they SHALL be wrapped in `gettext_lazy`.
- **AND** their `verbose_name` and `help_text` SHALL be translatable.

#### Scenario: Service Layer Translations
- **Given** I am in `scheduler/services.py`
- **When** a `ValidationError` is raised
- **Then** the message SHALL be translatable using `gettext_lazy`.

### Requirement: Tenant Admin Integration
The Tenant Admin Integration SHALL be implemented. Register models with `django-unfold`.

#### MODIFIED Scenario: Settings Hub (CompanyProfileAdmin)
- **GIVEN** I am in `scheduler/admin.py`
- **WHEN** I edit the `CompanyProfile` singleton
- **THEN** a `logo_preview` SHALL NOT be displayed.

### Requirement: Tenant-based Branding Logic
The admin interface MUST display the specific branding (Title, Header, Logo) based on the current active tenant.

#### Scenario: Active Tenant Admin
**Given** a request is made to a tenant-specific admin domain (e.g., `company1.localhost/admin/`)
**When** the page is rendered
**Then** the `<title>` MUST include "First Company" (or the tenant's name)
**AND** the admin sidebar header MUST display the tenant name
**AND** the site logo MUST be the one uploaded to `CompanyProfile` for that tenant.

#### Scenario: Public Admin Branding
**Given** a request is made to the public admin domain (e.g., `localhost/admin/`)
**When** the page is rendered
**Then** the branding MUST default to "DARI DEV CAL" and the default site logo.

