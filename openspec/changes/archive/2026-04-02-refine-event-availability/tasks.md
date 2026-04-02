# Tasks: Refine Event Availability

## Implementation
- [x] Add `start_time` and `end_time` fields to `EventDateOverride` model in `scheduler/models.py`.
- [x] Refactor `scheduler/services.py:validate_booking_time` to incorporate custom override hours.
- [x] Update `scheduler/models.py:Booking.clean` to call `validate_booking_time`.
- [x] Update `scheduler/serializers.py:EventDateOverrideSerializer` to include new time fields.
- [x] Update `scheduler/admin.py:EventDateOverrideInline` with new fields and layout.
- [x] Add `help_text` to models and inlines for UX clarifications.
- [x] Add Spanish translations for new fields and help texts in `locale/es/LC_MESSAGES/django.po`.
- [x] Compile translation messages.

## Verification
- [x] Create and run database migrations.
- [x] Add unit tests for `EventDateOverride` with custom hours in `scheduler/tests.py`.
- [x] Add unit tests for `Booking.clean` consolidation in `scheduler/tests.py`.
- [x] Verify that an override with custom hours correctly accepts/rejects bookings.
- [x] Verify that a blocked override (is_available=False) correctly rejects bookings.
