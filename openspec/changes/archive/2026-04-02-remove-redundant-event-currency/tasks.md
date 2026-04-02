# Tasks: Remove Redundant Event Currency

## Implementation
- [x] **1.1. Refactor `scheduler/models.py`**: Remove the `currency` field from the `Event` model.
- [x] **1.2. Update `scheduler/admin.py`**: Remove the `currency` field from the `EventAdmin` tabs.
- [x] **1.3. Clean up `scheduler/serializers.py`**: Remove `format_category` from the `EventSerializer` fields list.
- [x] **1.4. Run migrations**: Generate and apply the database schema change.

## Verification
- [x] **2.1. Model check**: Verify `Event` model no longer contains the `currency` column in the database.
- [x] **2.2. Admin UI check**: Log in to the tenant admin and confirm the "General" tab for any Event does not display a currency field.
- [x] **2.3. API check**: Query the `/api/events/` endpoint and verify the JSON response does not include `currency` or `format_category`.
