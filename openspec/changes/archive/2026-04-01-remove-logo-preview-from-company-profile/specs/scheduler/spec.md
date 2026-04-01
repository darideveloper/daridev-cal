# spec.md (scheduler)

## MODIFIED Requirements

### Requirement: Tenant Admin Integration
The Tenant Admin Integration SHALL be implemented. Register models with `django-unfold`.

#### MODIFIED Scenario: Settings Hub (CompanyProfileAdmin)
- **GIVEN** I am in `scheduler/admin.py`
- **WHEN** I edit the `CompanyProfile` singleton
- **THEN** a `logo_preview` SHALL NOT be displayed.
