## 1. Multi-Tenant Admin Site Separation
- [x] 1.1 In `project/admin.py`, instantiate `PublicAdminSite(name="admin")` and `TenantAdminSite(name="admin")` (extending `unfold.sites.UnfoldAdminSite`).
- [x] 1.2 In `project/admin.py`, explicitly register `User` and `Group` to `public_admin_site`.
- [x] 1.3 In `companies/admin.py`, explicitly register `Client` and `Domain` to `public_admin_site` (removing `@admin.register`).
- [x] 1.4 In `scheduler/admin.py`, explicitly register `CompanyProfile`, `EventType`, and `Booking` to `tenant_admin_site` (removing `@admin.register`).

## 2. Multi-Tenant URL Routing Isolation
- [x] 2.1 Create `project/urls_public.py` configured with `path("admin/", public_admin_site.urls)` and a root redirect to `/admin/` (including static/media routes in DEBUG).
- [x] 2.2 In `project/urls.py`, remove the default `admin.site.urls` and route `/admin` to `tenant_admin_site.urls`.
- [x] 2.3 In `project/settings.py`, declare `PUBLIC_SCHEMA_URLCONF = "project.urls_public"`.

## 3. Dynamic Sidebar Navigation Resolution
- [x] 3.1 In `project/settings.py`, modify `UNFOLD["SIDEBAR"]["navigation"]` to include a `permission` callable on the system and multi-tenancy items restricting them to `schema_name == "public"`.
- [x] 3.2 In `project/settings.py`, modify `UNFOLD["SIDEBAR"]["navigation"]` to include a `permission` callable on the Booking App items restricting them to `schema_name != "public"`.
