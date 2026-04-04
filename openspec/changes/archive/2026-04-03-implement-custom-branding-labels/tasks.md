# Tasks: Implement Customizable UI Labels in Company Profile

## Task List

- [x] **Data Model Updates**
  - [x] Add `event_type_label`, `event_label`, `availability_free_label`, `availability_regular_label`, `availability_no_free_label`, and `extras_label` to `CompanyProfile` model in `scheduler/models.py`.
  - [x] Run `python manage.py makemigrations scheduler` and `python manage.py migrate`.
- [x] **API Implementation**
  - [x] Add new fields to `CompanyConfigSerializer` in `scheduler/serializers.py`.
  - [x] Update `CompanyConfigView.get()` to include these fields in its response in `scheduler/views.py`.
- [x] **Admin UI**
  - [x] Add the "UI Labels" tab with new fields to `CompanyProfileAdmin` in `scheduler/admin.py`.
- [x] **Documentation**
  - [x] Update `docs/api.md` with the new fields in `GET /config/`.
- [x] **Validation**
  - [x] Verify the fields are visible and functional in the Admin UI.
  - [x] Verify the `GET /api/config/` response includes the new fields.
  - [x] Verify translations are picked up.
