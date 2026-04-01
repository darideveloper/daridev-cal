# Tasks: Project Setup - DariDevCal

## `infrastructure`
- [ ] Add `requirements.txt` with pinned versions (Django 5.2, DRF 3.16.1, Unfold 0.77.1, etc.).
- [ ] Initialize virtual environment and install dependencies.
- [ ] Add `.gitignore`.
- [ ] Create `.env`, `.env.dev`, and `.env.prod`.
- [ ] Initialize Git and make initial commit.

## `django-init`
- [ ] Run `django-admin startproject project .`.
- [ ] Run `python manage.py startapp booking`.

## `django-settings`
- [ ] Update `project/settings.py` to initialize `python-dotenv` and load environment-specific files.
- [ ] Configure `INSTALLED_APPS` and `MIDDLEWARE` including `corsheaders`, `rest_framework`, `solo`, `storages`, and `unfold`.
- [ ] Configure dynamic `DATABASES`.
- [ ] Configure `LANGUAGE_CODE`, `TIME_ZONE` ("America/Mexico_City"), `USE_I18N`, and `USE_TZ`.
- [ ] Configure static and media file settings.
- [ ] Implement conditional storage logic (Local vs AWS S3).
- [ ] Configure CORS and CSRF trusted origins from environment variables.
- [ ] Set up Django REST Framework settings.
- [ ] Implement global date/time formatting.
- [ ] Configure SMTP email settings.

## `project-wiring`
- [ ] Update `project/urls.py` with the DRF router, root redirect, and media serving.
- [ ] Create `project/pagination.py` with `CustomPageNumberPagination`.
- [ ] Create `project/storage_backends.py` with custom S3 backends.
- [ ] Create `project/handlers.py` with a custom exception handler.
- [ ] Update `project/admin.py` with Unfold-enabled User and Group models.

## `admin-theme`
- [ ] Create `project/templates/admin/base.html` to extend the Unfold base layout.
- [ ] Create `static/css/style.css`.
- [ ] Create `static/js/copy_clipboard.js`, `static/js/script.js`.
- [ ] Create `static/js/add_tailwind_styles.js`, `static/js/load_markdown.js`, and `static/js/range_date_filter_es.js`.
- [ ] Add placeholder `static/logo.svg` and `static/favicon.png`.
- [ ] Create empty `media/` directory.

## `utilities`
- [ ] Create `utils/admin_helpers.py` (permission logic).
- [ ] Create `utils/automation.py` (Selenium helpers).
- [ ] Create `utils/media.py` (image processing and URL resolution).

## `deployment`
- [ ] Create `Dockerfile`.
- [ ] Create `start.sh` and make it executable.

## `validation`
- [ ] Run `python manage.py check`.
- [ ] Run `python manage.py test` to ensure test-specific database isolation.
- [ ] Run `python manage.py makemigrations` and `python manage.py migrate`.
- [ ] Run `python manage.py createsuperuser` (as needed).
