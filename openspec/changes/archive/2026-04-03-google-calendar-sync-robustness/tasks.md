# Tasks: Google Calendar Sync Robustness

## 1. Model Updates
- [x] Add `google_sync_status`, `google_sync_error`, and `last_synced_at` to `Booking`.
- [x] Add choices (PENDING, SUCCESS, FAILURE, DISABLED) for `google_sync_status`.
- [x] Create and apply migrations.

## 2. Service Layer Enhancements
- [x] Implement `delete_google_calendar_event(booking)` in `scheduler/google_calendar.py`.
- [x] Update `sync_booking_to_google` to capture sync results and update `Booking` status fields.
- [x] Include a retry mechanism logic inside `sync_booking_to_google` (optional but recommended).

## 3. Signal Configuration
- [x] Add `post_delete` signal to `scheduler/signals.py` to trigger event deletion.
- [x] Ensure `post_save` correctly handles the updated status logic.

## 4. Admin Customization
- [x] Add `google_sync_status` to `BookingAdmin.list_display`.
- [x] Implement a "Manual Sync" action for `BookingAdmin` to re-sync selected entries.

## 5. Robust Automated Testing
- [x] Add `test_sync_recreation_on_404` to `scheduler/test_google_calendar.py`.
- [x] Add `test_sync_failure_handling` (401/403 mocks).
- [x] Add `test_deletion_sync` to verify `post_delete` calls `google_calendar.delete_event`.
- [x] Add `test_manual_sync_action` to verify the admin action logic.
