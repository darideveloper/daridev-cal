# admin-theme Specification Delta

## MODIFIED Requirements

### Requirement: Modern Admin Layout
The project SHALL use `django-unfold` as the primary admin theme, correctly preserving its layout structure.

#### Scenario: Unfold Layout Preservation
- **Given** I am customizing the admin template
- **When** I extend the admin templates
- **Then** I SHALL use `project/templates/admin/base_site.html` and extend `"admin/base.html"` to ensure Unfold's structural CSS classes are loaded.

### Requirement: Admin Static Assets
The project SHALL enhance Unfold's UI with custom scripts for styling, markdown, and localized filters.

#### Scenario: JS Enhancement Loading
- **Given** I am in `project/templates/admin/base_site.html`
- **When** I check the `extrahead` block
- **Then** it SHALL include `add_tailwind_styles.js`, `load_markdown.js`, and `range_date_filter_es.js`.
- **And** the file `static/js/add_tailwind_styles.js` SHALL exist and apply Tailwind classes to `.btn` and `.img-preview` elements.

### Requirement: ModelAdmin Unfold Base
The project SHALL provide a base `ModelAdmin` class to standardize Unfold's UI features, and all models SHALL use it.

#### Scenario: Base ModelAdmin Usage across Apps
- **Given** the models defined in `companies` and `scheduler` apps
- **When** they are registered in the admin site
- **Then** their admin classes (`ClientAdmin`, `DomainAdmin`, `CompanyProfileAdmin`, `EventTypeAdmin`, `BookingAdmin`) SHALL inherit from `project.admin.ModelAdminUnfoldBase` rather than the default Unfold `ModelAdmin`.
