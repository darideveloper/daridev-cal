# Design: Contextual Admin Inlines

## Context
A recurring friction point in multi-tenant SaaS applications is the overhead of navigating isolated administrative tables. Current users must jump between menus to configure related data.

## Objectives
- **Centralize tenant setup:** Onboard clients and their domains in one step.
- **Service Hubs:** Consolidate service definitions with their availability rules and recent booking history.
- **Global Settings:** Unify general business settings (logo, color) with operating hours.

## Architectural Reasoning

### Singleton-to-Child Relationship
Refactoring `BusinessHours` to have a `ForeignKey` to `CompanyProfile` is a deliberate design choice. Since `CompanyProfile` is a singleton (managed via `django-solo`), linking `BusinessHours` to it ensures that:
- A tenant only has one set of "Global Settings."
- All global configurations are physically grouped in the database per tenant.
- The admin interface can display them as a unified configuration hub.

### Nested Inlines & Tabbed Layouts
Since `django-nested-admin` is not currently installed, we will use standard `unfold` inlines with a **"Drill-down" pattern** combined with **Tabs** for complex models:
- **EventAdmin:** Will use Unfold's `Tabs` to separate "General Info", "Availability Rules", and "Booking History". This prevents vertical fatigue.
- **show_change_link:** Enabled for all inlines to allow quick navigation to deeper detail pages.

### Sidebar Optimization (UX)
To reduce cognitive load, child models that are primarily managed via inlines will be hidden from the main admin sidebar:
- Hide `Domain` from Public Admin (managed via `Client`).
- Hide `BusinessHours`, `AvailabilitySlot`, and `EventAvailability` from Tenant Admin.

### Visual Feedback
- **Logo/Image Previews:** Implement custom `readonly_fields` or widget overrides to show small thumbnails of uploaded logos/images directly in the change forms.

### Performance & Scalability
- **Booking History:** To prevent the `Event` edit page from slowing down, the `Booking` inline will be:
    - **Read-only**: To prevent accidental data modification.
    - **Limited**: Show only the most recent 5-10 bookings.
    - **Collapsed**: Hidden by default using Unfold's `classes = ["collapse"]`.
