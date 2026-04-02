# Design: DRY Availability Refactor

## Scope
This change aims to unify the availability logic between `CompanyProfile` and individual `Event` entities. We will refactor existing models in `scheduler` to use an inheritance-based model hierarchy.

## Architecture Change: Abstract Base Classes (ABC)
We will define three core abstract models in `scheduler/models.py`.

### 1. `BaseAvailabilityRange` (Abstract)
- Defines the validity period for the availability of the entity.
- **Fields**: `start_date`, `end_date`.

### 2. `BaseAvailabilitySlot` (Abstract)
- Defines weekly recurring time windows.
- **Fields**: `weekday`, `start_time`, `end_time`.

### 3. `BaseDateOverride` (Abstract)
- High-priority specific date rules.
- **Fields**: `date`, `is_available`, `start_time`, `end_time`.

---

## Model Reorganization
### At Company Level:
- `CompanyAvailability` (inherits `BaseAvailabilityRange`) -> ForeignKey to `CompanyProfile`.
- `CompanyWeekdaySlot` (inherits `BaseAvailabilitySlot`) -> ForeignKey to `CompanyProfile`.
- `CompanyDateOverride` (inherits `BaseDateOverride`) -> ForeignKey to `CompanyProfile`.
- **Note**: This will replace/complement the current `BusinessHours` model.

### At Event Level:
- `EventAvailability` -> Inherit from `BaseAvailabilityRange`.
- `AvailabilitySlot` -> Inherit from `BaseAvailabilitySlot`.
- `EventDateOverride` -> Inherit from `BaseDateOverride`.

---

## Service Logic Optimization: The "Matrix Engine"
The `validate_booking_time` function in `scheduler/services.py` will be refactored into a more robust hierarchical checker.

### Priority Matrix (High to Low):
1.  **Event.DateOverride** (if exists for current date)
2.  **Event.WeeklySlot** (if exists for current weekday)
3.  **Event.DateRange** (if rules exist, current date must be in at least one)
4.  **Company.DateOverride** (if exists for current date)
5.  **Company.WeeklySlot** (if exists for current weekday)
6.  **Company.DateRange** (if rules exist, current date must be in at least one)

---

## Implementation Details
1.  **Abstract Model Placement**: These ABCs will be placed at the top of `scheduler/models.py`.
2.  **Naming Consistency**: Models will use consistent field names to allow the service to be entity-agnostic.
3.  **Admin Refactoring**: `admin.py` will involve adding the new company-level inlines to the `CompanyProfileAdmin`.
