# Proposal: Refactor Booking & Event Models

This proposal outlines a significant refactoring of the database schema for the scheduling system. The goal is to move from a simple `EventType -> Booking` model to a more flexible and powerful structure that supports event categories, specific event instances, and complex availability rules.

This change introduces new models for `Event`, `BusinessHours`, `EventAvailability`, and `AvailabilitySlot`, refactors the existing `EventType` and `Booking` models, and adds a `currency` setting to the `CompanyProfile`. This will enable per-event customization and sophisticated booking limitations.

Please review the associated `design.md` for the detailed architectural changes and the spec deltas for specific requirements.
