# Spec Delta: Company Config API

Define the public endpoint for retrieving tenant configuration and branding.

## ADDED Requirements
### Requirement: Public Configuration Endpoint
The system MUST provide a public-facing API endpoint to retrieve the current tenant's branding and settings.

#### Scenario: Fetching Tenant Config
- **Given** a request to `GET /api/config/` with a valid tenant domain.
- **When** the tenant exists and has a `CompanyProfile`.
- **Then** the response MUST return `brand_color`, `logo`, `currency`, `timezone`, `company_name`, `contact_email`, and `contact_phone`.
- **And** the status code should be `200 OK`.
