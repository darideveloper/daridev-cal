# Design: Streamline Event Availability Management in Admin

## Architecture
The design prioritizes a two-step management process instead of triple-nesting inlines on a single page. This approach reduces complexity and ensures full compatibility with the `django-unfold` UI.

### Workflow: Event -> Availability -> Slots
1.  **Event Admin Page**:
    - Includes an "Availability" tab.
    - Contains `EventAvailabilityInline`.
    - Each rule in the inline has a "Change" link enabled (`show_change_link = True`).
2.  **EventAvailability Admin Page**:
    - Accessed by clicking "Change" from the Event page.
    - Contains `AvailabilitySlotInline`.
    - Allows adding/removing/editing slots for that specific availability rule.

### UI/UX Benefits
- **Clarity**: Each page has a single responsibility.
- **Responsiveness**: Smaller pages load faster and are more reliable on mobile devices.
- **Theming**: No third-party templates are required; the design remains purely `django-unfold`.
