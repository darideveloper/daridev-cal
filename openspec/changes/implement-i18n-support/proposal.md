# Proposal: Implement i18n Support

## Scope: Static vs. Dynamic Translations

- **Phase 1 (This Proposal):** Implement static i18n to translate core application interface elements (templates, Python files like `verbose_name`, and the Unfold admin theme).
- **Phase 2 (Future):** Implement database content translation (e.g., using `django-parler` or `django-modeltranslation`) if dynamic content translation is required for models like `Service`.


This proposal outlines the implementation of internationalization (i18n) and localization (l10n) for the Daridev-Cal project, enabling multi-language support for the user interface.

**Capability Specs**
- `specs/django-settings/spec.md`
- `specs/project-wiring/spec.md`
- `specs/admin-theme/spec.md`
- `specs/booking/spec.md`
- `specs/companies/spec.md`
- `specs/scheduler/spec.md`
