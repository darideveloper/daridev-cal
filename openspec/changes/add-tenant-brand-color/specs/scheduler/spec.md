## MODIFIED Requirements
### Requirement: CompanyProfile Model 
The CompanyProfile model SHALL be implemented.
Each tenant will have its own profile with encrypted credentials and branding.

#### Scenario: `CompanyProfile` fields
- `stripe_public_key`: `CharField` (max_length=255, null=True, blank=True).
- `stripe_secret_key`: `EncryptedCharField` (from `django-cryptography`).
- `google_calendar_id`: `CharField` (max_length=255, null=True, blank=True).
- `logo`: `ImageField` (to be stored in tenant-specific storage if possible).
- **BRAND_COLOR**: `CharField` (max_length=50, default="oklch(0.81 0.11 236)") with `RegexValidator` for OKLCH/HEX formats.
