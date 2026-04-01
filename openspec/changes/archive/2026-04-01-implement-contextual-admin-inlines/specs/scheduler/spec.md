# spec.md (scheduler)

## MODIFIED Requirements

### Requirement: Tenant Admin Integration
The Tenant Admin Integration SHALL be implemented. Register models with `django-unfold`.

#### ADDED Scenario: Service Hub (EventAdmin)
- **GIVEN** I am in `scheduler/admin.py`
- **WHEN** I edit an `Event` record
- **THEN** the interface SHALL use **Tabs** to separate "General", "Schedule", and "History".
- **AND** an `EventAvailabilityInline` SHALL be displayed in the "Schedule" tab.
- **AND** a read-only `BookingInline` SHALL be displayed in the "History" tab.
- **AND** a small image preview of the service image SHALL be displayed.

#### ADDED Scenario: Settings Hub (CompanyProfileAdmin)
- **GIVEN** I am in `scheduler/admin.py`
- **WHEN** I edit the `CompanyProfile` singleton
- **THEN** a `BusinessHoursInline` SHALL be displayed to manage global office hours.
- **AND** a small image preview of the tenant logo SHALL be displayed.

#### ADDED Scenario: Admin Navigation Cleanup
- **GIVEN** the admin sidebar is rendered
- **WHEN** the `Contextual Inlines` are active
- **THEN** child models (`BusinessHours`, `AvailabilitySlot`, `EventAvailability`) SHOULD NOT be displayed in the sidebar menu.
- **AND** `Domain` SHOULD NOT be displayed in the Public Admin sidebar.
