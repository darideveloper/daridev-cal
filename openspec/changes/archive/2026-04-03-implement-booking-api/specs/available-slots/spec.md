# Spec Delta: Available Slots API

Define the logic and endpoint for discovering available booking times.

## ADDED Requirements
### Requirement: Slot Discovery Endpoint
The system MUST provide an endpoint to return available time slots for a specific event and date.

#### Scenario: Requesting Slots for a Date
- **Given** an event with a 30-minute duration and business hours from 09:00 to 12:00.
- **When** an unauthenticated request to `GET /api/events/<id>/slots/?date=2026-05-01` is made.
- **Then** the response MUST return a list of start times as strict ISO 8601 strings (e.g., `["2026-05-01T09:00:00-06:00", "2026-05-01T09:30:00-06:00", ...]`).
- **And** the list MUST exclude slots that overlap with existing confirmed `Booking` instances (if `allow_overlap` is `False`).
- **And** the list MUST respect all hierarchical overrides and date ranges defined in `scheduler.services.validate_booking_time`.
- **And** the status code should be `200 OK`.

### Requirement: Month-Level Availability
The system MUST provide an endpoint to return daily availability status for a specific month and year.

#### Scenario: Fetching Calendar View Data
- **Given** an event with existing availability rules.
- **When** an unauthenticated request to `GET /api/events/<id>/calendar/?month=05&year=2026` is made.
- **Then** the response should return a mapping of dates to their availability status (e.g., `{"2026-05-01": true, "2026-05-02": false}`).
- **And** a date SHALL be marked as `true` only if at least one bookable slot exists for that date.
- **And** the status code should be `200 OK`.
