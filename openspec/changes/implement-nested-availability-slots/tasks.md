# Tasks: Streamline Event Availability Management in Admin

- [ ] Update `EventAvailabilityInline` in `scheduler/admin.py`:
    - [ ] Set `show_change_link = True`.
    - [ ] Ensure `tab = True` is set.
- [ ] Uncomment or register `EventAvailabilityAdmin` in `scheduler/admin.py`:
    - [ ] Ensure `AvailabilitySlotInline` is included in its `inlines` list.
    - [ ] Add `tenant_admin_site.register(EventAvailability, EventAvailabilityAdmin)`.
- [ ] Update `EventAdmin` in `scheduler/admin.py`:
    - [ ] Review the `tabs` definition to ensure `EventAvailabilityInline` is correctly mapped to a tab.
- [ ] Validate the administrative workflow:
    - [ ] Navigate to an `Event`.
    - [ ] Go to the "Schedule/Availability" tab.
    - [ ] Click "Change" on an `EventAvailability` rule.
    - [ ] Verify that `AvailabilitySlot` records are editable on that page.
