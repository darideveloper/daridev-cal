# Design: Single Tenant Currency

## Context
In a multi-tenant environment, consistent branding and configuration are crucial. The currency is a key business-level setting that should apply across all services offered by a tenant.

## Decision
We will enforce a single global currency per tenant schema by moving the responsibility of storing currency from individual bookable `Events` to the `CompanyProfile`.

## Implications
1.  **Schema Simplification**: Reduces the number of fields in the `Event` model.
2.  **API Changes**: The `EventSerializer` will no longer provide a `currency` field. Consumers of the API will need to look at the global company configuration if they need to display the currency symbol.
3.  **Admin Experience**: Service creation is faster as the currency is pre-defined for the entire tenant.

## Alternatives Considered
-   **Keeping both**: Allows per-service currency but introduces high complexity for payment integration and data validation.
-   **Moving currency to `EventType`**: Provides more flexibility than a global setting but still introduces redundancy if all event types use the same currency (which is the case for most small to medium businesses).

The global `CompanyProfile` setting is the most robust and simplest approach for the current requirements.
