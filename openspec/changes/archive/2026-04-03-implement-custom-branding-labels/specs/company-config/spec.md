## MODIFIED Requirements

### Requirement: Public Configuration Endpoint
The system MUST provide a public-facing API endpoint to retrieve the current tenant's branding and settings.

#### Scenario: Fetching Tenant Config
- **Given** a request to `GET /api/config/` with a valid tenant domain.
- **When** the tenant exists and has a `CompanyProfile`.
- **Then** the response MUST return `brand_color`, `logo`, `currency`, `timezone`, `company_name`, `contact_email`, and `contact_phone`.
- **AND** it MUST also include the customizable UI labels: `event_type_label`, `event_label`, `availability_free_label`, `availability_regular_label`, `availability_no_free_label`, and `extras_label`.
- **AND** the status code should be `200 OK`.
