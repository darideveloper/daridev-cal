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
The localization requirements for the `Event` model SHALL be updated to remove the redundant `currency` field.

#### MODIFIED Scenario: Translatable Metadata and Choices
- **Given** I am in `scheduler/models.py`
- **When** I check the `Event` model
- **Then** the `currency` field SHALL NOT be present.
- **AND** the localization for `Event.currency` SHALL be removed.

### Requirement: Tenant Admin Integration
The `EventAdmin` SHALL be updated to reflect the removal of the `currency` field.

#### MODIFIED Scenario: Event Management (EventAdmin)
- **GIVEN** an administrator is editing an `Event` in the Unfold Admin
- **WHEN** they view the "General" tab
- **THEN** the `currency` field MUST NOT be displayed.

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

### Requirement: Customizable UI Labels
The `CompanyProfile` SHALL include fields to allow tenants to customize the labels used in the frontend booking UI.

#### Scenario: `CompanyProfile` UI label fields
- `event_type_label`: `CharField` (max_length=100, default=_("Event Type")).
- `event_label`: `CharField` (max_length=100, default=_("Event")).
- `availability_free_label`: `CharField` (max_length=100, default=_("Free")).
- `availability_regular_label`: `CharField` (max_length=100, default=_("Regular")).
- `availability_no_free_label`: `CharField` (max_length=100, default=_("Full")).
- `extras_label`: `CharField` (max_length=100, default=_("Extras")).

#### Scenario: Translatable UI labels
- **Given** I am editing the `CompanyProfile` in the admin.
- **Then** the labels and help texts for these new fields SHALL be translatable.
- **AND** they SHALL be organized in a "UI Labels" tab.

