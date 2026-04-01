# Tasks

## Phase 1: Custom Scripts and Templates
- [x] Create `static/js/add_tailwind_styles.js` with the content provided in the `docs/unfold.md` guide.
- [x] Rename `project/templates/admin/base.html` to `project/templates/admin/base_site.html`.
- [x] Update `project/templates/admin/base_site.html` to extend `"admin/base.html"` instead of `"unfold/layouts/base.html"`.
- [x] Update `project/templates/admin/base_site.html` to include the script tag for `add_tailwind_styles.js` after the `simplemde` imports.

## Phase 2: Base Class Inheritance in Admin Models
- [x] In `companies/admin.py`, replace the import of `ModelAdmin` from `unfold.admin` with `ModelAdminUnfoldBase` from `project.admin`, and update `ClientAdmin` and `DomainAdmin` to inherit from it.
- [x] In `scheduler/admin.py`, replace the import of `ModelAdmin` from `unfold.admin` with `ModelAdminUnfoldBase` from `project.admin`, and update `CompanyProfileAdmin`, `EventTypeAdmin`, and `BookingAdmin` to inherit from it.
