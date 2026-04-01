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
The project SHALL be configured with a specific time zone and language.

#### Scenario: Time Zone Setup
- **Given** `TIME_ZONE` is set to `America/Mexico_City`
- **When** I check the project configuration
- **Then** `TIME_ZONE` and `USE_TZ` SHALL be correctly configured.

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

### Requirement: App Integration
Unfold and its extensions SHALL be integrated into `INSTALLED_APPS`.

#### Scenario: App Ordering
- **Given** I am in `project/settings.py`
- **When** I add Unfold apps
- **Then** `unfold`, `unfold.contrib.filters`, `unfold.contrib.forms`, and `unfold.contrib.inlines` SHALL be listed BEFORE `django.contrib.admin`.

