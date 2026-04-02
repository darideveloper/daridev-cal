## 1. Preparation
- [x] 1.1 Read related specs in `openspec/specs/`
- [x] 1.2 Identify all fields to be moved to abstract base classes

## 2. Model Implementation
- [x] 2.1 Define `BaseAvailabilityRange` abstract model with `start_date`, `end_date`
- [x] 2.2 Define `BaseAvailabilitySlot` abstract model with `weekday`, `start_time`, `end_time`
- [x] 2.3 Define `BaseDateOverride` abstract model with `date`, `is_available`, `start_time`, `end_time`
- [x] 2.4 Update `EventAvailability`, `AvailabilitySlot`, `EventDateOverride` to inherit from these bases
- [x] 2.5 Create `CompanyAvailability`, `CompanyWeekdaySlot`, `CompanyDateOverride` inheriting from the bases

## 3. Service Layer Refactor
- [x] 3.1 Refactor `validate_booking_time` to check both Entity-level and Provider-level rules
- [x] 3.2 Ensure Priority Matrix: Event Overrides > Event Slots > Event Ranges > Company Overrides > Company Slots > Company Ranges

## 4. Admin UI
- [x] 4.1 Update `scheduler/admin.py` with new inlines for `CompanyProfile`
- [x] 4.2 Sync `help_text` and translations across new models

## 5. Deployment and Validation
- [x] 5.1 Run `python manage.py makemigrations scheduler`
- [x] 5.2 Run `python manage.py migrate`
- [x] 5.3 Verify all scenarios in spec deltas pass
- [x] 5.4 Run `openspec validate refactor-availability-dry --strict`
