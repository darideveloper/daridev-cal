# Design: Improved i18n and Field Descriptions

## Principles
1.  **Contextual Clarity**: Labels should describe the field's role (e.g., "Brand Primary Color" vs. "Brand Color").
2.  **Guided Inputs**: `help_text` should provide examples for complex formats (HEX, OKLCH, UUIDs).
3.  **Language Consistency**: Ensure terms like "Booking" (Reserva), "Client" (Inquilino/Empresa), and "Event" (Servicio/Evento) are used consistently across the UI.

## Field Enhancements (Examples)

### `CompanyProfile`
- **`brand_color`**: "The primary theme color used for the public booking page. Supports HEX and OKLCH."
- **`stripe_secret_key`**: "Encrypted Stripe Secret Key. Used to process payments securely."
- **`google_calendar_id`**: "The ID of the calendar where new bookings will be synced (e.g., `user@gmail.com`)."

### `Event`
- **`duration_minutes`**: "The total length of the appointment in minutes. Used to auto-calculate the end time."
- **`allow_overlap`**: "If checked, multiple clients can book the same time slot simultaneously."

### `Booking`
- **`status`**: "Current lifecycle stage. 'Confirmed' allows the client to receive meeting details."

## Technical Approach
- All strings must use `django.utils.translation.gettext_lazy` (`_`).
- Metadata `verbose_name` and `verbose_name_plural` will be audited for all models.
- The `makemessages` command will be run after updates to capture new strings.
