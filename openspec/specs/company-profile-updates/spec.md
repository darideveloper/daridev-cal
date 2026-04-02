# company-profile-updates Specification

## Purpose
TBD - created by archiving change refactor-booking-event-models. Update Purpose after archive.
## Requirements
### Requirement: Add Currency to Company Profile
The `CompanyProfile` model MUST store the default currency for the business.

#### Scenario: Set Currency
- **GIVEN** a user is configuring their company profile
- **WHEN** they select a currency (e.g., "USD")
- **THEN** the system saves it in the `currency` field of the `CompanyProfile` model.

### Requirement: Company-Level Rules
The `CompanyProfile` MUST support date ranges, weekly slots, and date exceptions (overrides) in the same way `Event` does.

#### Scenario: Global Date Range Validity
- **WHEN** `CompanyAvailability` is set with `start_date="2026-01-01"` and `end_date="2026-06-30"`.
- **THEN** NO bookings MUST be allowed for any `Event` outside this period unless explicitly overridden by a specific `CompanyDateOverride`.

