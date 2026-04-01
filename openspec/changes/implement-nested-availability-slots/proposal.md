# Proposal: Streamline Event Availability Management in Admin

## Problem
Currently, managing `AvailabilitySlot` records is difficult because they are two levels deep (`Event` -> `EventAvailability` -> `AvailabilitySlot`). Standard Django and `django-unfold` do not support triple-nested inlines on a single page, making it hard to find where to edit specific time slots.

## Proposed Solution
Instead of adding heavy dependencies like `django-nested-admin`, we will leverage `django-unfold`'s native **Tabs** and **Change Links** features to create a clean, hierarchical workflow:
1.  **Event Admin**: Add a dedicated "Availability" tab.
2.  **EventAvailability Inline**: Display rules in this tab with `show_change_link = True`.
3.  **EventAvailability Admin**: Register this admin so the change link works, and include `AvailabilitySlotInline` here.

This allows an admin to go `Event` -> `Edit Availability Rule` -> `Manage Slots` with a single click, maintaining a clean UI.

## Scope
- Refactor `scheduler/admin.py` to register `EventAvailabilityAdmin`.
- Enable `show_change_link` on `EventAvailabilityInline`.
- Configure `EventAdmin` to use Tabs for better organization.
- Ensure `AvailabilitySlotInline` is correctly attached to `EventAvailabilityAdmin`.

## Technical Decisions
- **No New Dependencies**: Avoids `django-nested-admin` to prevent UI/CSS conflicts with the `Unfold` theme.
- **Native Unfold Features**: Uses `tab = True` and `show_change_link` for a modern, responsive feel.
