# Design: Refined Booking Inline UI

## Architecture Overview
The implementation involves adding a custom method to `BookingInline` in `scheduler/admin.py` that returns a styled HTML anchor tag for each booking row.

## Technical Details
- **Custom Method `manage_booking`**:
  - Takes the `obj` (the `Booking` instance) as an argument.
  - If `obj.pk` is present, it returns an HTML button using `format_html` and `reverse`.
  - The link will target the specific booking's change page (e.g., `admin:scheduler_booking_change`).
  - Styling will follow the Unfold theme using Tailwind classes (e.g., `bg-primary-600 font-medium px-4 py-1 rounded-md text-white text-xs`).
- **Inline Configuration**:
  - `fields` and `readonly_fields` in `BookingInline` will be updated to include `manage_booking` as the last column.
  - `show_change_link` will be set to `False` to prevent duplicate links.
