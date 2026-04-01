# Tasks: Integrate Unfold Admin

## Phase 1: Infrastructure & Callbacks
- [x] Create `utils/callbacks.py` with `environment_callback`.
    - **Validation**: Verify `environment_callback` returns correct labels for "prod", "dev", and "local".

## Phase 2: Configuration & Styling
- [x] Update `INSTALLED_APPS` in `project/settings.py` to include `unfold` and its extensions before `django.contrib.admin`.
    - **Validation**: Check app loading order via `python manage.py check`.
- [x] Add `UNFOLD` settings dictionary to `project/settings.py`.
    - **Validation**: Ensure `UNFOLD` is defined and contains the OKLCH scale for `#87d1ff`, `THEME="light"`, and `SITE_SYMBOL="calendar_today"`.

## Phase 3: Templates & Branding
- [x] Update `project/templates/admin/base.html` to extend `unfold/layouts/base.html` and load custom assets.
    - **Validation**: Open the admin dashboard and confirm visual theme change and logo presence.
- [x] Implement `ModelAdminUnfoldBase` in `project/admin.py`.
    - **Validation**: Ensure `compressed_fields`, `warn_unsaved_form`, and `actions_row` are correctly set.
- [x] Register `User` and `Group` in `project/admin.py` using `unfold.admin.ModelAdmin`.
    - **Validation**: Access "Users" in admin and verify the Unfold layout and password change forms.
