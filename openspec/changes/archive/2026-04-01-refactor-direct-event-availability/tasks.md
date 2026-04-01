# Tasks: Refactor to Matrix Event Availability (Option C)

## Model Refactor
- [x] Update `AvailabilitySlot` in `scheduler/models.py`:
    - [x] Add `event = ForeignKey(Event, related_name="availability_slots", ...)` as nullable initially.
- [x] Create and run migration: `python manage.py makemigrations scheduler && python manage.py migrate`.
- [x] Create a custom data migration to link `AvailabilitySlot` records directly to the `Event` via their parent `EventAvailability`.
- [x] Cleanup `AvailabilitySlot` in `scheduler/models.py`:
    - [x] Remove `event_availability` ForeignKey.
    - [x] Make `event` ForeignKey non-nullable.
- [x] **Logic Update**: Update `Booking.clean()` in `scheduler/models.py` to use the new Matrix logic:
    - [x] Date must fall within an `availability_rules` range (if any exist).
    - [x] Time/Weekday must match an `availability_slots` record.
- [x] Run cleanup migrations.

## Admin Refactor
- [x] Update `EventAvailabilityInline` in `scheduler/admin.py`:
    - [x] Switch to `TabularInline` for compactness.
- [x] Update `AvailabilitySlotInline` in `scheduler/admin.py`:
    - [x] Set `model = AvailabilitySlot`.
    - [x] Switch to `TabularInline`.
- [x] Update `EventAdmin` in `scheduler/admin.py`:
    - [x] Update `inlines` to include both `EventAvailabilityInline` and `AvailabilitySlotInline`.
    - [x] Update `tabs` definition to include both inlines in the "Schedule" tab.

## Validation
- [x] Verify "Matrix" overlap check: Ensure bookings are rejected if they fall outside active date ranges.
- [x] Verify "Matrix" time check: Ensure bookings are rejected if they don't match weekly slots.
- [x] Verify UI: Check that both inlines look clean in the Unfold "Schedule" tab.
