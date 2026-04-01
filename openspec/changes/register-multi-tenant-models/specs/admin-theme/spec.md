# Spec Delta: `django-unfold` Admin UI & Dynamic Branding

## MODIFIED Requirements

### Requirement: Admin Sidebar Navigation Update SHALL be applied.
The Admin Sidebar Navigation SHALL be updated.
Update the `UNFOLD['SIDEBAR']['navigation']` to include the new models.

#### Scenario: `UNFOLD` sidebar configuration
- Add `companies.Client` and `companies.Domain` under a "System" group.
- Add `scheduler.EventType` and `scheduler.Booking` under a "Scheduling" group.
- Icons SHALL be assigned: `business` (Client), `link` (Domain), `event_note` (EventType), `calendar_month` (Booking).

### Requirement: Dynamic Tenant Branding SHALL be implemented.
The Admin Sidebar Navigation SHALL be updated.
The `django-unfold` interface SHALL dynamically reflect the active tenant's branding using lambdas in `settings.py`.

#### Scenario: Dynamic Header and Icon
- `SITE_HEADER` SHALL return `request.tenant.name` if `request.tenant` is available.
- `SITE_TITLE` SHALL return `request.tenant.name` if `request.tenant` is available.
- `SITE_ICON` SHALL return the URL of `request.tenant.companyprofile.logo` if a profile and logo exist, otherwise fallback to the default logo.
