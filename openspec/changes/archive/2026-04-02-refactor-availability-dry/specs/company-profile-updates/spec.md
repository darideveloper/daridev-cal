# Specification Delta: company-profile-updates

## Why
`CompanyProfile` needs to support advanced scheduling models (Range, Slot, Override) that inherit from the same bases as `Event` components.

## ADDED Requirements

### Requirement: Company-Level Rules
The `CompanyProfile` MUST support date ranges, weekly slots, and date exceptions (overrides) in the same way `Event` does.

#### Scenario: Global Date Range Validity
- **WHEN** `CompanyAvailability` is set with `start_date="2026-01-01"` and `end_date="2026-06-30"`.
- **THEN** NO bookings MUST be allowed for any `Event` outside this period unless explicitly overridden by a specific `CompanyDateOverride`.
