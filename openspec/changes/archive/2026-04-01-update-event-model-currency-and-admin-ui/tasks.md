# Tasks: Update Event Model Currency and Admin UI

## Phase 1: Model Update
- [x] Rename `format_category` to `currency` in `scheduler/models.py`.
- [x] Add choices (MXN, USD, EUR) to the `currency` field.
- [x] Generate and apply migrations.

## Phase 2: Admin UI Update
- [x] Remove `image_preview` definition from `EventAdmin` in `scheduler/admin.py`.
- [x] Remove `image_preview` from `readonly_fields` in `EventAdmin`.
- [x] Update `tabs` in `EventAdmin` to remove `image_preview` and replace `format_category` with `currency`.

## Phase 3: Validation
- [x] Verify `Event` model has the new `currency` field with choices.
- [x] Verify `Event` admin interface no longer shows image preview.
- [x] Verify `Event` admin interface shows `Currency` field instead of `Format Category`.
