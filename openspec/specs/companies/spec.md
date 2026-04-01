# companies Specification

## Purpose
TBD - created by archiving change register-multi-tenant-models. Update Purpose after archive.
## Requirements
### Requirement: Client (Tenant) Model 
The Client model SHALL be implemented.
The `Client` model represents a tenant in the system. It must inherit from `django_tenants.models.TenantMixin`.

#### Scenario: `Client` model fields
- `schema_name`: `CharField` (unique, max_length=63).
- `name`: `CharField` (max_length=100).
- `created_on`: `DateField` (auto_now_add=True).
- `is_active`: `BooleanField` (default=True).
- `auto_create_schema`: `True`.

### Requirement: Domain Model 
The Domain model SHALL be implemented.
The `Domain` model manages subdomains for each tenant. It must inherit from `django_tenants.models.DomainMixin`.

#### Scenario: `Domain` model relationship
- Links to `Client` (FK).
- `domain`: `CharField` (unique, max_length=253).
- `is_primary`: `BooleanField` (default=True).

### Requirement: Shared Admin Integration
The Shared Admin Integration SHALL be implemented. Register `Client` and `Domain` models with `django-unfold` admin.

#### Scenario: `ClientAdmin` with `TenantAdminMixin`
- Inherit from `TenantAdminMixin` and `project.admin.ModelAdminUnfoldBase`.
- `list_display`: `('schema_name', 'name', 'created_on', 'is_active')`.
- Search fields: `('schema_name', 'name')`.

