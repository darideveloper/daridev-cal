# Capability: Admin Theme Refinement for Bookings

## ADDED Requirements

### Requirement: Event Admin Booking Management
The `Event` admin ChangeForm SHALL provide a read-only summary of linked bookings and a direct link to the full filtered `Booking` changelist.

#### Scenario: Read-only Booking Inline
- **Given** an existing `Event` in the admin
- **When** I navigate to the "Bookings" tab
- **Then** the `BookingInline` SHALL display bookings in a read-only format.
- **And** it SHALL NOT allow adding or deleting bookings directly from this inline.

#### Scenario: Link to Full Booking Table
- **Given** an existing `Event` in the admin
- **When** I navigate to the "Bookings" tab
- **Then** a "View All Bookings" button/link SHALL be visible.
- **And** clicking this link SHALL redirect to the `Booking` changelist with the filter `event__id__exact` applied for the current event.

### Requirement: Booking Changelist Filtering
The `Booking` admin changelist SHALL provide robust filtering capabilities to facilitate management.

#### Scenario: Booking Table Filters
- **Given** I am in the `Booking` changelist
- **When** I open the filter sidebar
- **Then** I SHALL see filters for `Event`, `Status`, and a date range filter for `Start Time`.
