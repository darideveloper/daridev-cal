# Frontend Booking API Documentation

This document describes the public-facing API for the booking system, designed to support external Astro + React frontends.

## Overview
The API is tenant-aware and uses the `Host` header (or domain) to identify the current provider. It supports internationalization via the `Accept-Language` header (Spanish `es` and English `en`).

### Base URL
`http://<tenant-domain>/api/`

---

## 1. Public Configuration
Retrieve branding, business info, and regional settings to initialize the frontend.

**Endpoint:** `GET /config/`

**Response Example:**
```json
{
  "brand_color": "#a01313",
  "logo": "http://company1.localhost/media/logos/logo.png",
  "currency": "USD",
  "contact_email": "contact@company.com",
  "contact_phone": "+123456789",
  "company_name": "First Company",
  "timezone": "America/Mexico_City",
  "event_type_label": "Event Type",
  "event_label": "Event",
  "availability_free_label": "Free",
  "availability_regular_label": "Regular",
  "availability_no_free_label": "Full",
  "extras_label": "Extras"
}
```

**Integration Tip:** Use `brand_color` for dynamic CSS (e.g., buttons, accents) and `timezone` to inform date displays.

---

## 2. Business Hours
Retrieve the company's global operating hours.

**Endpoint:** `GET /business-hours/`

**Response Example:**
```json
[
  {
    "weekday": 1,
    "start_time": "09:00:00",
    "end_time": "18:00:00"
  },
  {
    "weekday": 2,
    "start_time": "09:00:00",
    "end_time": "18:00:00"
  }
]
```
*Note: `weekday` follows ISO 1 (Monday) to 7 (Sunday).*

---

## 3. Services (Events) Discovery
List available bookable services.

**Endpoint:** `GET /events/`

**Query Parameters:**
- `page`: Pagination page number.

**Response Snippet:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Depilación de cejas",
      "event_type_title": "Servicios",
      "image": "...",
      "description": "Limpieza y diseño de cejas.",
      "detailed_description": "<p>Full details including 디자인 and cleanup.</p>",
      "price": "99.00",
      "duration_minutes": 30,
      "availability_rules": [
        {
          "start_date": "2026-01-01",
          "end_date": "2026-12-31",
          "slots": [
            { "weekday": 1, "start_time": "09:00:00", "end_time": "17:00:00" }
          ]
        }
      ],
      "date_overrides": []
    }
  ]
}
```

**i18n:** Sending `Accept-Language: es` will return `title` and `description` in Spanish if translations are provided.

---

## 4. Availability Engine
The engine calculates available slots based on business hours, overrides, and existing confirmed bookings.

### A. Monthly Calendar View
Identifies which days in a month have at least one free slot.

**Endpoint:** `GET /events/<id>/calendar/`

**Parameters:**
- `year` (int): e.g., 2026
- `month` (int): 1-12

**Response:**
```json
{
  "2026-04-01": false,
  "2026-04-02": true,
  ...
}
```

### B. Daily Slot Generation
Returns specific start times available for a chosen date.

**Endpoint:** `GET /events/<id>/slots/`

**Parameters:**
- `date` (string): `YYYY-MM-DD`

**Response:**
```json
[
  "2026-04-10T09:00:00-06:00",
  "2026-04-10T09:30:00-06:00",
  ...
]
```
**Note:** These are strict ISO 8601 strings including the timezone offset. Use them directly in the booking payload.

---

## 5. Booking Workflow

### Initiate Booking
Creates a booking record. Handles both free/post-paid (automatic confirmation) and pre-paid (Stripe redirection) services.

**Endpoint:** `POST /bookings/`

**Payload:**
```json
{
  "event": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com",
  "client_phone": "+521234567890",
  "start_time": "2026-04-10T09:00:00-06:00",
  "success_url": "https://frontend.com/booking/success",
  "cancel_url": "https://frontend.com/booking/cancel"
}
```
*Note: `success_url` and `cancel_url` are only strictly required for PRE-PAID services.*

**Response (POST-PAID):**
```json
{
  "id": 123,
  "status": "CONFIRMED",
  "event": 1,
  "client_name": "John Doe",
  "start_time": "2026-04-10T09:00:00-06:00",
  "end_time": "2026-04-10T09:30:00-06:00"
}
```

**Response (PRE-PAID):**
```json
{
  "id": 124,
  "status": "PENDING",
  "checkout_url": "https://checkout.stripe.com/pay/..."
}
```
**Action:** The frontend should redirect the user to `checkout_url`.

---

## 6. Stripe Webhook (Backend Only)
The backend listens at `/api/webhooks/stripe/` for `checkout.session.completed` to update bookings to `PAID` and trigger Google Calendar synchronization.

---

## 7. API Behavior

### Throttling
The API implements **AnonRateThrottle** for all public endpoints. If the limit is exceeded, a `429 Too Many Requests` status will be returned.

### Internationalization
Use the `Accept-Language` header to request localized content. Supported values: `en`, `es`.

---

## Integration Examples (curl)

### Fetch Config
```bash
curl -H "Host: company1.localhost" http://localhost:8000/api/config/
```

### Fetch Slots for a Day
```bash
curl -H "Host: company1.localhost" "http://localhost:8000/api/events/1/slots/?date=2026-04-10"
```

### Create a Booking
```bash
curl -X POST -H "Host: company1.localhost" -H "Content-Type: application/json" \
-d '{
  "event": 1,
  "client_name": "Jane Smith",
  "client_email": "jane@example.com",
  "client_phone": "555-0199",
  "start_time": "2026-04-10T10:00:00-06:00",
  "success_url": "http://localhost:3000/success",
  "cancel_url": "http://localhost:3000/cancel"
}' http://localhost:8000/api/bookings/
```

