# Change: Fix Tenant Branding

## Why
Currently, the `django-unfold` configuration sets `SITE_LOGO`, which entirely replaces the textual brand name and headline across all domains (public and tenant). Unfold's template logic exclusively prioritizes the `SITE_LOGO` image, hiding all header texts. Additionally, the fallback branding values (`SITE_HEADER`, `SITE_TITLE`, and `SITE_SUBHEADER`) are hardcoded static strings ("DARI DEV CAL", etc.) instead of tenant-aware callables, preventing proper multi-tenant dynamic branding.

## What Changes
- **Remove `SITE_LOGO`:** Remove `SITE_LOGO` from `UNFOLD` settings so Unfold uses `site_icon.html`, displaying both the logo image (`SITE_ICON`) and the header text (`SITE_HEADER`).
- **Dynamic Callbacks:** Modify `SITE_TITLE`, `SITE_HEADER`, `SITE_SUBHEADER`, and `SITE_ICON` to point to functions in `utils/callbacks.py`.
- **Tenant Context:** Implement `site_title_callback`, `site_header_callback`, `site_subheader_callback`, and `site_icon_callback` safely in `utils/callbacks.py` to interact with `django-tenants` context via `request.tenant` without causing import or database errors on the public schema.

## Impact
- **Affected specs:** `admin-theme`, `utilities`
- **Affected code:** `project/settings.py`, `utils/callbacks.py`
