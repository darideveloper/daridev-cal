# Tasks: Centralize Google Calendar Credentials

## Preparation
- [x] Research: Confirm Google Cloud Platform (GCP) constraints for number of calendars per service account.
- [x] Configuration: Add `GOOGLE_CALENDAR_CREDENTIALS` (JSON string) and `MASTER_CALENDAR_EMAIL` (for sharing) to `.env` and `settings.py`.

## Model Refactor
- [x] Modification: Remove `google_calendar_credentials` field from `CompanyProfile` in `scheduler/models.py`.
- [x] Migration: Create and run Django migrations for the model changes.

## Service Refactor
- [x] Modification: Update `get_google_calendar_service` in `scheduler/google_calendar.py` to use global credentials instead of tenant-specific ones.
- [x] Logic: Add `create_tenant_calendar` function to programmatically create a new calendar for a tenant.
- [x] Logic: Add `share_calendar_with_client` function to grant `reader` access to the tenant's primary email.
- [x] Logic: Update `sync_booking_to_google` and `delete_google_calendar_event` to use the centralized master credentials.

## Lifecycle Automation
- [x] Signal: Create a new signal `ensure_tenant_google_calendar` in `scheduler/signals.py` that triggers when `CompanyProfile` is saved.
- [x] Validation: Test that new tenants automatically get a calendar ID assigned upon profile creation.

## Spec Updates
- [x] Spec: Update `openspec/specs/sync/spec.md` to reflect the centralized authentication requirement.
- [x] Spec: Update `openspec/specs/scheduler/spec.md` (or relevant profile spec) to reflect the removal of credential fields.

## Validation
- [x] Testing: Create a unit test to verify that the master account creates a calendar and returns a valid ID.
- [x] Testing: Verify that bookings for different tenants sync to their respective (newly created) calendars using the same master account.
- [x] Manual Check: Verify in Google Calendar UI (if possible) that calendars are being created and shared correctly.
