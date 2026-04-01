# Proposal: Implement Public Booking API (Phase 3)

## Goal
Implement the unauthenticated Public Django Rest Framework (DRF) APIs necessary to power the customer-facing booking frontend. This fulfills Phase 3 of the project requirements.

## Context
The project already features a robust multi-tenant backend and an administrative dashboard (Unfold). However, the public-facing booking engine is missing. According to the `docs/pr.md` requirements for Phase 3, we need to create unauthenticated DRF endpoints to list available `EventType` instances, view availability (slots), and create `Booking` instances, while ensuring strict data privacy and enforcing the existing `allow_overlap` business rules. 

Furthermore, to support frontend rendering and client-side payments, we must expose limited tenant configuration (like logos and public Stripe keys).

## Proposed Solution
We will implement standard DRF ViewSets and Serializers in the `scheduler` app (or a dedicated `api` module within it). All views in this proposal must have `authentication_classes = []` and `permission_classes = [AllowAny]` to prevent session-based CSRF blocks for public unauthenticated users.

1. **Serializers:**
   - `CompanyProfileSerializer`: Exposes non-sensitive tenant details necessary for the frontend (`logo`, `stripe_public_key`). It strictly excludes secrets.
   - `EventTypeSerializer`: Exposes basic details of available event types (`id`, `title`, `duration_minutes`, `price`, `payment_model`).
   - `BookingReadSerializer`: A stripped-down serializer used only for the availability check. It will strictly expose `start_time`, `end_time`, and `event_type` to prevent leaking PII.
   - `BookingWriteSerializer`: Accepts incoming payload (`event_type`, `client_name`, `client_email`, `start_time`) to create a new booking.

2. **Views (ViewSets):**
   - `CompanyProfileViewSet`: `ReadOnlyModelViewSet` (or simple APIView) to fetch the current tenant's profile.
   - `EventTypeViewSet`: `ReadOnlyModelViewSet` for querying available event types.
   - `BookingViewSet`: A ViewSet supporting `list` and `create`.
     - `list`: Uses `BookingReadSerializer`. MUST support `start_date` and `end_date` query parameters to filter bookings and prevent data dumps.
     - `create`: Uses `BookingWriteSerializer` to handle new bookings.

3. **Validation & Routing:**
   - The conflict check logic `(NewStart < ExistingEnd) AND (NewEnd > ExistingStart)` is already handled in `Booking.clean()`. We just need to ensure the DRF Serializer triggers this validation (e.g., by calling `instance.clean()` during the save process).
   - Wire these ViewSets to the existing DRF router in `project/urls.py` under the `/api/` prefix.

## Changes
- **`public-api`**: Adds the `CompanyProfile` read API, `EventType` read API, the `Booking` availability read API with date filtering, and the `Booking` creation API.
