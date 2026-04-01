# Proposal: Full Unfold Integration and Customization

## Description
This change implements a complete integration and visual customization of the `django-unfold` admin theme for the "DARI DEV CAL" appointment system. It focuses on brand alignment using the color `#87d1ff` and professional dashboard layouts.

## Goals
- Integrate `django-unfold` with advanced filters, forms, and inlines.
- Customize the admin UI with the brand color `#87d1ff` using OKLCH scaling.
- Configure the sidebar with the brand logo and specific application navigation.
- Implement an environment callback to display the current stage (Dev/Local/Prod) in the admin header.
- Localize filter placeholders and integrate markdown support in text areas.
- **Added**: Implement `ModelAdminUnfoldBase` for consistent UI behavior across all models.
- **Added**: Enable advanced admin features like history, view on site, and unsaved form warnings.

## Relationships
- **admin-theme**: Updates requirements for the visual layout, static assets, and the new base `ModelAdmin`.
- **django-settings**: Adds comprehensive Unfold configuration including theme and site metadata.
- **utilities**: Adds environment callbacks for the admin interface.
