# Specification Delta: validation-logic

## Why
Validation logic MUST be hierarchical to check Provider (Company) rules if Entity (Event) rules do not explicitly allow/deny a booking slot.

## MODIFIED Requirements

### Requirement: Priority-Based Availability Matrix
The system MUST follow a strict priority when checking availability: Event Overrides > Event Slots > Event Ranges > Company Overrides > Company Slots > Company Ranges.

#### Scenario: Company Override Blocks All
- **GIVEN** `CompanyDateOverride` is set to `is_available=False` for Dec 25th
- **WHEN** a booking is requested for Dec 25th at 10 AM
- **THEN** the system MUST reject the booking even if the `Event` has a valid range or slot for that date.

#### Scenario: Event Slot Overrides Company Slot
- **GIVEN** Company is open 09:00-17:00 on Mondays
- **AND** `Event` has a specific `AvailabilitySlot` for 10:00-11:00 on Mondays
- **WHEN** booking is requested for 14:00 on Monday
- **THEN** the system MUST reject it as the Event slot has priority over the global business hours.
