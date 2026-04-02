# spec.md

## ADDED Requirements

### Requirement: Consolidate Availability Validation Logic
Booking validation logic MUST be centralized in `scheduler.services.validate_booking_time`.

#### Scenario: Unified Validation Result
- **GIVEN** a booking attempt is made for an event with a date override
- **WHEN** `Booking.clean()` is called in `models.py`
- **THEN** it MUST invoke `validate_booking_time()` to determine availability.
- **AND** any validation error raised by the service MUST be propagated as a `ValidationError`.

### Requirement: Priority-Based Availability Matrix
The system MUST follow a strict priority when checking availability: Override > Range > Weekly Pattern > Business Hours.

#### Scenario: Override vs. Range
- **GIVEN** an event has a blocked override for a date within its valid range
- **WHEN** a booking is requested for that date
- **THEN** the system MUST reject the booking.
