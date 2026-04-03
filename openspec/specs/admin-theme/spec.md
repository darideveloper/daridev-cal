# admin-theme Specification

## Purpose
TBD - created by archiving change init-daridev-cal-project. Update Purpose after archive.
## Requirements
### Requirement: Modern Admin Layout
The project SHALL use `django-unfold` as the primary admin theme, correctly preserving its layout structure.

#### Scenario: Unfold Layout Preservation
- **Given** I am customizing the admin template
- **When** I extend the admin templates
- **Then** I SHALL use `project/templates/admin/base_site.html` and extend `"admin/base.html"` to ensure Unfold's structural CSS classes are loaded.

### Requirement: Admin Static Assets

The `django-unfold` interface SHALL dynamically reflect the active tenant's branding using callback strings in `settings.py` mapped to functions in `utils.callbacks`. To ensure textual branding (headline) correctly displays, the `SITE_LOGO` option SHALL NOT be declared in `UNFOLD`.

#### Scenario: Dynamic Header and Icon
- **Given** I am rendering the Unfold admin interface
- **When** the `SITE_HEADER` and `SITE_TITLE` config is evaluated
- **Then** they SHALL return the result of `request.tenant.name` from the tenant schema via a callback, and `SITE_LOGO` MUST remain undefined so the text displays.
- **And** `SITE_ICON` SHALL return the URL of `request.tenant.companyprofile.logo` via a callback if a profile and logo exist, otherwise fallback to the default global icon.

#### Scenario: Dynamic Brand Color
- **Given** I am rendering the admin template as a tenant
- **When** a custom `brand_color` is configured in the `CompanyProfile`
- **Then** the global CSS variables `--color-primary-400`, `--color-primary-500`, and `--color-primary-600` MUST be overridden in the template.
- **And** the UI (buttons, active states, markdown highlights) MUST update to reflect this color palette dynamically.

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
The project SHALL provide a base `ModelAdmin` class to standardize Unfold's UI features, and all models SHALL use it.

#### Scenario: Base ModelAdmin Usage across Apps
- **Given** the models defined in `companies` and `scheduler` apps
- **When** they are registered in the admin site
- **Then** their admin classes (`ClientAdmin`, `DomainAdmin`, `CompanyProfileAdmin`, `EventTypeAdmin`, `BookingAdmin`) SHALL inherit from `project.admin.ModelAdminUnfoldBase` rather than the default Unfold `ModelAdmin`.

### Requirement: Admin Sidebar Navigation Update SHALL be applied.
The Admin Sidebar Navigation SHALL be updated.
Update the `UNFOLD['SIDEBAR']['navigation']` to include the new models.

#### Scenario: `UNFOLD` sidebar configuration
- Add `companies.Client` and `companies.Domain` under a "System" group.
- Add `scheduler.EventType` and `scheduler.Booking` under a "Scheduling" group.
- Icons SHALL be assigned: `business` (Client), `link` (Domain), `event_note` (EventType), `calendar_month` (Booking).

### Requirement: Display Language Switcher
The Unfold admin theme MUST display a UI control for switching languages.

#### Scenario: Admin Interface
- **GIVEN** the `UNFOLD` settings dictionary
- **WHEN** an admin page is rendered
- **THEN** the `SHOW_LANGUAGES` key must be set to `True`.
- **AND** the `LANGUAGES` key must be a dictionary containing `navigation` with `name_local` labels to correctly display capitalized language names (e.g., "Español").

### Requirement: Admin Static Assets

The `django-unfold` interface SHALL dynamically reflect the active tenant's branding using callback strings in `settings.py` mapped to functions in `utils.callbacks`. To ensure textual branding (headline) correctly displays, the `SITE_LOGO` option SHALL NOT be declared in `UNFOLD`.

#### Scenario: Dynamic Header and Icon
- **Given** I am rendering the Unfold admin interface
- **When** the `SITE_HEADER` and `SITE_TITLE` config is evaluated
- **Then** they SHALL return the result of `request.tenant.name` from the tenant schema via a callback, and `SITE_LOGO` MUST remain undefined so the text displays.
- **And** `SITE_ICON` SHALL return the URL of `request.tenant.companyprofile.logo` via a callback if a profile and logo exist, otherwise fallback to the default global icon.

#### Scenario: Dynamic Brand Color
- **Given** I am rendering the admin template as a tenant
- **When** a custom `brand_color` is configured in the `CompanyProfile`
- **Then** the global CSS variables `--color-primary-400`, `--color-primary-500`, and `--color-primary-600` MUST be overridden in the template.
- **And** the UI (buttons, active states, markdown highlights) MUST update to reflect this color palette dynamically.

### Requirement: Event Admin Booking Management
The `Event` admin ChangeForm SHALL provide a read-only summary of linked bookings and a direct link to the full filtered `Booking` changelist.

#### Scenario: Read-only Booking Inline
- **Given** an existing `Event` in the admin
- **When** I navigate to the "Bookings" tab
- **Then** the `BookingInline` SHALL display bookings in a read-only format.
- **And** it SHALL NOT allow adding or deleting bookings directly from this inline.

#### Scenario: Link to Full Booking Table
- **Given** an existing `Event` in the admin
- **When** I navigate to the "Bookings" tab
- **Then** a "View All Bookings" button/link SHALL be visible.
- **And** clicking this link SHALL redirect to the `Booking` changelist with the filter `event__id__exact` applied for the current event.

### Requirement: Booking Changelist Filtering
The `Booking` admin changelist SHALL provide robust filtering capabilities to facilitate management.

#### Scenario: Booking Table Filters
- **Given** I am in the `Booking` changelist
- **When** I open the filter sidebar
- **Then** I SHALL see filters for `Event`, `Status`, and a date range filter for `Start Time`.

### Requirement: Styled Booking Inline Actions
The `BookingInline` in the `Event` admin SHALL include a dedicated column for a styled "Manage" button, improving the user interface for booking management.

#### Scenario: Manage Button in Booking Inline
- **Given** an existing `Event` in the admin
- **When** I navigate to the "Bookings" tab
- **Then** the `BookingInline` SHALL display a "Manage" button for each booking record.
- **And** clicking this button SHALL take me to the full edit form for that specific booking.
- **And** the default Django "Change" link SHALL NOT be visible.

