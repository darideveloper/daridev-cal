# spec.md (companies)

## MODIFIED Requirements

### Requirement: Shared Admin Integration
The Shared Admin Integration SHALL be implemented. Register `Client` and `Domain` models with `django-unfold` admin.

#### ADDED Scenario: `Domain` as Inline for `Client`
- **GIVEN** I am in `companies/admin.py`
- **WHEN** I edit a `Client` record
- **THEN** a `DomainInline` SHALL be displayed at the bottom.
- **AND** the inline SHALL be `unfold.admin.TabularInline`.
- **AND** it SHALL allow adding/editing domains for that tenant.
