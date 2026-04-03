# storage Specification

## Purpose
TBD - created by archiving change google-calendar-sync. Update Purpose after archive.
## Requirements
### Requirement: Secure Tenant Service Credentials
The `CompanyProfile` model MUST be extended with a `google_calendar_credentials` field that utilizes encryption.

#### Scenario: Store Google Service Account Credentials
- **GIVEN** a tenant has a Google Cloud Service Account JSON key
- **WHEN** they paste the raw JSON into the "Google Calendar Credentials" field in the admin
- **THEN** the system stores the content in an encrypted format using `django-cryptography`.

### Requirement: Track External Calendar Events
The `Booking` model MUST be extended with a `google_event_id` field to maintain a reference to the corresponding external calendar event.

#### Scenario: First successful sync
- **GIVEN** a new `Booking` is being synced for the first time
- **WHEN** the Google Calendar API returns a success response with an event ID
- **THEN** the system updates the `Booking` record with this `google_event_id`.

