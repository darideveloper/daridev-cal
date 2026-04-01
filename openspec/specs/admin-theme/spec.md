# admin-theme Specification

## Purpose
TBD - created by archiving change init-daridev-cal-project. Update Purpose after archive.
## Requirements
### Requirement: Modern Admin Layout
The project SHALL use a custom base template for the Django Admin to include additional external assets.

#### Scenario: Admin Template Customization
- **Given** I am in `project/templates/admin/base.html`
- **When** I check the `extrahead` block
- **Then** it SHALL load `SimpleMDE` for markdown support and custom project scripts.

### Requirement: Admin Static Assets
The project SHALL include essential static scripts and styles.

#### Scenario: Script Initialization
- **Given** I am in `static/js/`
- **When** I check the scripts
- **Then** `copy_clipboard.js`, `script.js`, `add_tailwind_styles.js`, `load_markdown.js`, and `range_date_filter_es.js` SHALL be present.

### Requirement: Placeholder Assets
The project SHALL include placeholder logo and favicon files.

#### Scenario: Placeholder Presence
- **Given** I am in `static/`
- **When** I check the assets
- **Then** `logo.svg` and `favicon.png` SHALL be present to prevent 404 errors in the admin layout.

### Requirement: User/Group Admin Customization
The Django Admin SHALL be configured for standard model customization.

#### Scenario: Custom User Admin
- **Given** I am in `project/admin.py`
- **When** I check the `UserAdmin`
- **Then** it SHALL use Unfold's forms and `ModelAdmin` for a consistent UI experience.

