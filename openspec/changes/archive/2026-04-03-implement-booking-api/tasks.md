# Tasks: Implement Frontend Booking API

Development plan for the public-facing booking API.

## Phase 1: Service Layer Enhancement
- [x] **Booking Model Update:** Add `client_phone` field to `scheduler.models.Booking`.
- [x] **Company Profile Update:** Add `contact_email` and `contact_phone` fields to `scheduler.models.CompanyProfile`.
- [x] **Daily Slot Generation:** Implement `get_available_slots` returning strict ISO 8601 strings.
- [x] **Monthly Availability Logic:** Implement `get_monthly_availability`.
- [x] **Migrations:** Create and run migrations for model updates.

## Phase 2: Public Configuration & Event APIs
- [x] **Config Endpoint:** Create `CompanyConfigView` to return branding, business info, and `timezone`.
- [x] **Event API Refinement:** 
    - [x] Update `EventSerializer` to include `duration_minutes`.
    - [x] **i18n Support:** Ensure title/description are translated using `i18n` utilities.
- [x] **CORS Verification:** Ensure the frontend origin is correctly configured.

## Phase 3: Booking & Availability API
- [x] **Availability Actions:**
    - [x] Add `GET /api/events/<id>/calendar/` action (for month view).
    - [x] Add `GET /api/events/<id>/slots/` action (for day view).
- [x] **Public Booking:**
    - [x] Update `BookingViewSet` for public creation.
    - [x] **i18n Support:** Ensure validation error messages are localized.
- [x] **Throttling:** Apply `AnonRateThrottle`.

## Phase 4: Stripe Pre-Payment Integration
- [x] **Stripe Client Utility:** Initialize Stripe with tenant-specific keys.
- [x] **Checkout Session Logic:** 
    - [x] Implement `create_stripe_checkout(booking, success_url, cancel_url)` utility.
    - [x] Integrate with `BookingViewSet.create`.
- [x] **Webhook Handler:** Implement `/api/webhooks/stripe/`.

## Phase 5: Validation & Final Polish
- [x] **Localization Verification:** Test endpoints with `Accept-Language: es` and `en`.
- [x] **End-to-End API Test:** Complete the flow: Config -> Calendar -> Slots -> Booking.
- [x] **Google Calendar Verification:** Ensure confirmed bookings sync automatically.
