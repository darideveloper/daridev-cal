# utilities Specification

## Purpose
TBD - created by archiving change init-daridev-cal-project. Update Purpose after archive.
## Requirements
### Requirement: Admin Permission Helpers
The project SHALL include utilities for validating admin and support group permissions.

#### Scenario: Admin Group Validation
- **Given** I am in `utils/admin_helpers.py`
- **When** the `is_user_admin` function is called with a user object
- **Then** it SHALL correctly identify if the user belongs to "admins" or "supports" groups or is a superuser.

### Requirement: Automation Helpers
The project SHALL include helpers for Selenium-based web automation.

#### Scenario: Element Retrieval
- **Given** I am in `utils/automation.py`
- **When** `get_selenium_elems` is called with a driver and selectors
- **Then** it SHALL return a dictionary of web elements found using CSS selectors.

### Requirement: Media Processing Helpers
The project SHALL include utilities for image processing and URL resolution.

#### Scenario: URL Resolution
- **Given** I am in `utils/media.py`
- **When** `get_media_url` is called with an object or URL string
- **Then** it SHALL return a fully qualified URL including the host if the file is stored locally.

#### Scenario: Test Image Generation
- **Given** I am in `utils/media.py`
- **When** `get_test_image` is called
- **Then** it SHALL return a valid `SimpleUploadedFile` for testing purposes.

### Requirement: Environment Badge Callback
The project SHALL include a callback function to identify the current environment stage in the admin interface.

#### Scenario: Environment Badge Identification
- **Given** I am in `utils/callbacks.py`
- **When** `environment_callback` is executed
- **Then** it SHALL return the environment label and badge color (e.g., ["Production", "danger"]) based on the `ENV` variable.

