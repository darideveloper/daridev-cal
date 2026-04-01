# Spec: Booking Logic

## ADDED Requirements

### Requirement: Link Booking to a Specific Event
The `Booking` model MUST be directly associated with a specific `Event`, not a general `EventType`.

#### Scenario: Create a Booking
- **GIVEN** a client wants to book a "Men's Haircut"
- **WHEN** they select a valid time slot for that specific `Event`
- **THEN** the system creates a `Booking` record with a foreign key pointing to the "Men's Haircut" `Event` record.

### Requirement: Calculate Booking End Time from Event Duration
The `end_time` of a booking MUST be automatically calculated based on the duration of the specific `Event`.

#### Scenario: End Time Calculation
- **GIVEN** a booking is made for an `Event` that has a `duration_minutes` of 45
- **WHEN** the booking's `start_time` is set to "10:00"
- **THEN** the system automatically sets the booking's `end_time` to "10:45" upon saving.

### Requirement: Validate Bookings Against Availability Rules
The system MUST validate any new or modified booking against the new hierarchical availability rules.

#### Scenario: Booking Violates Specific Availability
- **GIVEN** an `Event` has an `EventAvailability` rule making it available only on Mondays
- **WHEN** a client attempts to book this event on a Tuesday
- **THEN** the system rejects the booking with a validation error.

#### Scenario: Booking Obeys Specific Availability
- **GIVEN** an `Event` has an `EventAvailability` rule making it available only on Mondays from 09:00 to 12:00
- **WHEN** a client attempts to book this event on a Monday at 10:00
- **THEN** the booking is accepted (assuming no overlaps).

#### Scenario: Booking Falls Back to Global Business Hours
- **GIVEN** an `Event` has no `EventAvailability` rules
- **AND** the company's `BusinessHours` are "09:00" to "17:00"
- **WHEN** a client attempts to book this event at 18:00
- **THEN** the system rejects the booking with a validation error.
