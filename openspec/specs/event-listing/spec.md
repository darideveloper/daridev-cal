# event-listing Specification

## Purpose
TBD - created by archiving change implement-booking-api. Update Purpose after archive.
## Requirements
### Requirement: Public Event List
The `EventViewSet` SHALL be updated to support public (unauthenticated) listing while ensuring only bookable services are returned.

#### Scenario: Listing Services
- **Given** an unauthenticated request to `GET /api/events/`.
- **When** there are active events.
- **Then** the response should include a list of `Event` objects with `id`, `title`, `image`, `description`, `price`, and `duration_minutes`.
- **And** the status code should be `200 OK`.

