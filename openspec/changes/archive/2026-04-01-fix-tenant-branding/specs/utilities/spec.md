## ADDED Requirements

### Requirement: Admin Branding Callbacks
The `utils.callbacks` module SHALL implement tenant-aware callables for `django-unfold` admin branding components: `SITE_HEADER`, `SITE_TITLE`, `SITE_SUBHEADER`, and `SITE_ICON`.

#### Scenario: Tenant Subdomain Resolution
- **Given** I am in `utils/callbacks.py`
- **When** formatting titles, headers, and icons via `site_header_callback` etc.
- **Then** the callbacks SHALL verify `request.tenant` exists and is not the `"public"` schema, return `request.tenant.name` for the titles and headers, exclusively query the `CompanyProfile` for the logo in `site_icon_callback`, and gracefully return fallback values ("DARI DEV CAL", "DARI DEV", "Appointment System", and `static('logo.png')`) for the public domain or exceptions.
