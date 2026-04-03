# Tasks: Improved Booking Management

- [x] **Configure Read-Only Booking Inline**
  - Update `BookingInline` in `scheduler/admin.py`:
    - Set `extra = 0` and `max_num = 0`.
    - Set `can_delete = False`.
    - Update `readonly_fields` and `fields` to include `client_name`, `client_email`, `start_time`, `end_time`, and `status`, while hiding Google sync fields.
  - **Validation**:
    - Login to a tenant admin.
    - Edit an existing `Event`.
    - Navigate to the "Bookings" tab and verify the inline is read-only.

- [x] **Implement View All Bookings Link**
  - Add `view_bookings_link` method to `EventAdmin` in `scheduler/admin.py`.
    - Use `reverse` to generate the URL for the `Booking` changelist.
    - Append `?event__id__exact=<id>` to the URL.
    - Return a formatted HTML anchor tag with Tailwind styling.
  - Update `EventAdmin.tabs` to include `view_bookings_link` in the "Bookings" tab.
  - **Validation**:
    - Verify the "View All Bookings" button appears in the "Bookings" tab.
    - Click the button and verify it redirects to the `Booking` changelist filtered by the current event.

- [x] **Enhance Booking Table Filters**
  - Update `BookingAdmin` in `scheduler/admin.py`:
    - Add `event` and `status` to `list_filter`.
    - Add `("start_time", RangeDateFilter)` to `list_filter`.
  - **Validation**:
    - Navigate directly to the `Booking` changelist.
    - Verify the sidebar filters are available and functional.
