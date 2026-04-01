# Design: Register Multi-Tenant Models

## Architecture
The system follows a **Shared Database, Isolated Schemas** approach. Each `Client` corresponds to a unique PostgreSQL schema. Requests are routed via subdomains using the `Domain` model.

### Key Components
- **Public Schema (Shared):** Contains `Client`, `Domain`, and system-wide authentication (`User`, `Group`).
- **Tenant Schemas (Isolated):** Contains `CompanyProfile`, `EventType`, and `Booking`.

## Data Model Details

### App: `companies` (Public)
| Model | Inherits | Key Fields |
| :--- | :--- | :--- |
| **Client** | `TenantMixin` | `schema_name`, `name`, `is_active` |
| **Domain** | `DomainMixin` | `domain`, `tenant`, `is_primary` |

### App: `scheduler` (Tenant)
| Model | Key Fields | Purpose |
| :--- | :--- | :--- |
| **CompanyProfile** | `stripe_secret_key` (Encrypted), `google_calendar_id`, `logo` | Tenant-specific config. |
| **EventType** | `title`, `duration_minutes`, `price`, `payment_model` (PRE/POST), `allow_overlap` | Service definitions. |
| **Booking** | `event_type`, `client_name`, `client_email`, `start_time`, `end_time`, `status` | Individual appointments. |

## Administrative Interface
- **Theme:** `django-unfold` with `TenantAdminMixin` for `Client` and `Domain`.
- **Tenant Isolation:** Admin views for `scheduler` models are automatically scoped to the active tenant.
- **Dynamic Branding:** The `UNFOLD` settings should eventually reflect the active `CompanyProfile` branding.

## Validation & Business Logic
- **Overlap Conflict Rule:** $(\text{NewStart} < \text{ExistingEnd}) \text{ AND } (\text{NewEnd} > \text{ExistingStart})$
- **Status badges:** In `BookingAdmin`, status will be rendered using Unfold's label component.
