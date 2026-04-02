# Proposal: Refine Event Availability and Date Overrides

## Summary
Enhance the recently added `EventDateOverride` model to support custom operating hours for specific dates and consolidate booking validation logic into a single service layer to ensure consistency and maintainability.

## Problem Statement
Currently, `EventDateOverride` can only block or allow a date based on existing weekly slots or business hours. If a business wants to open on a Sunday (usually closed) for a special event with specific hours, the current model cannot support it. Additionally, validation logic is duplicated between `models.py` and `services.py`, creating a maintenance risk.

## Proposed Solution
1.  **Enhance `EventDateOverride` Model**: Add optional `start_time` and `end_time` fields. If provided, these will define the available window for that specific date, bypassing both `EventAvailability` ranges AND `AvailabilitySlot`/`BusinessHours` for that day.
2.  **Consolidate Validation**: Move all availability validation into `scheduler.services.validate_booking_time` and update `Booking.clean` to call this service.
3.  **Update Serializers**: Ensure `EventSerializer` correctly exports the new time fields in `date_overrides`.
4.  **Admin UI Improvements**: Update `EventDateOverrideInline` to include the new time fields.
5.  **Administrative UX Hints**: Add descriptive `help_text` to the models and admin inlines (in English and Spanish) to explain the priority of overrides, ranges, and weekly slots.

## Scope
- `scheduler/models.py`: Update `EventDateOverride` and `Booking.clean`.
- `scheduler/services.py`: Refactor `validate_booking_time` to handle custom override hours.
- `scheduler/serializers.py`: Update `EventDateOverrideSerializer`.
- `scheduler/admin.py`: Update `EventDateOverrideInline`.
- `scheduler/tests.py`: Add test cases for custom override hours.
