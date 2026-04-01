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

