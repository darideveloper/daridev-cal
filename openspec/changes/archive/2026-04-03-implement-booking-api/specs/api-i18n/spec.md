# Spec Delta: API i18n Support

Define requirements for multi-language support in public API endpoints.

## ADDED Requirements
### Requirement: Localized Public Content
All public API endpoints MUST support content localization based on the standard `Accept-Language` header.

#### Scenario: Fetching Localized Event Data
- **Given** an event with titles and descriptions available in English and Spanish.
- **When** an unauthenticated request to `GET /api/events/` is made with `Accept-Language: es`.
- **Then** the response fields for `title` and `description` MUST return the Spanish translation.
- **And** the status code should be `200 OK`.

#### Scenario: Localized Validation Errors
- **Given** an invalid booking request.
- **When** the request is made with `Accept-Language: es`.
- **Then** the error messages in the response MUST be returned in Spanish.
- **And** the status code should be `400 Bad Request`.
