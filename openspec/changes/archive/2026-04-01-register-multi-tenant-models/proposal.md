# Proposal: Register Multi-Tenant Models

## Summary
Implement a multi-tenant architecture using `django-tenants` for data isolation per company. This involves creating a `companies` app for shared tenant data and a `scheduler` app for tenant-specific scheduling data, while integrating with the `django-unfold` admin theme.

## Why
As specified in `docs/pr.md`, the platform requires independent companies to manage their own booking rules and event types with total data isolation. `django-tenants` provides PostgreSQL schema-level isolation, which aligns with this requirement.

## What Changes
- **Infrastructure**: Install `django-tenants==3.10.1` and `django-cryptography-5==2.0.3` (fork for Django 5.x support).
- **Shared App (`companies`)**: Define `Client` (Tenant) and `Domain` models to manage tenant routing.
- **Tenant App (`scheduler`)**: Define `CompanyProfile`, `EventType`, and `Booking` models for the scheduling logic.
- **Settings Configuration**: Update `project/settings.py` with multi-tenant settings (DATABASE_ROUTERS, SHARED_APPS, TENANT_APPS, etc.).
- **Admin Integration**: Register models with `django-unfold` for a modern administrative UI, ensuring tenant-aware branding.
- **Validation**: Implement overlap check logic in `Booking.clean()` based on the `EventType.allow_overlap` flag.
