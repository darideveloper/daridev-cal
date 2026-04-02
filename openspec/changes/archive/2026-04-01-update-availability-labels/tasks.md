# Tasks: Update Availability Inline Labels for Clarity

- [x] Update `scheduler/models.py`:
    - [x] `EventAvailability.Meta`: `verbose_name = _("Date Range")`, `verbose_name_plural = _("Date Ranges")`.
    - [x] `AvailabilitySlot.Meta`: `verbose_name = _("Week Day")`, `verbose_name_plural = _("Week Days")`.
- [x] Update `scheduler/admin.py`:
    - [x] Ensure `EventAdmin` tabs are correctly labeled if they don't use model `verbose_name` by default.
- [x] Create and run migration: `python manage.py makemigrations scheduler && python manage.py migrate scheduler`.
- [x] Verify labels in admin UI.
