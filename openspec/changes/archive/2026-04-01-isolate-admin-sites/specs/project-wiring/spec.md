## MODIFIED Requirements
### Requirement: URL Configuration
The project's URLs SHALL be correctly configured to include the Django Admin and a REST API router, strictly separating public and tenant endpoints to avoid database overlap errors.

#### Scenario: Global URLs
- **Given** I am in `project/urls_public.py`
- **When** I check the `urlpatterns`
- **Then** the `admin/` route SHALL map to `PublicAdminSite`.
- **And** the root redirect to admin SHALL be mapped accurately.

#### Scenario: Tenant URLs
- **Given** I am in `project/urls.py`
- **When** I check the `urlpatterns`
- **Then** the `admin/` route SHALL map to `TenantAdminSite`.
- **And** the `api/` route SHALL map to the REST API router.
