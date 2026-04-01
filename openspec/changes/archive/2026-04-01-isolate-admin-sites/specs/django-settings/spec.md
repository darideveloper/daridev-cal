## ADDED Requirements
### Requirement: Multi-Tenant Schema Routing
The `settings.py` SHALL define distinct routing configurations to isolate the public schema from the tenant schemas.

#### Scenario: Multi-Tenant Router
- **Given** I am in `project/settings.py`
- **When** the URLs are configured
- **Then** it SHALL define `PUBLIC_SCHEMA_URLCONF` for public domain traffic and `ROOT_URLCONF` for tenant domain traffic.

## MODIFIED Requirements
### Requirement: Unfold Brand Customization
The project SHALL configure `django-unfold` in `settings.py` with custom branding and operational features.

#### Scenario: Site Metadata
- **Given** I am in `project/settings.py`
- **When** `UNFOLD` dictionary is defined
- **Then** `SITE_TITLE`, `SITE_HEADER`, and `SITE_SUBHEADER` SHALL align with "DARI DEV CAL" branding.
- **Then** `THEME` SHALL be set to "light".
- **Then** `SITE_SYMBOL` SHALL be set to "calendar_today".

#### Scenario: Admin Features
- **Given** I am in `project/settings.py`
- **When** I configure Unfold
- **Then** `SHOW_HISTORY` and `SHOW_VIEW_ON_SITE` SHALL be set to `True`.

#### Scenario: Color Customization
- **Given** `#87d1ff` is the primary brand color
- **When** `UNFOLD["COLORS"]["primary"]` is defined
- **Then** it SHALL use an OKLCH scale centered around `oklch(0.81 0.11 236)`.

#### Scenario: Custom Sidebar
- **Given** `UNFOLD["SIDEBAR"]` is configured
- **When** I check the `navigation`
- **Then** it SHALL use `reverse_lazy` for model links and Material Symbols for icons.
- **Then** global items (System, Multi-Tenancy) SHALL enforce a `permission` check restricting them to `schema_name == 'public'`.
- **Then** tenant items (Booking App) SHALL enforce a `permission` check restricting them to `schema_name != 'public'`.
