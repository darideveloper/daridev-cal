# Proposal: Google Calendar Sync Robustness

## Why
To enhance the Google Calendar integration with event deletion synchronization, improved visibility into sync status, and a mechanism for manual error recovery.

## Context
The initial implementation of Google Calendar synchronization provides real-time creation and updates for bookings. However, it lacks:
- **Deletion Sync**: Removing events from Google Calendar when a booking is deleted.
- **Monitoring**: Tracking whether a sync succeeded or failed.
- **Resilience**: A way to manually retry a failed sync or re-sync all data.

## What Changes

### Model Updates
- **`Booking`**: Add `sync_status` (Choices: `PENDING`, `SUCCESS`, `FAILED`) and `last_synced_at` (Datetime).
- **`Booking`**: Add `sync_error` (TextField) to store the latest error message for easier debugging.

### Logic & Services
- **`scheduler/google_calendar.py`**:
    - Update `sync_booking_to_google` to update the `sync_status` and `last_synced_at` fields on success or failure.
    - Implement `delete_google_calendar_event(booking)` to remove events from Google.
- **`scheduler/signals.py`**:
    - Add a `post_delete` signal handler to trigger `delete_google_calendar_event`.

### Admin Enhancements
- **Action**: Add a "Retry Sync with Google Calendar" action to the `Booking` admin to allow bulk re-syncing of selected records.
- **List Display**: Include `sync_status` in the list view for better monitoring.

### Acceptance Criteria
- [x] Deleting a booking in Django removes the corresponding event in Google Calendar.
- [x] Every booking record clearly shows its latest sync status and timestamp.
- [x] Admins can manually trigger a sync for one or more bookings from the admin action menu.
- [x] Automated tests cover deletion, self-healing (404), and authentication failures.
