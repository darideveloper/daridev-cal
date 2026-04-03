# Capability: Sync Robustness

## ADDED Requirements

### Requirement: [ADDED] Automated Sync Lifecycle
Synchronization MUST follow the lifecycle of the object (Creation, Update, and Deletion).

#### Scenario: Deleting a booking
**Context**: An existing `Booking` record that is already synced to Google Calendar (has a `google_event_id`).
**Action**: The admin or client deletes the `Booking` record.
**Result**:
- A `post_delete` signal is triggered.
- `google_calendar.delete_google_calendar_event()` is called with the `google_event_id`.
- The corresponding Google Calendar event is deleted.

### Requirement: [ADDED] Monitoring & Error Capture
Every synchronization attempt MUST be tracked at the database level for monitoring purposes.

#### Scenario: Sync Success
**Context**: A valid `Booking` record.
**Action**: `sync_booking_to_google` is executed successfully.
**Result**:
- `google_sync_status` is set to `SUCCESS`.
- `last_synced_at` is updated to the current server timestamp.
- `google_sync_error` is cleared (null).

#### Scenario: Sync Failure
**Context**: Invalid credentials or network error during sync.
**Action**: `sync_booking_to_google` fails.
**Result**:
- `google_sync_status` is set to `FAILURE`.
- `google_sync_error` is populated with the error message.
- `last_synced_at` is updated to reflect the last attempt.

#### Scenario: Missing Configuration
**Context**: A tenant with no `google_calendar_credentials` provided.
**Action**: A booking is created or updated.
**Result**:
- `google_sync_status` is set to `DISABLED`.
- No Google API call is attempted.
