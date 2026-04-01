# Spec: Event Category

## MODIFIED Requirements

### Requirement: Refactor EventType to be a Category
The `EventType` model MUST be simplified to function as a high-level category for events.

#### Scenario: Create a Category
- **GIVEN** an administrator is setting up services
- **WHEN** they create an `EventType` named "Hair Services"
- **AND** provide a description, a "POST-PAID" payment model, and set `allow_overlap` to `false`
- **THEN** the system saves a new `EventType` record.
- **AND** the `duration_minutes` and `price` fields are no longer present on this model.

## REMOVED Requirements

### Requirement: EventType Booking Details
The `EventType` model will no longer store details specific to a single bookable event.

#### Scenario: Redundant Fields
- **GIVEN** the `EventType` model
- **WHEN** a developer inspects the model definition
- **THEN** the `duration_minutes` and `price` fields are not present.
