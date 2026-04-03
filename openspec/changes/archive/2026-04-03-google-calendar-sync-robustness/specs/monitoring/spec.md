# Capability: Monitoring & Recovery

## ADDED Requirements

### Requirement: [ADDED] Manual Re-sync
Admins MUST be able to manually trigger a synchronization for one or more bookings.

#### Scenario: Bulk re-sync
**Context**: A list of `Booking` records selected from the admin panel.
**Action**: An admin selects the "Retry Sync with Google Calendar" action.
**Result**:
- The system iterates over the selected bookings.
- `sync_booking_to_google()` is called for each record.
- The `google_sync_status` and `last_synced_at` fields are updated for each record in the database.
- A final success message is shown to the admin with the count of successful/failed operations.
