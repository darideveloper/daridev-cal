# event-model Specification Delta

## MODIFIED Requirements
### Requirement: Create Specific Event Model
The requirement to select a currency during `Event` creation SHALL be removed.

#### MODIFIED Scenario: Create a New Event
- **GIVEN** an administrator wants to add a new service
- **WHEN** they create an `Event` with title "Masterclass: Lifting de Pestañas", link it to the "Masterclass" `EventType`, and provide details like an image, description, price of 150, and duration of 960 minutes.
- **THEN** the system SHALL NOT require a currency selection.
- **AND** the system saves a new `Event` record.
