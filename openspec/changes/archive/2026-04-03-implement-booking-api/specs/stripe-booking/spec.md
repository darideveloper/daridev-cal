# Spec Delta: Stripe Booking Workflow

Define the integrated Stripe checkout and booking confirmation process.

## ADDED Requirements
### Requirement: Pre-Paid Booking Workflow
The system SHALL support a two-stage booking confirmation for services marked as `PRE-PAID` in their `EventType`.

#### Scenario: Initiating a Pre-Paid Booking
- **Given** an `Event` with `payment_model == "PRE-PAID"`.
- **When** a `POST /api/bookings/` request is made with `client_name`, `client_email`, `client_phone`, `start_time`, `success_url`, and `cancel_url`.
- **Then** a `Booking` record SHOULD be created with `status == "PENDING"`.
- **And** the `Booking` SHOULD store the `client_phone`.
- **And** the response SHOULD return a `checkout_url` from Stripe configured with the provided `success_url` and `cancel_url`.
- **And** the status code should be `201 Created`.

#### Scenario: Finalizing a Booking via Webhook
- **Given** a `Booking` with `status == "PENDING"`.
- **When** a Stripe webhook `checkout.session.completed` is received for the associated session.
- **Then** the `Booking` status MUST be updated to `"PAID"`.
- **And** automated notifications (e.g., Google Calendar sync) MUST be triggered.
- **And** the status code should be `200 OK`.
