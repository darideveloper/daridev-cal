## MODIFIED Requirements

### Requirement: Tenant-based Branding Logic
The admin interface MUST display the specific branding (Title, Header, Logo) based on the current active tenant.

#### Scenario: Active Tenant Admin
**Given** a request is made to a tenant-specific admin domain (e.g., `company1.localhost/admin/`)
**When** the page is rendered
**Then** the `<title>` MUST include "First Company" (or the tenant's name)
**AND** the admin sidebar header MUST display the tenant name
**AND** the site logo MUST be the one uploaded to `CompanyProfile` for that tenant.

#### Scenario: Public Admin Branding
**Given** a request is made to the public admin domain (e.g., `localhost/admin/`)
**When** the page is rendered
**Then** the branding MUST default to "DARI DEV CAL" and the default site logo.
