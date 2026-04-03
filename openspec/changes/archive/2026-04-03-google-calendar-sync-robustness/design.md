# Design: Google Calendar Robustness

## 1. Data Model
To track sync status, the `Booking` model will be expanded with the following fields:

- **`google_sync_status`**: `CharField` (Choices: `PENDING`, `SUCCESS`, `FAILURE`, `DISABLED`)
- **`last_synced_at`**: `DateTimeField` (Optional)
- **`sync_error`**: `TextField` (Optional, encrypted if necessary, but plain text is usually fine for debugging).

## 2. Service Layer Updates: `scheduler/google_calendar.py`
The service functions will be updated to:
- Accept a `skip_save` parameter to avoid recursion if needed.
- Catch `HttpError` specifically:
    - 401/403: Update status to `FAILURE`.
    - 404 on `patch`: Re-create the event (Self-healing).
- Provide a `delete_google_calendar_event(booking)` function.

## 3. Observer Pattern: `scheduler/signals.py`
- **`post_save`**: Keep as is, but updated to handle status updates.
- **`post_delete`**: Implement to gracefully remove external events.

## 4. UI: `scheduler/admin.py`
- Add an `Unfold` action: `sync_with_google`.
- This action iterates over selected bookings and calls `sync_booking_to_google` for each.

## 5. Security Note
To avoid storing credentials twice, the service continues to look up the `CompanyProfile` for credentials on each call. If the profile doesn't exist, the status is set to `DISABLED`.
