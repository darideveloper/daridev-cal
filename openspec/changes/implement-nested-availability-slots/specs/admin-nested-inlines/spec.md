# admin-nested-inlines Specification

## Requirements
### Requirement: Unified Event Setup Workflow
The `Event` admin MUST provide a clear path to manage `EventAvailability` rules and their associated `AvailabilitySlot` records using a nested navigation workflow.

#### Scenario: Navigating from Event to Slots
- **GIVEN** an administrator is editing an `Event`
- **WHEN** they view the "Availability" tab
- **AND** they click "Change" on an `EventAvailability` rule
- **THEN** they are directed to the `EventAvailability` edit page.
- **AND** they can directly manage (add/edit/delete) multiple `AvailabilitySlot` records on that page.
- **AND** saving that page returns them to the `EventAvailability` list or the rule itself.
