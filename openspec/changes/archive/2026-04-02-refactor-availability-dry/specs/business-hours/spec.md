# Specification Delta: business-hours

## Why
`BusinessHours` is being refactored into a more powerful, hierarchical system using `CompanyWeekdaySlot` which shares logic with Event-level units.

## MODIFIED Requirements

### Requirement: Define Global Business Hours
The `CompanyProfile` MUST store recurring weekly operating hours using `CompanyWeekdaySlot` which inherits from `BaseAvailabilitySlot`.

#### Scenario: Define Weekly Hours
- **GIVEN** a business owner wants to set their weekly availability
- **WHEN** they create a `CompanyWeekdaySlot` entry
- **THEN** it MUST be associated with the `CompanyProfile` singleton via a `ForeignKey`.
- **AND** the record SHALL store the `weekday`, `start_time`, and `end_time`.
