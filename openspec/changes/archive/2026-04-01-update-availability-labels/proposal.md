# Proposal: Update Availability Inline Labels for Clarity

## Why
The current model names `EventAvailability` and `AvailabilitySlot` can be confusing for administrators. It's not immediately clear which one defines the overall date ranges and which one defines the specific recurring weekly hours.

## What Changes
We will update the `verbose_name` and `verbose_name_plural` for these models (and their inlines) to explicitly state their purpose:
1.  **EventAvailability** -> "Date Range" / "Date Ranges"
2.  **AvailabilitySlot** -> "Week Day" / "Week Days"

This will make the tabs and section headers in the `Event` admin much more intuitive.

## Proposed Solution
Update the `Meta` classes in `scheduler/models.py` and ensure the `EventAdmin` in `scheduler/admin.py` reflects these labels correctly in its tab definitions if necessary.

## Scope
- Update `scheduler/models.py`: `EventAvailability` and `AvailabilitySlot` Meta classes.
- Verify `scheduler/admin.py`: Inline labels and tab names.
