# Spec: Business Hours

## ADDED Requirements

### Requirement: Define Global Business Hours
A new model, `BusinessHours`, MUST be created to store the default weekly operating hours for a business.

#### Scenario: Define Weekly Hours
- **GIVEN** a business owner wants to set their weekly availability
- **WHEN** they create a `BusinessHours` entry for "Monday" with a start time of "09:00" and an end time of "17:00"
- **THEN** the system stores this as a new record.

#### Scenario: Booking Check Fallback
- **GIVEN** an event has no specific availability rules
- **AND** a client attempts to book it on a Monday at 08:00
- **WHEN** the system validates the booking
- **THEN** the booking is rejected because it falls outside the global `BusinessHours`.
