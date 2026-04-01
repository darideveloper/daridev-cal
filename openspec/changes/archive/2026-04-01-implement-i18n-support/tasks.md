# Tasks: Implement i18n Support

- [x] **[django-settings]** In `project/settings.py`, define the `LANGUAGES` and `LOCALE_PATHS` settings.
- [x] **[django-settings]** In `project/settings.py`, insert `django.middleware.locale.LocaleMiddleware` between `SessionMiddleware` and `CommonMiddleware`.
- [x] **[admin-theme]** In `project/settings.py`, add `"SHOW_LANGUAGES": True` to the `UNFOLD` configuration dictionary.
- [x] **[project-wiring]** In `project/urls.py` and `project/urls_public.py`, add the `i18n` URL include and wrap admin URLs with `i18n_patterns`.
- [x] **[project-wiring]** Replace the hardcoded `RedirectView(url='/admin/')` with a language-aware version using `pattern_name='admin:index'`.
- [x] **[apps]** Add translatable `verbose_name` to `BookingConfig`, `CompaniesConfig`, and `SchedulerConfig`.
- [x] **[models]** In `scheduler/models.py`, wrap all field names, `help_text`, and `choices` (Weekdays, Statuses) with `gettext_lazy`.
- [x] **[models]** In `companies/models.py`, add translatable `verbose_name` and `verbose_name_plural` to `Client` and `Domain`.
- [x] **[services]** In `scheduler/services.py`, wrap all `ValidationError` messages with `gettext_lazy`.
- [x] **[utils]** In `utils/callbacks.py`, translate environment names and site header/subheader strings.
- [x] **[admin]** In `project/admin.py`, translate custom action descriptions like `@action(description="Edit")`.
- [x] **[frontend]** Rename `range_date_filter_es.js` to a generic name and modify it to accept translatable labels from the template.
- [x] **[setup]** Create the `locale/es/LC_MESSAGES` directory in the project root.
- [x] **[l10n]** Execute `python manage.py makemessages -l es` to generate the Spanish translation source file (`.po`).
- [x] **[l10n]** Populate the generated `django.po` file with Spanish translations for key UI elements.
- [x] **[l10n]** Execute `python manage.py compilemessages` to compile the translations for use.
- [x] **[validate]** Start the development server and confirm that the language switcher appears in the admin UI and correctly switches between English and Spanish.
