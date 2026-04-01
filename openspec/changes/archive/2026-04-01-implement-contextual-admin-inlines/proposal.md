# Proposal: Implement Contextual Admin Inlines

## Problem
The current Django admin implementation uses a "flat" structure where models are managed in isolated tables. This requires users to perform multiple navigation steps (Menu -> List -> Item -> Save -> Back -> Repeat) to complete a single logical workflow, such as onboarding a new tenant or setting up a bookable service with its schedules.

## Proposed Solution
Implement **Contextual Inlines** using `django-unfold` to group related models into hierarchical management hubs. This will:
1.  **Reduce Friction:** Enable multi-model management from a single "Main" page.
2.  **Improve Data Integrity:** Ensure that required related data (like domains or availability slots) is less likely to be forgotten.
3.  **Modernize UX:** Leverage `unfold`'s UI components to create a "SaaS Dashboard" feel.

## Key Changes
- **Public Admin:** Inline `Domain` into the `Client` admin.
- **Tenant Admin:**
    - Inline `BusinessHours` into `CompanyProfile` (requires model refactor).
    - Inline `Event` into `EventType`.
    - Inline `EventAvailability` into `Event`.
    - Inline `Booking` (read-only) into `Event`.
    - Inline `AvailabilitySlot` into `EventAvailability`.

## Impact
- **Database:** Minor schema change for `BusinessHours` (adding `ForeignKey` to `CompanyProfile`).
- **UI:** Significant improvement in management speed and cognitive load.
- **API:** No direct impact.
