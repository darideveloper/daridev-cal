# Design: Improved Booking Management

## Architecture Overview
The solution leverages Django's `reverse` and Unfold's custom field capabilities to create a seamless transition between the `Event` change form and the `Booking` changelist.

## Technical Details

### 1. Read-Only Inline (`BookingInline`)
The `BookingInline` in `scheduler/admin.py` will be configured as read-only:
- `extra = 0`, `max_num = 0`.
- All displayed fields (`client_name`, `client_email`, `start_time`, `status`) will be added to `readonly_fields`.
- `can_delete = False` will be set to prevent deletion from this view.

### 2. Full Bookings Link (`EventAdmin`)
A custom method `view_bookings_link` will be added to `EventAdmin`:
- It will calculate the URL for the `scheduler_booking_changelist` with an `event__id__exact` query parameter for the current `Event`.
- It will return an HTML anchor tag styled as an Unfold button using Tailwind classes (e.g., `bg-primary-600 text-white rounded-md px-4 py-2 inline-block`).
- This field will be included in the "Bookings" tab in `EventAdmin.tabs`.

### 3. Booking Table Filters (`BookingAdmin`)
The `BookingAdmin` class will ensure `event` and `status` are in `list_filter`.
- It will use `unfold.contrib.filters.admin.RangeDateFilter` for the `start_time` field to allow robust date filtering.

## Trade-offs
- **One extra click**: Users must click a button to perform full management tasks, but this is offset by the improved performance and richer tools available in the full table.
