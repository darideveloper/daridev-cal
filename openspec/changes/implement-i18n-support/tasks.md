# Tasks: Implement i18n Support

- [ ] **[django-settings]** In `project/settings.py`, define the `LANGUAGES` and `LOCALE_PATHS` settings.
- [ ] **[django-settings]** In `project/settings.py`, insert `django.middleware.locale.LocaleMiddleware` into the `MIDDLEWARE` list at the correct position.
- [ ] **[admin-theme]** In `project/settings.py`, add `"SHOW_LANGUAGES": True` to the `UNFOLD` configuration dictionary.
- [ ] **[project-wiring]** In both `project/urls.py` and `project/urls_public.py`, add the `i18n` URL include for language switching.
- [ ] **[project-wiring]** In both `project/urls.py` and `project/urls_public.py`, wrap the admin URL patterns with `i18n_patterns`.
- [ ] **[booking]** In `booking/apps.py`, add a translatable `verbose_name` to the `BookingConfig`.
- [ ] **[companies]** In `companies/apps.py`, add a translatable `verbose_name` to the `CompaniesConfig`.
- [ ] **[scheduler]** In `scheduler/apps.py`, add a translatable `verbose_name` to the `SchedulerConfig`.
- [ ] **[setup]** Create the `locale/es/LC_MESSAGES` directory in the project root.
- [ ] **[l10n]** Execute `python manage.py makemessages -l es` to generate the Spanish translation source file (`.po`).
- [ ] **[l10n]** Populate the generated `django.po` file with Spanish translations for key UI elements.
- [ ] **[l10n]** Execute `python manage.py compilemessages` to compile the translations for use.
- [ ] **[validate]** Start the development server and confirm that the language switcher appears in the admin UI and correctly switches between English and Spanish.
