# Proposal: Refactor Booking & Event Models

## Why
The current model is too rigid, combining service categories with booking details. This refactor decouples them to allow for specific service instances, per-event availability rules, and global business hour fallbacks, supporting a more scalable multi-tenant architecture.

## What Changes
- **New Models**: Introduced `Event`, `BusinessHours`, `EventAvailability`, and `AvailabilitySlot`.
- **Refactored Models**: Updated `EventType` to act as a category and `Booking` to link directly to specific `Event`s.
- **Service Layer**: Introduced `scheduler/services.py` for hierarchical validation logic.
- **Admin & API**: Updated the admin sidebar and DRF viewsets to reflect the new structure.

Please review the associated `design.md` and spec deltas in `specs/`.
