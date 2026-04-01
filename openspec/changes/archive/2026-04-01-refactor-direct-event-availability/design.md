# Design: Refactor to Matrix Event Availability (Option C)

## Model Structure Refactor
Both Date Ranges and Weekly Hours will now be direct children of the `Event` model.

### After (Matrix / Siblings)
- **`Event`**: Root model.
- **`EventAvailability`** (Related: `availability_rules`): Holds date ranges (`start_date`, `end_date`).
- **`AvailabilitySlot`** (Related: `availability_slots`): Holds weekly hours (`weekday`, `start_time`, `end_time`).

## Validation Logic: "The Intersection Rule"
A booking is valid if, and only if:
1.  **Date Validity**:
    - If `EventAvailability` records exist, the booking date MUST fall within at least one range.
    - If no `EventAvailability` records exist, all dates are considered valid (infinite availability).
2.  **Time Validity**:
    - The booking's weekday and time range MUST match at least one `AvailabilitySlot`.
    - If no `AvailabilitySlot` records exist, the event is never bookable.

## Admin UI: Compacting the Schedule
Both inlines will use `TabularInline` to maximize vertical space in the `Unfold` "Schedule" tab.

-   **Tab: Schedule**
    - **Header: Active Date Ranges** (e.g., Summer, Holiday, etc.)
    - **Header: Weekly Recurring Hours** (e.g., Mon 9-5, etc.)

This creates a high-density, high-information view on a single page.
