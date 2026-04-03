# Tasks: Refine Booking Inline UI

- [x] **Implement `manage_booking` Button in `BookingInline`**
  - Update `BookingInline` in `scheduler/admin.py`:
    - Add `manage_booking` method that returns a styled "Manage" button linking to the booking change page.
    - Set `hide_title = True` to remove redundant row titles.
    - Add `manage_booking` to `fields` and `readonly_fields`.
    - Set `show_change_link = False`.
  - **Validation**:
    - Login to a tenant admin.
    - Edit an existing `Event`.
    - Navigate to the "Bookings" tab and verify the "Manage" button is correctly rendered and functional.
