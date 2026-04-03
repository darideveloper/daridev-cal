# Tasks: Google Calendar Integration

## 1. Environment & Dependencies
- [x] Add `google-api-python-client`, `google-auth`, and `google-auth-httplib2` to `requirements.txt`.
- [x] Verify consistent installation in the development environment.

## 2. Model Updates
- [x] Add `google_calendar_credentials` (encrypted) to `CompanyProfile`.
- [x] Add `google_event_id` to `Booking`.
- [x] Create and apply migrations for these fields across all tenant schemas.
- [x] Update `CompanyProfileAdmin` and `BookingAdmin` to include the new fields.

## 3. Integration Service
- [x] Create `scheduler/google_calendar.py`.
- [x] Implement `get_google_calendar_service(company_profile)` to initialize the Google API client with service account credentials.
- [x] Implement `sync_booking_to_google(booking)` to handle both `insert` and `patch` operations.
- [x] Map internal `Booking` fields to a valid Google Calendar event body.

## 4. Automation & Signals
- [x] Create `scheduler/signals.py`.
- [x] Implement the `post_save` receiver for the `Booking` model to call `sync_booking_to_google` when credentials exist.
- [x] Register `scheduler/signals` in `scheduler/apps.py:SchedulerConfig.ready()`.

## 5. Testing & Validation
- [x] Unit test `get_google_calendar_service` with mocked credentials.
- [x] Integration test `sync_booking_to_google` by mocking the Google API client response.
- [x] Verify that saving a `Booking` via the admin correctly triggers the synchronization.
- [x] Validate handle error scenarios (e.g., missing credentials or invalid calendar ID).
