# Spec: Django Settings

## MODIFIED Requirements

### Requirement: Configure i18n settings

The system MUST be configured to support internationalization.

#### Scenario: English and Spanish Support
- **GIVEN** the project settings
- **WHEN** the application is running
- **THEN** the `LANGUAGES` setting must include English and Spanish
- **AND** `USE_I18N` must be `True`
- **AND** `LOCALE_PATHS` must point to the project's `locale` directory.

### Requirement: Enable Locale Middleware

The system MUST process requests to determine the current language.

#### Scenario: Middleware Activation
- **GIVEN** the project settings
- **WHEN** a request is processed
- **THEN** the `django.middleware.locale.LocaleMiddleware` must be present in the `MIDDLEWARE` list, placed after `SessionMiddleware` and before `CommonMiddleware`.
