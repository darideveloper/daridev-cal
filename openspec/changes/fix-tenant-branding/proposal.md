# Fix Tenant Branding

The branding logic for each tenant (Company Name, Heading, and Logo) is currently not rendering in the admin interface. This is due to a customized `base_site.html` template that overrides necessary blocks used by `django-unfold` for branding injection.

## Proposed Changes

### 1. Template Fix
Update `project/templates/admin/base_site.html` to include the standard `unfold` blocks for `title` and `branding`. This allows the `UNFOLD` settings (which already point to the correct callbacks) to correctly inject tenant-specific data into the HTML.

### 2. Callback Robustness
Update `utils/callbacks.py` to:
- Use `django_tenants.utils.schema_context` when fetching the `CompanyProfile` to ensure multi-schema queries succeed even if the global context is not correctly set.
- Add error handling for logo URL generation if the profile or image is missing.

## Verification Plan

### Automated Tests
- Test `site_title_callback` and `site_icon_callback` with a mock request containing a valid tenant.
- Verify that `scheduler_companyprofile` is queried within the correct schema context.

### Manual Verification
- Access the admin panel of a specific tenant (e.g., `company1.localhost`) and verify:
    - Browser tab title shows "First Company".
    - Admin header shows "First Company".
    - Admin logo shows the uploaded tenant logo.
