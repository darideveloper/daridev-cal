# Proposal: Refactor to Matrix Event Availability (Option C)

## Why
The current 3-tier hierarchy (`Event` -> `EventAvailability` -> `AvailabilitySlot`) is overly complex for standard scheduling. It requires nested navigation (clicking through multiple pages) to manage simple weekly hours.

## What Changes
We will implement **Option C (The Matrix Approach)**. This decouples Date Ranges from Weekly Hours, allowing both to be managed as independent inlines directly within the `Event` model.
1.  **Decoupled Structure**: Both `EventAvailability` (Date Ranges) and `AvailabilitySlot` (Weekly Hours) will link directly to `Event`.
2.  **Unified Admin**: Both will appear as separate, side-by-side (or tab-organized) inlines on the `Event` admin page.
3.  **Booking Logic**: A booking is valid if the date falls within *any* `EventAvailability` range AND the time falls within *any* `AvailabilitySlot`.

## Proposed Solution
Instead of a nested structure, both date ranges and weekly slots are now direct siblings under the `Event` model.

## Scope
-   **Model Refactor**:
    -   Change `AvailabilitySlot.event_availability` (FK) to `AvailabilitySlot.event` (FK to `Event`).
    -   Keep `EventAvailability` as a child of `Event` (already exists).
-   **Admin Update**:
    -   Update `EventAdmin` to include both `EventAvailabilityInline` and `AvailabilitySlotInline`.
    -   Organize the "Schedule" tab to show both inlines.
-   **Cleanup**: Remove the indirect link between slots and date ranges.

## Technical Decisions
-   **Direct Relation**: Both sub-models are now siblings under `Event`.
-   **Admin Tabs**: Use the "Schedule" tab to host both inlines, making the "General" tab cleaner.
