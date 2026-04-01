# spec.md (scheduler)

## MODIFIED Requirements

### Requirement: Tenant Admin Integration
The Tenant Admin Integration SHALL be implemented. Register models with `django-unfold`.

#### MODIFIED Scenario: Service Hub (EventAdmin)
- **GIVEN** I am in `scheduler/admin.py`
- **WHEN** I edit an `Event` record
- **THEN** an `image_preview` SHALL NOT be displayed.
- **AND** the "General" tab SHALL display a `currency` choice field instead of `format_category`.
