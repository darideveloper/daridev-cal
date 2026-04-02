# Specification Delta: date-override

## Why
Date overrides MUST share an abstract model `BaseDateOverride` to ensure consistent handling of exceptions at both Entity (Event) and Provider (Company) levels.

## MODIFIED Requirements

### Requirement: Event Date Overrides MUST support custom hours
`EventDateOverride` MUST inherit from `BaseDateOverride` and optionally include `start_time` and `end_time` to override standard weekly slots.

#### Scenario: Blocked Override
- **GIVEN** an event is normally available on Monday, April 6th
- **WHEN** an `EventDateOverride` is created for April 6th with `is_available=False`
- **THEN** all booking attempts for that date MUST be rejected.

#### Scenario: Custom Hours Override (Special Day)
- **GIVEN** an event is normally CLOSED on Sunday, April 12th
- **WHEN** an `EventDateOverride` is created for April 12th with `is_available=True`
- **AND** `start_time` is set to "10:00" and `end_time` is set to "14:00"
- **THEN** a booking for 11:00 MUST be accepted.
- **AND** a booking for 15:00 MUST be rejected.

#### Scenario: Forced Range Override (No custom hours)
- **GIVEN** an event is outside its normal range on Monday, April 20th
- **WHEN** an `EventDateOverride` is created for April 20th with `is_available=True`
- **AND** NO custom hours are provided
- **THEN** a booking for 10:00 MUST be accepted if it matches normal weekly slots.
