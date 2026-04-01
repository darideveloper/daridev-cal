# Tasks: Implement Contextual Admin Inlines

## Phase 1: Model Refactor
- [x] Add `ForeignKey` from `BusinessHours` to `CompanyProfile` in `scheduler/models.py`.
- [x] Create and apply migrations for the model change.

## Phase 2: Public Admin Implementation
- [x] Define `DomainInline` in `companies/admin.py`.
- [x] Add `DomainInline` to `ClientAdmin`.

## Phase 3: Tenant Admin Implementation
- [x] Define `BusinessHoursInline` and add it to `CompanyProfileAdmin`.
- [x] Define `EventInline` and add it to `EventTypeAdmin`.
- [x] Define `AvailabilitySlotInline` and add it to `EventAvailabilityAdmin`.
- [x] Define `EventAvailabilityInline` and `BookingInline`.
- [x] Implement **Tabs** in `EventAdmin` (General, Schedule, History).
- [x] Add Image/Logo previews to `Event` and `CompanyProfile` admins.

## Phase 4: Sidebar Cleanup & Navigation
- [x] Unregister/Hide `Domain` from Public Admin sidebar.
- [x] Unregister/Hide `BusinessHours`, `AvailabilitySlot`, and `EventAvailability` from Tenant Admin sidebar.
- [x] Ensure `show_change_link=True` for all relevant inlines.
- [x] Verify `Client` page shows `Domain` inline in Public Admin.
- [x] Verify `CompanyProfile` page shows `BusinessHours` inline in Tenant Admin.
- [x] Verify `EventType` page shows `Event` inline in Tenant Admin.
- [x] Verify `Event` page shows `EventAvailability` and `Booking` inlines in Tenant Admin.
- [x] Verify `EventAvailability` page shows `AvailabilitySlot` inline in Tenant Admin.
