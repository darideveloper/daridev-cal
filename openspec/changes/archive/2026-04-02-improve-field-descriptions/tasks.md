# Tasks: Improved i18n and Field Descriptions

- [x] 1. **Update `companies/models.py` Labels**
    - [x] Update `Client` and `Domain` labels with `gettext_lazy`.
    - [x] Add `help_text` to `schema_name` explaining its role in the URL.
- [x] 2. **Update `scheduler/models.py` Labels**
    - [x] Add descriptive `help_text` for `CompanyProfile` fields (Stripe, OKLCH).
    - [x] Update `EventType`, `Event`, and `Booking` fields with more descriptive names.
    - [x] Improve labels for `BusinessHours` and `AvailabilitySlot` to clarify "Operating Hours" vs "Bookable Slots".
- [x] 3. **Validation & i18n Sync**
    - [x] Run `python manage.py makemessages -l es` to sync strings.
    - [x] Update `locale/es/LC_MESSAGES/django.po` with improved Spanish translations.
    - [x] Compile messages with `python manage.py compilemessages`.
- [x] 4. **Admin UI Review**
    - [x] Verify that all labels and help texts appear correctly in the Public and Tenant admin sites.
