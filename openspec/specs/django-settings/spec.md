# django-settings Specification

## Purpose
TBD - created by archiving change init-daridev-cal-project. Update Purpose after archive.
## Requirements
### Requirement: Dynamic Configuration
The `settings.py` SHALL load environment variables from `.env` files.

#### Scenario: Dotenv Integration
- **Given** I am in `project/settings.py`
- **When** I initialize `python-dotenv`
- **Then** it SHALL load `.env` first, followed by the environment-specific file determined by `ENV`.

### Requirement: Database Selection
The project SHALL dynamically switch between database backends.

#### Scenario: Test Database Isolation
- **Given** I am running `python manage.py test`
- **When** the project initializes
- **Then** it SHALL use a SQLite database.

#### Scenario: Production Database
- **Given** I am in a dev or prod environment
- **When** `DB_ENGINE` is specified in the environment
- **Then** it SHALL use the corresponding database credentials.

### Requirement: Storage Configuration
The project SHALL support both local and cloud-based file storage.

#### Scenario: AWS S3 Storage
- **Given** `STORAGE_AWS=True` is set in the environment
- **When** I upload a file
- **Then** it SHALL be stored in an AWS S3 bucket.

### Requirement: Localization
The project SHALL be configured with a specific time zone and language, supporting multi-language interfaces.

#### Scenario: i18n/l10n Configuration
- **Given** I am in `project/settings.py`
- **When** I check the project configuration
- **Then** `TIME_ZONE` and `USE_TZ` SHALL be correctly configured.
- **AND** `USE_I18N` SHALL be set to `True`.
- **AND** `LANGUAGES` SHALL include at least English and Spanish.
- **AND** `LOCALE_PATHS` SHALL point to the project's `locale` directory.
- **AND** `django.middleware.locale.LocaleMiddleware` SHALL be inserted in `MIDDLEWARE` after `SessionMiddleware`.

### Requirement: Unfold Brand Customization
The project SHALL configure `django-unfold` in `settings.py` with custom branding and operational features.

#### Scenario: Color Customization
- **Given** I am in `project/settings.py`
- **When** the `UNFOLD["COLORS"]["primary"]` is configured
- **Then** it SHALL prioritize using the CSS variables `var(--color-primary-400)`, `var(--color-primary-500)`, and `var(--color-primary-600)`.
- **And** it SHALL fallback to default OKLCH values for the public schema.

### Requirement: App Integration
Unfold and its extensions SHALL be integrated into `INSTALLED_APPS`.

#### Scenario: App Ordering
- **Given** I am in `project/settings.py`
- **When** I add Unfold apps
- **Then** `unfold`, `unfold.contrib.filters`, `unfold.contrib.forms`, and `unfold.contrib.inlines` SHALL be listed BEFORE `django.contrib.admin`.

### Requirement: Multi-Tenant Schema Routing
The `settings.py` SHALL define distinct routing configurations to isolate the public schema from the tenant schemas.

#### Scenario: Multi-Tenant Router
- **Given** I am in `project/settings.py`
- **When** the URLs are configured
- **Then** it SHALL define `PUBLIC_SCHEMA_URLCONF` for public domain traffic and `ROOT_URLCONF` for tenant domain traffic.

