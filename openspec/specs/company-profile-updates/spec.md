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

