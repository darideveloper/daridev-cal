# Design: Booking & Event Model Architecture

## 1. Overview
The current model is too rigid for the desired functionality. It combines the concept of a service category (e.g., "Haircut") with the booking details (price, duration). The proposed architecture decouples these concepts, providing a more scalable and flexible system.

The new entity relationship will be:
- `CompanyProfile`: Holds tenant-level configuration, including the new `currency` setting and global `BusinessHours`.
- `EventType`: Acts as a high-level category (e.g., "Consultations", "Hair Services"). It will retain shared properties like `description`, `payment_model`, and `allow_overlap`.
- `Event`: Represents a specific, bookable service (e.g., "Basic Consultation", "Men's Haircut"). It contains the unique details like title, price, duration, and image. It links back to an `EventType`.
- `EventAvailability`: An optional set of rules that constrain when a specific `Event` can be booked. This includes date ranges and links to specific `AvailabilitySlot` records for weekly rules.
- `AvailabilitySlot`: Represents a specific time window on a specific day of the week for an `EventAvailability` set (e.g., Monday 9:00-12:00).
- `BusinessHours`: The default, global availability for the entire company, used as a fallback when an `Event` has no specific `EventAvailability` rules.
- `Booking`: The final appointment, now linked directly to a specific `Event`.
- `Services`: A dedicated layer for business logic, specifically for booking creation and validation.

## 2. Model Schema Changes

### `scheduler.CompanyProfile`
- **MODIFIED**: Add a `currency` field to store the business's operating currency (e.g., 'USD', 'EUR').

### `scheduler.BusinessHours` (New Model)
- **ADDED**: A new model to define the default weekly operating hours for a business.
- **Fields**: `weekday` (Mon-Sun), `start_time`, `end_time`.
- **Relationship**: A tenant will have a set of these records, one for each day of the week they are open.

### `scheduler.EventType`
- **MODIFIED**: This model will be simplified to act as a category.
- **Fields to KEEP**: `title`, `description`, `payment_model`, `allow_overlap`.
- **Fields to REMOVE**: `duration_minutes`, `price`. These are now specific to an `Event`.

### `scheduler.Event` (New Model)
- **ADDED**: The core new model representing a specific bookable service.
- **Fields**:
    - `event_type` (FK to `EventType`)
    - `title`, `image`, `description`, `detailed_description`
    - `price` (optional)
    - `duration_minutes` (for internal calculation)
    - `format_category`
- **Relationship**: Many `Event`s can belong to one `EventType`.

### `scheduler.EventAvailability` (New Model)
- **ADDED**: Defines complex, optional availability rules for a single `Event`.
- **Fields**:
    - `event` (FK to `Event`)
    - `start_date` (nullable): Start of the rule's validity.
    - `end_date` (nullable): End of the rule's validity.
- **Relationship**: Links to multiple `AvailabilitySlot` records for weekly constraints.

### `scheduler.AvailabilitySlot` (New Model)
- **ADDED**: Normalized storage for weekly time slots.
- **Fields**:
    - `event_availability` (FK to `EventAvailability`)
    - `weekday` (0-6): Monday to Sunday.
    - `start_time` (TimeField)
    - `end_time` (TimeField)
- **Logic**: Allows an event to have multiple distinct time slots on the same day (e.g., morning and afternoon sessions).

### `scheduler.Booking`
- **MODIFIED**: The booking will now be tied to the specific `Event`.
- **Relationship Change**: The `event_type` ForeignKey will be replaced with an `event` ForeignKey pointing to the `Event` model.
- **Calculated Field**: The `end_time` will continue to be calculated based on `start_time + event.duration_minutes`.

## 3. Booking Validation & Service Layer
For a system of this complexity, business logic should be encapsulated in a dedicated service layer (`scheduler/services.py`). This keeps models clean and ensures consistency across the application (API, admin, background tasks).

The validation process for creating or updating a booking will be as follows:

1.  **Check for Overlap**: First, perform the existing overlap check based on the `event.event_type.allow_overlap` flag.
2.  **Check for Specific Availability**: Does the `event` have an associated `EventAvailability` record?
    - If **YES**: The requested booking `start_time`'s date and time must fall within the constraints defined by `EventAvailability` (date range and/or weekly time slots). If it doesn't, the booking is invalid.
3.  **Check for Global Availability**: If the `event` has NO `EventAvailability` record.
    - The requested booking `start_time`'s weekday and time must fall within the `BusinessHours` defined for the company. If it doesn't, the booking is invalid.
4.  If all checks pass, the booking is considered valid.
