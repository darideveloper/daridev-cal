# Change: Google Calendar Integration

## Why
Currently, tenant users have to manually add bookings to their Google Calendar. By integrating directly with the Google Calendar API, the application will provide a seamless automated experience where every confirmed booking is synced in real-time, including updates. This reduces manual work and ensures schedule consistency for professional providers.

## What Changes
- [ ] Add `google_calendar_credentials` (encrypted) to the `CompanyProfile` model.
- [ ] Add `google_event_id` to the `Booking` model to track external events.
- [ ] Create a robust `GoogleCalendarService` for authentication and event synchronization (Insert/Patch).
- [ ] Implement `post_save` signals on the `Booking` model for automated synchronization.
- [ ] Add Google API client libraries to `requirements.txt`.
- [ ] Update the `CompanyProfile` and `Booking` admin interfaces to support the integration.

## Impact
- Affected specs: `company-profile-updates`, `booking-logic`, `scheduler` (new specs for integration and service will be added)
- Affected code: `scheduler/models.py`, `scheduler/services.py`, `scheduler/admin.py`, `requirements.txt`
- New code: `scheduler/google_calendar.py`, `scheduler/signals.py`, `scheduler/apps.py` (updated)
