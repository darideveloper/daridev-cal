# public-api Specification

## Purpose
Defines the public Django Rest Framework endpoints needed for the booking frontend (Phase 3).

## ADDED Requirements

### Requirement: Public CompanyProfile API
The CompanyProfile API SHALL expose non-sensitive tenant configuration to the public.

#### Scenario: Retrieving Tenant Configuration
- The API returns the current tenant's profile.
- Fields exposed include: `id`, `logo`, and `stripe_public_key`.
- Sensitive fields like `stripe_secret_key` and `google_calendar_id` MUST NEVER be exposed.
- Authentication checks are bypassed (`authentication_classes = []`) to prevent public CSRF failures.

### Requirement: Public EventType API
The EventType API SHALL expose unauthenticated read-only endpoints.

#### Scenario: Listing Event Types
- The API returns a list of active `EventType` instances for the current tenant.
- Fields exposed include: `id`, `title`, `duration_minutes`, `price`, and `payment_model`.
- Authentication checks are bypassed (`authentication_classes = []`).

### Requirement: Public Booking Availability API
The Booking API SHALL expose existing bookings as read-only slots without sensitive client data, filtered by a date range.

#### Scenario: Checking Availability with Date Filtering
- The API accepts `start_date` and `end_date` query parameters.
- It returns a list of `Booking` instances that overlap with the provided date range.
- Only `start_time`, `end_time`, and `event_type.title` are exposed.
- Client name, email, and any other private data MUST NOT be exposed.
- Authentication checks are bypassed (`authentication_classes = []`).

### Requirement: Booking Creation API
The Booking API SHALL allow unauthenticated users to create new bookings.

#### Scenario: Submitting a Booking
- The API accepts `event_type`, `client_name`, `client_email`, and `start_time`.
- The system automatically calculates `end_time` and validates overlaps using the model's `clean()` method.
- Returns the created booking details with status `PENDING`.
- If an overlap occurs and `allow_overlap` is False, the API MUST return a 400 Bad Request with a validation error.
- Authentication checks are bypassed (`authentication_classes = []`).