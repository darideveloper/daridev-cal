# Tasks

- [x] **Remove `SITE_LOGO` from `UNFOLD` settings**
  - In `project/settings.py`, remove the `"SITE_LOGO"` key inside the `UNFOLD` dictionary to re-enable text display for Unfold.
- [x] **Update textual branding callbacks in `UNFOLD`**
  - Set `"SITE_TITLE": "utils.callbacks.site_title_callback"`.
  - Set `"SITE_HEADER": "utils.callbacks.site_header_callback"`.
  - Set `"SITE_SUBHEADER": "utils.callbacks.site_subheader_callback"`.
  - Set `"SITE_ICON": "utils.callbacks.site_icon_callback"`.
- [x] **Implement Branding Callbacks in `utils/callbacks.py`**
  - Create a helper `get_tenant_profile(request)` to fetch `CompanyProfile` securely using a local import (e.g. `from scheduler.models import CompanyProfile`) after verifying `hasattr(request, "tenant")` and `request.tenant.schema_name != "public"`.
  - Implement `site_title_callback(request)` returning `request.tenant.name` if tenant is available and not public, or default "DARI DEV CAL".
  - Implement `site_header_callback(request)` returning `request.tenant.name` if tenant is available and not public, or default "DARI DEV".
  - Implement `site_subheader_callback(request)` returning `request.get_host()` or a default "Appointment System".
  - Implement `site_icon_callback(request)` returning the URL of the `CompanyProfile`'s custom logo if available, or default static `logo.png`.
- [x] **Validate tenant integration**
  - Restart the server and visit the tenant subdomain admin `/admin/` to verify the brand name updates based on `request.tenant`.
  - Assure the public domain continues displaying "DARI DEV".
