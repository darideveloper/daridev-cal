# Tasks: Remove Logo Preview from Company Profile Admin

## Phase 1: Implementation
- [x] Remove `logo_preview` method from `CompanyProfileAdmin` in `scheduler/admin.py`.
- [x] Remove `readonly_fields = ("logo_preview",)` from `CompanyProfileAdmin`.

## Phase 2: Validation
- [x] Verify `CompanyProfile` change form no longer displays the logo preview.
