## MODIFIED Requirements

### Requirement: Dynamic Tenant Branding SHALL be implemented.
The `django-unfold` interface SHALL dynamically reflect the active tenant's branding using callback strings in `settings.py` mapped to functions in `utils.callbacks`. To ensure textual branding (headline) correctly displays, the `SITE_LOGO` option SHALL NOT be declared in `UNFOLD`.

#### Scenario: Dynamic Header and Icon
- **Given** I am rendering the Unfold admin interface
- **When** the `SITE_HEADER` and `SITE_TITLE` config is evaluated
- **Then** they SHALL return the result of `request.tenant.name` from the tenant schema via a callback, and `SITE_LOGO` MUST remain undefined so the text displays.
- **And** `SITE_ICON` SHALL return the URL of `request.tenant.companyprofile.logo` via a callback if a profile and logo exist, otherwise fallback to the default global icon.
