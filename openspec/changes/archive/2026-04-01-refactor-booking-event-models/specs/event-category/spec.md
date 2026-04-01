# Spec: Event Category

## ADDED Requirements

### Requirement: Event Service Categorization
The `EventType` model MUST function as a high-level category for grouping specific `Event` instances and defining shared metadata.

#### Scenario: Define a Service Category
- **GIVEN** an administrator needs to group different types of "Haircuts"
- **WHEN** they create an `EventType` named "Hair Services"
- **THEN** the system saves the record with the provided `title`, `description`, and `payment_model`.
- **AND** the category-level `allow_overlap` setting is registered successfully.
