# companies Specification Delta

## MODIFIED Requirements

### Requirement: Shared Admin Integration
The Shared Admin Integration SHALL be implemented. Register `Client` and `Domain` models with `django-unfold` admin.

#### Scenario: `ClientAdmin` with `TenantAdminMixin`
- Inherit from `TenantAdminMixin` and `project.admin.ModelAdminUnfoldBase`.
- `list_display`: `('schema_name', 'name', 'created_on', 'is_active')`.
- Search fields: `('schema_name', 'name')`.
