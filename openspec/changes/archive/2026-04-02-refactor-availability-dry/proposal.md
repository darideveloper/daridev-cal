# Change: Refactor Availability for DRY Compliance

## Why
The current availability logic is duplicated between `Event` and `CompanyProfile` levels but remains unequal in power. `Event` has ranges and overrides, while `CompanyProfile` only has simple hours. We need to unify these using **Abstract Model Inheritance** to ensure a single, powerful validation engine for all bookable entities.

## What Changes
- [x] Create abstract base models for Ranges, Slots, and Overrides in `scheduler/models.py`.
- [x] Refactor `EventAvailability`, `AvailabilitySlot`, and `EventDateOverride` to inherit from these bases.
- [x] Implement **BREAKING** schema changes by adding `CompanyAvailability`, `CompanyWeekdaySlot`, and `CompanyDateOverride`.
- [x] Refactor `validate_booking_time` service to handle hierarchical Provider-Entity levels.
- [x] Update the Admin UI to include new company-level availability inlines.

## Impact
- Affected specs: `event-availability`, `availability-slot`, `date-override`, `business-hours`, `validation-logic`, `company-profile-updates`
- Affected code: `scheduler/models.py`, `scheduler/services.py`, `scheduler/admin.py`
