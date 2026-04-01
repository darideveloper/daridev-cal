# scheduler Specification Delta

## MODIFIED Requirements

### Requirement: Tenant Admin Integration
The Tenant Admin Integration SHALL be implemented. Register models with `django-unfold`.

#### Scenario: Admin Classes Inheritance
- Inherit from `project.admin.ModelAdminUnfoldBase` for all model admin classes in the `scheduler` app (`CompanyProfileAdmin`, `EventTypeAdmin`, `BookingAdmin`).
