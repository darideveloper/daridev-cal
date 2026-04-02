# Specification Delta: availability-slot

## Why
`AvailabilitySlot` needs to inherit from a unified `BaseAvailabilitySlot` abstract model to share its time-based logic with company-level slots.

## MODIFIED Requirements

### Requirement: Independent Time Windows
The system MUST support multiple non-overlapping time windows on a single weekday by having `AvailabilitySlot` inherit from `BaseAvailabilitySlot`.

#### Scenario: Morning and Afternoon Slots
- **GIVEN** an event is available from 09:00 to 11:00 and 14:00 to 16:00 on Mondays
- **WHEN** the system stores these as two separate `AvailabilitySlot` records
- **THEN** it validates bookings for 10:00 (Valid) and 15:00 (Valid) but rejects 12:00 (Invalid).
