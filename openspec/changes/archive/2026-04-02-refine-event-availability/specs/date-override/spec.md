# spec.md

## ADDED Requirements

### Requirement: Event Date Overrides MUST support custom hours
`EventDateOverride` MUST optionally include `start_time` and `end_time` to define specific hours for a single date.

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

### Requirement: Admin UI MUST provide hierarchy clarifications
The Django admin MUST display `help_text` in both English and Spanish that explains the priority relationship between overrides, ranges, and slots.

#### Scenario: User clarifies priority in Spanish
- **GIVEN** an administrator is viewing an Event in Spanish
- **WHEN** they look at the `Date Overrides` section
- **THEN** they MUST see a text explaining that it has maximum priority ("máxima prioridad").
