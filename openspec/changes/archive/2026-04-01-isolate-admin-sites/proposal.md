# Change: Isolate Admin Sites

## Why
When a public domain attempts to access models located entirely within `TENANT_APPS` using a single global admin registry and sidebar, Django throws a `ProgrammingError` because the related tables do not exist in the public schema. The admin experiences must be strictly isolated to avoid misrouting and leaking isolated configuration into global controls.

## What Changes
- Split the monolithic `admin.site` into `PublicAdminSite` and `TenantAdminSite`.
- Create `urls_public.py` to route `/admin` strictly to the `PublicAdminSite`.
- Ensure `urls.py` routes `/admin` strictly to the `TenantAdminSite`.
- Modify `settings.py` to define `PUBLIC_SCHEMA_URLCONF` to enforce domain-specific routing.
- Restrict UNFOLD sidebar items using permission callables so the global items disappear from tenant subdomains, and tenant items disappear from the public domain.
- Create explicit `.register()` patterns across all applications using target instances instead of the global `@admin.register` decorator.

## Impact
- Affected specs: `project-wiring`, `django-settings`
- Affected code: `project/admin.py`, `project/urls.py`, `project/urls_public.py`, `project/settings.py`, and app `admin.py` files.
