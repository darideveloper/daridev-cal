# Design: Frontend Booking API

Architecture for the public-facing booking API to support an external Astro + React frontend.

## Overview
The system must provide the frontend with all necessary configuration, services, and availability data to facilitate a booking, while ensuring strict backend validation, i18n support, and pre-payment handling.

## Architecture

### 1. Public Configuration API
**Goal:** Allow the frontend to identify the current tenant, apply branding, and understand regional/business context.
**Mechanism:** 
- A new viewset/endpoint `GET /api/config/` (Public).
- Uses `django-tenants` middleware to identify the `Client`.
- Returns:
    - `brand_color`, `logo` URL, `currency`, and current project `TIME_ZONE`.
    - Business Info: `company_name` (from `Client.name`), `contact_email`, and `contact_phone`.

### 2. Enhanced Availability Engine
**Goal:** Generate daily slots AND monthly calendar data.
**A. Monthly Calendar View (`GET /api/events/<id>/calendar/`):**
- **Logic:** For each day in the requested month/year, check the availability service.
- **Optimization:** Returns a simple boolean or count per day (e.g., `{"2026-05-01": true, "2026-05-02": false}`).
**B. Daily Slot Generation (`GET /api/events/<id>/slots/`):**
- **Logic:** Calculate theoretical slots from rules and subtract busy blocks from confirmed `Booking` instances (respecting `allow_overlap`).
- **Formatting:** Returns strict ISO 8601 strings (e.g., `["2026-05-01T09:00:00-06:00", ...]`). The frontend can use these strings directly in the `POST /api/bookings/` payload.

### 3. Booking Model Update
**Goal:** Capture all necessary client data.
- **Field:** Add `client_phone` to the `Booking` model.

### 4. Stripe Integration Workflow
**Goal:** Securely handle pre-payments for `PRE-PAID` services with dynamic redirects.
**Workflow:**
1.  **Initiate Booking:** Frontend sends `POST /api/bookings/` with `client_phone`, `success_url`, and `cancel_url`.
2.  **Validation:** Backend runs full `validate_booking_time`.
3.  **Checkout Session:**
    - Create Stripe Checkout session using the `success_url` and `cancel_url` provided by the frontend.
    - Return session `checkout_url`.
4.  **Webhook:** Stripe sends a `checkout.session.completed` event to finalize the `Booking` status.

### 5. Internationalization (i18n)
- All public endpoints SHALL integrate with `django.middleware.locale.LocaleMiddleware`.
- Serializers will return translated fields for `Event.title`, `Event.description`, and `EventType.title` based on the `Accept-Language` header.

### 6. Security & Permissions
- **Public Access:** `GET /api/events/`, `GET /api/config/`, `GET /api/events/<id>/calendar/`, `GET /api/events/<id>/slots/`, and `POST /api/bookings/` (Creation only).
- **Throttling:** Implement `AnonRateThrottle`.
