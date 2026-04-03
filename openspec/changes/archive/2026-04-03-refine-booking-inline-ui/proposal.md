# Proposal: Refine Booking Inline UI

## Why
The default Django "Change" link in `BookingInline` is small and easily overlooked, making it difficult for admins to manage individual bookings within the `Event` change form. A dedicated, styled "Manage" button in a separate column would provide a clearer and more accessible user interface.

## What Changes
1.  **Add `manage_booking` method to `BookingInline`**: This method will return a styled HTML anchor tag acting as a "Manage" button.
2.  **Update `BookingInline` Fields**: Add `manage_booking` to the `fields` and `readonly_fields` to create a dedicated action column.
3.  **Disable `show_change_link`**: Set `show_change_link = False` in `BookingInline` to remove the redundant and less prominent default link.

## Benefits
- **Clearer UI**: A prominent button is easier to find and interact with.
- **Improved UX**: Admins can quickly manage individual bookings with a single, clear action.
- **Consistent Aesthetics**: The "Manage" button will align with the project's Tailwind-based Unfold theme.
