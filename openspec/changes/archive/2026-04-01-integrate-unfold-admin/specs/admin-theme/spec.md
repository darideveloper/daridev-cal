# admin-theme Specification Delta

## ADDED Requirements
### Requirement: ModelAdmin Unfold Base
The project SHALL provide a base `ModelAdmin` class to standardize Unfold's UI features.

#### Scenario: Base ModelAdmin Configuration
- **Given** I am in `project/admin.py`
- **When** `ModelAdminUnfoldBase` is implemented
- **Then** it SHALL set `compressed_fields = True`, `warn_unsaved_form = True`, and `actions_row = ["edit"]`.

## MODIFIED Requirements
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
