# booking-model-update Specification

## Purpose
TBD - created by archiving change implement-booking-api. Update Purpose after archive.
## Requirements
### Requirement: Comprehensive Client Contact Data
The `Booking` model MUST store the client's phone number to facilitate automated reminders and direct communication.

#### Scenario: Capturing Phone Number
- **Given** a new booking is being created.
- **When** the client provides a phone number.
- **Then** the `Booking` record SHALL store this value in a `client_phone` field.
- **And** the field MUST support international phone number formats.

