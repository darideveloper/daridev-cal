# admin-theme Specification

## Purpose
TBD - created by archiving change init-daridev-cal-project. Update Purpose after archive.
## Requirements
### Requirement: Modern Admin Layout
The project SHALL use `django-unfold` as the primary admin theme.

#### Scenario: Unfold Integration
- **Given** I am in `project/templates/admin/base.html`
- **When** I extend `unfold/layouts/base.html`
- **Then** it SHALL load the Unfold design system.

### Requirement: Admin Static Assets
The project SHALL enhance Unfold's UI with custom scripts for styling, markdown, and localized filters.

#### Scenario: JS Enhancement Loading
- **Given** I am in `project/templates/admin/base.html`
- **When** I check the `extrahead` block
- **Then** it SHALL include `add_tailwind_styles.js`, `load_markdown.js`, and `range_date_filter_es.js`.

### Requirement: Placeholder Assets
The project SHALL include the brand's logo and favicon.

#### Scenario: Brand Asset Presence
- **Given** I am in `static/`
- **When** I check the assets
- **Then** `logo.png` and `favicon.ico` SHALL be present for branding the admin interface.

### Requirement: User/Group Admin Customization
The Django Admin SHALL be configured to use Unfold's advanced forms and model admin capabilities.

#### Scenario: Custom User Admin
- **Given** I am in `project/admin.py`
- **When** I check the `UserAdmin`
- **Then** it SHALL inherit from `ModelAdminUnfoldBase` and use Unfold's specialized forms.

### Requirement: ModelAdmin Unfold Base
The project SHALL provide a base `ModelAdmin` class to standardize Unfold's UI features.

#### Scenario: Base ModelAdmin Configuration
- **Given** I am in `project/admin.py`
- **When** `ModelAdminUnfoldBase` is implemented
- **Then** it SHALL set `compressed_fields = True`, `warn_unsaved_form = True`, and `actions_row = ["edit"]`.

### Requirement: Admin Sidebar Navigation Update SHALL be applied.
The Admin Sidebar Navigation SHALL be updated.
Update the `UNFOLD['SIDEBAR']['navigation']` to include the new models.

#### Scenario: `UNFOLD` sidebar configuration
- Add `companies.Client` and `companies.Domain` under a "System" group.
- Add `scheduler.EventType` and `scheduler.Booking` under a "Scheduling" group.
- Icons SHALL be assigned: `business` (Client), `link` (Domain), `event_note` (EventType), `calendar_month` (Booking).

### Requirement: Dynamic Tenant Branding SHALL be implemented.
The `django-unfold` interface SHALL dynamically reflect the active tenant's branding using callback strings in `settings.py` mapped to functions in `utils.callbacks`. To ensure textual branding (headline) correctly displays, the `SITE_LOGO` option SHALL NOT be declared in `UNFOLD`.

#### Scenario: Dynamic Header and Icon
- **Given** I am rendering the Unfold admin interface
- **When** the `SITE_HEADER` and `SITE_TITLE` config is evaluated
- **Then** they SHALL return the result of `request.tenant.name` from the tenant schema via a callback, and `SITE_LOGO` MUST remain undefined so the text displays.
- **And** `SITE_ICON` SHALL return the URL of `request.tenant.companyprofile.logo` via a callback if a profile and logo exist, otherwise fallback to the default global icon.

