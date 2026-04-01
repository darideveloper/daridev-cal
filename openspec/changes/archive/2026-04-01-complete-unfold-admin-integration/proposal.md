# Proposal: Complete Unfold Admin Integration

## Goal
To apply the remaining missing pieces of the `django-unfold` integration as specified in the project documentation (`docs/unfold.md`). This includes adding missing custom scripts and ensuring all registered admin models use the centralized base class `ModelAdminUnfoldBase` for a consistent UI experience.

## Context
A review of the current implementation against the integration guide revealed that:
1. The custom script `static/js/add_tailwind_styles.js` is missing.
2. The template `project/templates/admin/base.html` is missing the import of that script.
3. The custom `project/templates/admin/base.html` overrides the Unfold layout in a way that drops its CSS classes (like `@container px-4 pb-4 grow`) by extending `unfold/layouts/base.html`.
4. ModelAdmin classes in `companies/admin.py` and `scheduler/admin.py` inherit from `unfold.admin.ModelAdmin` directly instead of the project-specific `project.admin.ModelAdminUnfoldBase`.

## Scope
- **Added**: Create `static/js/add_tailwind_styles.js`.
- **Modified**: Rename `project/templates/admin/base.html` to `project/templates/admin/base_site.html` and update it to extend `"admin/base.html"` instead to restore the Unfold layout classes.
- **Modified**: Update the newly renamed `project/templates/admin/base_site.html` to include the `add_tailwind_styles.js` script.
- **Modified**: Update `companies/admin.py` so `ClientAdmin` and `DomainAdmin` inherit from `project.admin.ModelAdminUnfoldBase`.
- **Modified**: Update `scheduler/admin.py` so `CompanyProfileAdmin`, `EventTypeAdmin`, and `BookingAdmin` inherit from `project.admin.ModelAdminUnfoldBase`.

## Alternatives Considered
- **No-op:** Leave models inheriting from the base Unfold ModelAdmin. This was rejected because `ModelAdminUnfoldBase` applies project-wide admin settings (e.g. `compressed_fields=True`, row actions).
