# direct-availability Specification

## Purpose
TBD - created by archiving change refactor-direct-event-availability. Update Purpose after archive.
## Requirements
### Requirement: Matrix Availability Management
The `Event` admin MUST provide a unified interface to manage multiple active date ranges and a single unified set of weekly hours.

#### Scenario: Defining Intermittent Event Availability
- **GIVEN** an administrator is editing an `Event`
- **WHEN** they define two `EventAvailability` date ranges (Jan-Feb, Apr-May)
- **AND** they define a single set of `AvailabilitySlot` weekly hours (Mon 9-5)
- **THEN** the event is only bookable on Mondays from 9 to 5 during Jan, Feb, Apr, and May.
- **AND** the administrator manages both the dates and the hours in separate inlines on the same `Event` page.

