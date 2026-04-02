# scheduler Specification Delta

## MODIFIED Requirements
### Requirement: Model and Service Localization
The localization requirements for the `Event` model SHALL be updated to remove the redundant `currency` field.

#### MODIFIED Scenario: Translatable Metadata and Choices
- **Given** I am in `scheduler/models.py`
- **When** I check the `Event` model
- **Then** the `currency` field SHALL NOT be present.
- **AND** the localization for `Event.currency` SHALL be removed.

### Requirement: Tenant Admin Integration
The `EventAdmin` SHALL be updated to reflect the removal of the `currency` field.

#### MODIFIED Scenario: Event Management (EventAdmin)
- **GIVEN** an administrator is editing an `Event` in the Unfold Admin
- **WHEN** they view the "General" tab
- **THEN** the `currency` field MUST NOT be displayed.
