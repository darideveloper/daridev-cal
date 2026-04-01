# spec.md (event-model)

## MODIFIED Requirements

### Requirement: Create Specific Event Model
A new `Event` model MUST be created to represent a specific, bookable service.

#### MODIFIED Scenario: Create a New Event
- **GIVEN** an administrator wants to add a new service
- **WHEN** they create an `Event` with title "Masterclass: Lifting de Pestañas", link it to the "Masterclass" `EventType`, and provide details like an image, description, price of 150, and duration of 960 minutes.
- **AND** they select a **currency** from the allowed list: `MXN`, `USD`, `EUR`.
- **THEN** the system saves a new `Event` record.
