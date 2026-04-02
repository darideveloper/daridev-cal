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

### Requirement: Model Localization
The project SHALL provide translated names for models and fields in the `companies` app.

#### Scenario: Translatable Metadata
- **Given** I am in `companies/models.py`
- **When** I check the `Client` and `Domain` models
- **Then** their `verbose_name` and `verbose_name_plural` SHALL be translatable.
- **AND** their fields SHALL have translatable names and help texts.
- **AND** `Client.schema_name` SHALL have verbose_name = _("tenant ID") and help_text = _("Internal identifier used to isolate data. Must be unique and lowercase.")
- **AND** `Client.name` SHALL have verbose_name = _("company name") and help_text = _("Official display name of the tenant.")
- **AND** `Client.is_active` SHALL have verbose_name = _("active status") and help_text = _("Uncheck to suspend all tenant operations.")
- **AND** `Domain.domain` SHALL have verbose_name = _("web address") and help_text = _("The URL where users will access the booking portal (e.g., tenant.com).")
- **AND** `Domain.is_primary` SHALL have verbose_name = _("primary URL") and help_text = _("If multiple domains exist, this is the main address.")

### Requirement: Shared Admin Integration
The Shared Admin Integration SHALL be implemented. Register `Client` and `Domain` models with `django-unfold` admin.

#### ADDED Scenario: `Domain` as Inline for `Client`
- **GIVEN** I am in `companies/admin.py`
- **WHEN** I edit a `Client` record
- **THEN** a `DomainInline` SHALL be displayed at the bottom.
- **AND** the inline SHALL be `unfold.admin.TabularInline`.
- **AND** it SHALL allow adding/editing domains for that tenant.

