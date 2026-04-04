# Proposal: Centralize Google Calendar Credentials

## Why
Currently, every tenant needs to provide their own Google Cloud Service Account credentials (JSON key) to enable calendar synchronization. This is a high-friction onboarding step that requires technical knowledge. Moving to a centralized "Master" account allows the system to provision calendars automatically, improving user experience and centralizing security management.

## What Changes
- [x] Move `google_calendar_credentials` from `CompanyProfile` to global `settings.py`.
- [x] Keep `google_calendar_id` in `CompanyProfile`.
- [x] **BREAKING**: Removed `google_calendar_credentials` from `CompanyProfile` model and Admin.
- [x] Automate the creation of a new Google Calendar for each tenant via signals.
- [x] Automate sharing the tenant's calendar with the tenant's contact email.
- [x] Update synchronization logic to use the centralized master account and handle missing credentials globally.

## Impact
- Affected specs: `sync`, `scheduler`
- Affected code: `scheduler/models.py`, `scheduler/google_calendar.py`, `scheduler/admin.py`, `scheduler/signals.py`, `project/settings.py`
