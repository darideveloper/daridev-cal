## MODIFIED Requirements

### Requirement: Automated Real-time Synchronization
The system MUST synchronize booking details with Google Calendar automatically upon creation or update using the centralized master credentials.

#### Scenario: Insert New Event
- **GIVEN** a `Booking` is confirmed
- **AND** the master `GOOGLE_CALENDAR_CREDENTIALS` and the tenant's `google_calendar_id` are configured
- **WHEN** the `Booking` is saved for the first time
- **THEN** the system inserts a new event into the tenant's Google Calendar and stores the returned event ID.

#### Scenario: Update Existing Event
- **GIVEN** a `Booking` already has a `google_event_id`
- **WHEN** its `start_time` or `client_name` is modified and saved
- **THEN** the system patches the existing event in Google Calendar with the new details.

## ADDED Requirements

### Requirement: Resilient Authentication
The integration MUST handle invalid or missing credentials gracefully.

#### Scenario: Missing Credentials
- **GIVEN** `GOOGLE_CALENDAR_CREDENTIALS` is NOT configured in global settings
- **WHEN** a new `Booking` is saved
- **THEN** the system skips the synchronization step with a "FAILURE" status but without raising a blocking error for the user.
