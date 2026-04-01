# spec.md (scheduler)

## MODIFIED Requirements

### Requirement: Tenant Admin Integration
The Tenant Admin Integration SHALL be implemented. Register models with `django-unfold`.

#### REMOVED Scenario: Category Hub (EventTypeAdmin)
- **GIVEN** I am in `scheduler/admin.py`
- **WHEN** I edit an `EventType` record
- **THEN** an `EventInline` SHALL NOT be displayed.
