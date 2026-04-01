# Proposal: Implement i18n Support

## Scope: Interface Translation

Implement static i18n to translate core application interface elements (templates, Python files like `verbose_name`, and the Unfold admin theme). This includes:
    - Model metadata (`verbose_name`, `verbose_name_plural`).
    - Model field attributes (`verbose_name`, `help_text`, `choices`).
    - Service-layer and view validation error messages.
    - Admin UI callbacks and custom actions.
    - Language-aware URL redirections.
    - Generalized static assets for multi-language support.

This proposal outlines the implementation of internationalization (i18n) and localization (l10n) for the Daridev-Cal project, enabling multi-language support for the user interface.

**Capability Specs**
- `specs/django-settings/spec.md`
- `specs/project-wiring/spec.md`
- `specs/admin-theme/spec.md`
- `specs/booking/spec.md`
- `specs/companies/spec.md`
- `specs/scheduler/spec.md`
