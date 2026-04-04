## MODIFIED Requirements

### Requirement: CompanyProfile Model 
The CompanyProfile model SHALL be implemented.
Each tenant will have its own profile for branding and per-tenant configurations (using centralized master credentials for third-party integrations).

#### Scenario: `CompanyProfile` fields
- `stripe_public_key`: `CharField` (max_length=255, null=True, blank=True).
- `stripe_secret_key`: `EncryptedCharField` (from `django-cryptography`).
- `stripe_webhook_secret`: `EncryptedCharField`.
- `google_calendar_id`: `CharField` (max_length=255, null=True, blank=True, help_text=_("Calendar ID created automatically for this tenant.")).
- `logo`: `ImageField` (to be stored in tenant-specific storage if possible).
- **BRAND_COLOR**: `CharField` (max_length=50, default="oklch(0.81 0.11 236)") with `RegexValidator` for OKLCH/HEX formats.

## ADDED Requirements

### Requirement: Automated Calendar Provisioning
The system MUST automatically provision a new Google Calendar for tenants that do not have any `google_calendar_id` set.

#### Scenario: Auto-create Calendar
- **GIVEN** a new `CompanyProfile` is created
- **AND** `google_calendar_id` is empty
- **THEN** the system creates a new calendar via the master account and assigns the ID to the profile.
