---
change-id: improve-field-descriptions
title: Improve i18n and Field Descriptions
description: Update all verbose names and add descriptive help text to complex fields in both Spanish and English to enhance admin usability and clarity.
author: Gemini CLI
status: implemented
created: "2026-04-01"
---

# Proposal: Improve i18n and Field Descriptions

## Goal
To provide a more intuitive and professional administrative experience by refining model and field labels (`verbose_name`, `verbose_name_plural`) and adding contextual `help_text` to complex or required fields. This update ensures that both Spanish-speaking and English-speaking administrators have clear guidance on how to manage the system.

## Scope
- **Applications**: `companies`, `scheduler`.
- **Fields**: All model fields, including `verbose_name` and `help_text` where applicable.
- **Translations**: Ensure all new strings are properly wrapped in `gettext_lazy` and added to `django.po`.

## Rationale
The current labels are basic and sometimes technical. For a multi-tenant booking system, clarity on fields like "Brand Color" (OKLCH support), "Stripe Keys", and "Availability Slots" is crucial for tenant onboarding and troubleshooting.
