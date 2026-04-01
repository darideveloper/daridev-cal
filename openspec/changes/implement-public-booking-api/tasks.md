# Tasks

- [ ] **Create Serializers:** Create `scheduler/serializers.py` with `CompanyProfileSerializer` (logo, stripe_public_key), `EventTypeSerializer`, `BookingReadSerializer` (exposing only `id`, `start_time`, `end_time`, `event_type`), and `BookingWriteSerializer` (invoking `Booking.clean()` on save/validate).
- [ ] **Create ViewSets:** Implement `CompanyProfileViewSet` (ReadOnly), `EventTypeViewSet` (ReadOnly), and `BookingViewSet` (List/Create) in `scheduler/views.py` (or `scheduler/api.py`). Ensure `authentication_classes = []` and permissions are set to `AllowAny` on all public viewsets to bypass CSRF.
- [ ] **Implement Date Filtering:** Update `BookingViewSet.get_queryset()` to accept `start_date` and `end_date` query parameters and filter bookings accordingly to prevent returning the entire database history.
- [ ] **Configure URL Routing:** Update `project/urls.py` to register the new ViewSets with the DRF router under `/api/`. Ensure routing works correctly for tenant schemas.
- [ ] **Add Unit Tests for CompanyProfile:** Add a test in `scheduler/tests.py` to verify the `CompanyProfile` API returns 200 OK and strictly excludes secret keys.
- [ ] **Add Unit Tests for EventType:** Add a test to verify `EventType` list API returns 200 OK and valid data.
- [ ] **Add Unit Tests for Booking Availability:** Add a test to verify `Booking` availability list API successfully scrubs private data (name, email) and respects `start_date`/`end_date` filtering.
- [ ] **Add Unit Tests for Booking Creation:** Add a test to verify `Booking` creation succeeds with valid data.
- [ ] **Add Unit Tests for Booking Validation:** Add a test to verify `Booking` creation fails with 400 Bad Request when overlapping slots occur (and `allow_overlap` is False).