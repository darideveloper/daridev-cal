# Spec: Project Wiring

## MODIFIED Requirements

### Requirement: Language-Prefixed URLs

The system MUST use URL prefixes to determine the active language for a request.

#### Scenario: Admin URLs
- **GIVEN** a request to the admin interface
- **WHEN** the URL is resolved
- **THEN** the admin URL patterns must be wrapped in `i18n_patterns`
- **AND** the URL must be prefixed with a language code (e.g., `/en/admin/`, `/es/admin/`).

## ADDED Requirements

### Requirement: Language Switching URL

The system MUST provide an endpoint to allow users to change the active language.

#### Scenario: Language Selector
- **GIVEN** the root URL configuration
- **WHEN** the application is running
- **THEN** a `path('i18n/', include('django.conf.urls.i18n'))` must be included in the `urlpatterns`.
