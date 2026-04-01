# Spec: Event Availability

## ADDED Requirements

### Requirement: Define Optional, Granular Event Availability
A new `EventAvailability` model MUST be created to define specific, optional availability rules for an `Event`.

#### Scenario: Availability by Date Range Only
- **GIVEN** an event is only available for a specific week
- **WHEN** an `EventAvailability` record is created for that event with a `start_date` of "2024-08-05" and an `end_date` of "2024-08-11"
- **AND** all weekly time slots are left empty (null)
- **THEN** the event can be booked at any time of day, but only on dates within that range.

#### Scenario: Availability by Weekly Time Only
- **GIVEN** an event is only available on Monday mornings
- **WHEN** an `EventAvailability` record is created for that event with `monday_start_time` of "09:00" and `monday_end_time` of "12:00"
- **AND** the `start_date` and `end_date` are left empty (null)
- **THEN** the event can be booked on any Monday, but only between 9 AM and 12 PM.

#### Scenario: Availability by Date Range and Weekly Time
- **GIVEN** a special course runs for two weeks in July, only on Tuesdays and Thursdays in the afternoon
- **WHEN** an `EventAvailability` record is created with a `start_date` of "2024-07-15" and `end_date` of "2024-07-26"
- **AND** `tuesday_start_time` and `thursday_start_time` are set to "14:00"
- **AND** `tuesday_end_time` and `thursday_end_time` are set to "18:00"
- **THEN** a booking request for Wednesday, July 17th at 3 PM is rejected.
- **AND** a booking request for Tuesday, July 16th at 3 PM is accepted.
