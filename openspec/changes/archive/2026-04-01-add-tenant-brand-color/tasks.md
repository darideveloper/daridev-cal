## 1. Implementation
- [x] 1.1 Add `brand_color` CharField to `scheduler.CompanyProfile` with `RegexValidator` for OKLCH/HEX (default: current OKLCH color).
- [x] 1.2 Update `scheduler.admin.CompanyProfileAdmin` to use `TextInput(attrs={'type': 'color'})` for the `brand_color`.
- [x] 1.3 Generate and run migrations for tenant schemas (`python manage.py makemigrations` and `python manage.py migrate_schemas`).
- [x] 1.4 Create `utils.callbacks.get_brand_config` to resolve the tenant's brand color into light, main, and dark shades.
- [x] 1.5 Implement `project.context_processors.branding` calling `get_brand_config` and register it in `settings.py`.
- [x] 1.6 Update `UNFOLD['COLORS']['primary']` in `project/settings.py` (shades 400, 500, 600) to reference the CSS variables.
- [x] 1.7 Update `project/templates/admin/base_site.html` to inject a `<style>` block for `--color-primary-400`, `--color-primary-500`, and `--color-primary-600`.
- [x] 1.8 Refactor `static/css/style.css` to use these CSS variables.

## 2. Validation
- [x] 2.1 Verify that the public admin retains the default brand color.
- [x] 2.2 Verify that a tenant with a custom `brand_color` displays that color across the admin interface (buttons, links, active sidebar items).
- [x] 2.3 Verify that the Markdown editor accents in the tenant admin also reflect the custom brand color.
