# spec.md (business-hours)

## MODIFIED Requirements

### Requirement: Define Global Business Hours
A new model, `BusinessHours`, MUST be created to store the default weekly operating hours for a business.

#### MODIFIED Scenario: Define Weekly Hours
- **GIVEN** a business owner wants to set their weekly availability
- **WHEN** they create a `BusinessHours` entry
- **THEN** it MUST be associated with the `CompanyProfile` singleton via a `ForeignKey`.
- **AND** the record SHALL store the `weekday`, `start_time`, and `end_time`.
