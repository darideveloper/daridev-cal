# Change: Add Tenant Brand Color

## Why
Tenants need the ability to customize the admin interface with their own brand color to provide a consistent and white-labeled experience for their users. Currently, the brand color is globally defined and cannot be overridden per tenant.

## What Changes
- **MODIFIED**: `scheduler.CompanyProfile` model to include a `brand_color` field with `RegexValidator` for OKLCH/HEX formats.
- **MODIFIED**: `scheduler.admin.CompanyProfileAdmin` to use a color picker widget.
- **ADDED**: `utils.callbacks.get_brand_config` helper to centralize brand color resolution and palette derivation (light/main/dark).
- **ADDED**: `project.context_processors.branding` to provide the derived brand palette to all templates.
- **MODIFIED**: `project/templates/admin/base_site.html` to inject the full color palette (400, 500, 600) as CSS variables.
- **MODIFIED**: `static/css/style.css` to use these CSS variables consistently.
- **MODIFIED**: `project/settings.py` to register the context processor and update `UNFOLD` colors.

## Impact
- Affected specs: `specs/scheduler/spec.md`, `specs/admin-theme/spec.md`, `specs/django-settings/spec.md`
- Affected code: `scheduler/models.py`, `scheduler/admin.py`, `utils/callbacks.py`, `project/settings.py`, `project/templates/admin/base_site.html`, `static/css/style.css`
