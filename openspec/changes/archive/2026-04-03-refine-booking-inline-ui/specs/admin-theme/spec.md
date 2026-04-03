# Capability: Admin Theme Refinement for Bookings

## ADDED Requirements

### Requirement: Styled Booking Inline Actions
The `BookingInline` in the `Event` admin SHALL include a dedicated column for a styled "Manage" button, improving the user interface for booking management.

#### Scenario: Manage Button in Booking Inline
- **Given** an existing `Event` in the admin
- **When** I navigate to the "Bookings" tab
- **Then** the `BookingInline` SHALL display a "Manage" button for each booking record.
- **And** clicking this button SHALL take me to the full edit form for that specific booking.
- **And** the default Django "Change" link SHALL NOT be visible.
