# event-model Specification

## Purpose
TBD - created by archiving change refactor-booking-event-models. Update Purpose after archive.
## Requirements
### Requirement: Create Specific Event Model
A new `Event` model MUST be created to represent a specific, bookable service.

#### Scenario: Create a New Event
- **GIVEN** an administrator wants to add a new service
- **WHEN** they create an `Event` with title "Masterclass: Lifting de Pestañas", link it to the "Masterclass" `EventType`, and provide details like an image, description, price of 150, and duration of 960 minutes
- **THEN** the system saves a new `Event` record.

#### Scenario: Event has a Category
- **GIVEN** an `Event` for "Men's Haircut"
- **WHEN** it is created
- **THEN** it must be associated with an `EventType` category, such as "Hair Services".

