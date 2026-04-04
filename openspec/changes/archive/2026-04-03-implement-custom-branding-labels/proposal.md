---
change-id: implement-custom-branding-labels
title: Implement Customizable UI Labels in Company Profile
status: proposed
author: Gemini CLI
date: 2026-04-03
---

# Change: Implement Customizable UI Labels in Company Profile

## Why
Currently, UI labels like "Event Type", "Event", and "Free" are hardcoded in the frontend. Different tenants (e.g., tours, medical consultations, classes) require different terminology. This change allows each tenant to define their own labels, providing a more professional and tailored experience for their clients.

## What Changes
- **MODIFIED** `CompanyProfile` model: Added 6 new fields for custom UI labels.
- **MODIFIED** `CompanyConfigSerializer`: Exposed the 6 new fields in the API.
- **MODIFIED** `CompanyConfigView`: Updated to include the new labels in the `/api/config/` response.
- **MODIFIED** `CompanyProfileAdmin`: Added a "UI Labels" tab to group the new settings.
- **MODIFIED** `docs/api.md`: Updated API documentation with the new response fields.

## Impact
- **Affected specs**: `specs/companies/spec.md` (or creating a new branding capability if it fits better).
- **Affected code**: `scheduler/models.py`, `scheduler/serializers.py`, `scheduler/views.py`, `scheduler/admin.py`.
- **API**: `GET /api/config/` response schema has changed (added fields).
