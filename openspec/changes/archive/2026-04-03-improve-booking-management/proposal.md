# Proposal: Improve Booking Management in Event Admin

## Why
Currently, the "Bookings" tab in the `Event` admin ChangeForm uses an inline model that allows full editing. As the number of bookings grows, this becomes difficult to manage, slows down the page, and lacks the powerful filtering and search capabilities of the main `Booking` changelist.

## What Changes
1.  **Refactor `BookingInline`**: Make it read-only and limited to a summary of fields (Client, Start Time, Status).
2.  **Add Direct Link to Full Table**: Add a custom field/button in the "Bookings" tab of the `Event` admin that links to the `Booking` changelist with a filter for the current `Event` already applied.
3.  **Enhance `BookingAdmin` Filters**: Ensure the `Booking` changelist has robust filters (Event, Status, Date Range) to support the redirected view.

## Benefits
- **Improved Performance**: Reduced overhead in the `Event` change form.
- **Better UX**: Access to full admin features (search, export, bulk actions) for managing bookings.
- **Data Integrity**: Prevents accidental edits of historical bookings directly from the `Event` page.
