# Design: Implement Customizable UI Labels in Company Profile

## Architecture
The system follows a standard Django/DRF architecture. The `CompanyProfile` model stores tenant-specific configuration. The `CompanyConfigView` retrieves the single `CompanyProfile` instance (multi-tenancy is handled via the domain) and returns a JSON response.

## Data Model Changes
Add the following fields to `CompanyProfile`:

- `event_type_label` (CharField): Label for the `EventType` categories.
- `event_label` (CharField): Label for the `Event` services.
- `availability_free_label` (CharField): Text for available slots.
- `availability_regular_label` (CharField): Text for slots with bookings.
- `availability_no_free_label` (CharField): Text for no more capacity.
- `extras_label` (CharField): Label for additional details or comments.

## API Changes
Update `GET /api/config/` to return these new labels. This involves updating:
- `CompanyConfigSerializer`: Add new fields to the serializer.
- `CompanyConfigView`: Populate the data dictionary with values from the `CompanyProfile` instance.

## Admin UI Changes
Update `CompanyProfileAdmin` to include a new tab named "UI Labels" containing the new fields. This ensures a clean separation between business settings (e.g., Stripe keys, Google Calendar ID) and UI labels.

## Internationalization
All new labels in the model and admin UI will use `gettext_lazy` so they can be translated into other languages (e.g., Spanish).
