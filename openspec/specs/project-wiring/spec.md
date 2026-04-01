# project-wiring Specification

## Purpose
TBD - created by archiving change init-daridev-cal-project. Update Purpose after archive.
## Requirements
### Requirement: URL Configuration
The project's URLs SHALL be correctly configured to include the Django Admin and a REST API router, strictly separating public and tenant endpoints to avoid database overlap errors.

#### Scenario: Global URLs
- **Given** I am in `project/urls_public.py`
- **When** I check the `urlpatterns`
- **Then** the `admin/` route SHALL map to `PublicAdminSite`.
- **And** the `i18n/` URL SHALL be included for language switching.
- **And** the root redirect to admin SHALL use `pattern_name="admin:index"` for language awareness.

#### Scenario: Tenant URLs
- **Given** I am in `project/urls.py`
- **When** I check the `urlpatterns`
- **Then** the `admin/` route SHALL map to `TenantAdminSite`.
- **And** the `i18n/` URL SHALL be included for language switching.
- **And** the `api/` route SHALL map to the REST API router.
- **And** the root redirect to admin SHALL use `pattern_name="admin:index"` for language awareness.

### Requirement: i18n URL Prefixes
The project SHALL use language-prefixed URLs for its admin and home interfaces.

#### Scenario: Language Prefixed Patterns
- **Given** I am in `project/urls.py` or `project/urls_public.py`
- **When** I check the `urlpatterns`
- **Then** `admin/` and root patterns SHALL be wrapped in `i18n_patterns`.

### Requirement: API Support
The project SHALL include custom pagination and exception handling for its API.

#### Scenario: Custom Pagination
- **Given** I am in `project/pagination.py`
- **When** I use `CustomPageNumberPagination`
- **Then** the paginated responses SHALL include `count`, `next`, `previous`, `page`, `page_size`, `total_pages`, and `results`.

#### Scenario: Exception Handler
- **Given** I am in `project/handlers.py`
- **When** I use `custom_exception_handler`
- **Then** error responses SHALL follow a standardized structure with `status`, `message`, and `data`.

### Requirement: Custom Storage Backends
The project SHALL support custom S3 storage classes for static and media files.

#### Scenario: S3 Storage Backends
- **Given** I am in `project/storage_backends.py`
- **When** I check the storage classes
- **Then** `StaticStorage`, `PublicMediaStorage`, and `PrivateMediaStorage` SHALL be correctly defined.

