# label-updates Specification

## Purpose
TBD - created by archiving change update-availability-labels. Update Purpose after archive.
## Requirements
### Requirement: Clear Availability Labels
The `Event` admin MUST use descriptive labels for its availability inlines to distinguish between date ranges and recurring weekly hours.

#### Scenario: Intuitive Tabbed Navigation
- **GIVEN** an administrator is editing an `Event`
- **WHEN** they look at the availability tabs
- **THEN** they see "Date Ranges" for defining seasonal validity.
- **AND** they see "Week Days" for defining recurring weekly slots.

