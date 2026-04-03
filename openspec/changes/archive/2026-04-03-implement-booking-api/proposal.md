# Proposal: Implement Frontend Booking API

Implement a comprehensive API suite to support a separated Astro + React frontend, enabling tenant-aware branding, service discovery, real-time availability slot generation, and a multi-stage booking workflow including Stripe pre-payment integration.

## Problem
The current system has robust internal validation and models but lacks the public-facing API endpoints required for an external client-side application. Specifically, there is no way for a client to discover available time slots, view monthly availability, or provide complete contact details and localized content for a pre-paid booking via Stripe.

## Solution
1.  **Public Config API:** Provide an endpoint for the frontend to fetch tenant branding (`brand_color`, `logo`, `currency`), regional settings (`timezone`), and business info (`company_name`, `contact_email`, `contact_phone`).
2.  **Refined Event API:** Ensure services are listable with all necessary UI metadata, including `duration_minutes`.
3.  **Enhanced Availability Engine:**
    - **Month-Level Calendar:** New endpoint to identify which days in a month have free slots (for the calendar view).
    - **Daily Slot Generation:** New endpoint to calculate specific start times. **Requirement:** All times MUST be returned as strict ISO 8601 strings with timezone offsets.
4.  **Booking Model Update:** Add `client_phone` to the `Booking` model to ensure complete contact data.
5.  **Flexible Booking Workflow:** Update the booking creation to handle both `POST-PAID` (immediate confirmation) and `PRE-PAID` (Stripe checkout) services, accepting dynamic redirect URLs from the frontend.
6.  **Stripe Integration:** Add support for initializing Stripe Checkout sessions and handling webhooks to finalize bookings.
7.  **Explicit i18n Support:** Ensure all public endpoints respect the `Accept-Language` header to return localized content (titles, descriptions, error messages) in Spanish or English.

## Impact
- **Developer Experience:** Decouples the frontend from Django templates, allowing for a modern Astro + React UI.
- **User Experience:** Provides real-time availability feedback, localized content, and a complete booking journey with integrated payments.
- **Business Value:** Enables automated revenue collection and better client communication through captured phone numbers.

## Relationship
- **Depends on:** `scheduler` (models), `companies` (tenancy).
- **Influences:** `booking` (workflow).
