# Design: Centralized Google Calendar Integration

## Architecture

### 1. Global Credentials
The Google Service Account JSON credentials will be moved to the environment configuration (`.env`) and loaded into `settings.py`.

```python
# settings.py
GOOGLE_CALENDAR_CREDENTIALS = os.getenv("GOOGLE_CALENDAR_CREDENTIALS")
```

### 2. Tenant Profile Cleanup
The `google_calendar_credentials` field will be removed from `CompanyProfile`. The `google_calendar_id` field will remain, as it uniquely identifies the specific calendar allocated to that tenant within the master account.

### 3. Automated Lifecycle
A new signal or service logic will be added:
- **When `CompanyProfile` is created/updated**: 
  - If `google_calendar_id` is empty, the master service account creates a new calendar via the API.
  - The new `calendar_id` is saved to the `CompanyProfile`.
  - The calendar is shared with the client's email address (view-only) via `acl().insert()`.

### 4. Shared Access Control
The `ACL` (Access Control List) for each created calendar will be strictly managed:
- **Service Account**: Owner/Writer.
- **Client Email**: Reader (View-only).
- **Public**: No access (unless explicitly enabled for public booking views).

## Quota and Limits
- **Daily Requests**: 1,000,000 (standard).
- **Calendars per Account**: Google Workspace accounts allow thousands of secondary calendars.
- **Sharing**: Calendars can be shared with individual emails programmatically.

## Sequence Diagram (Simplified)

1. Admin creates Client (Tenant).
2. `post_save` on `CompanyProfile` triggers `ensure_google_calendar`.
3. System uses `settings.GOOGLE_CALENDAR_CREDENTIALS` to:
   a. Create Calendar "Client Name - Bookings".
   b. Grant `reader` access to `client_email`.
   c. Store `calendar_id` in `CompanyProfile`.
4. Subsequent `Booking` objects use the same global credentials to sync to the tenant's specific `calendar_id`.
