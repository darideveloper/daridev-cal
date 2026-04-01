# Tasks: Project Setup - DariDevCal

## `infrastructure`
- [x] Add `requirements.txt` with pinned versions (Django 5.2, DRF 3.16.1, Unfold 0.77.1, etc.).
- [x] Initialize virtual environment and install dependencies.
- [x] Add `.gitignore`.
- [x] Create `.env`, `.env.dev`, and `.env.prod`.
- [x] Initialize Git and make initial commit.

## `django-init`
- [x] Run `django-admin startproject project .`.
- [x] Run `python manage.py startapp booking`.

## `django-settings`
- [x] Update `project/settings.py` to initialize `python-dotenv` and load environment-specific files.
- [x] Configure `INSTALLED_APPS` and `MIDDLEWARE` including `corsheaders`, `rest_framework`, `solo`, `storages`, and `unfold`.
- [x] Configure dynamic `DATABASES`.
- [x] Configure `LANGUAGE_CODE`, `TIME_ZONE` ("America/Mexico_City"), `USE_I18N`, and `USE_TZ`.
- [x] Configure static and media file settings.
- [x] Implement conditional storage logic (Local vs AWS S3).
- [x] Configure CORS and CSRF trusted origins from environment variables.
- [x] Set up Django REST Framework settings.
- [x] Implement global date/time formatting.
- [x] Configure SMTP email settings.

## `project-wiring`
- [x] Update `project/urls.py` with the DRF router, root redirect, and media serving.
- [x] Create `project/pagination.py` with `CustomPageNumberPagination`.
- [x] Create `project/storage_backends.py` with custom S3 backends.
- [x] Create `project/handlers.py` with a custom exception handler.
- [x] Update `project/admin.py` with Unfold-enabled User and Group models.

## `admin-theme`
- [x] Create `project/templates/admin/base.html` to extend the Unfold base layout.
- [x] Create `static/css/style.css`.
- [x] Create `static/js/copy_clipboard.js`, `static/js/script.js`.
- [x] Create `static/js/add_tailwind_styles.js`, `static/js/load_markdown.js`, and `static/js/range_date_filter_es.js`.
- [x] Add placeholder `static/logo.svg` and `static/favicon.png`.
- [x] Create empty `media/` directory.

## `utilities`
- [x] Create `utils/admin_helpers.py` (permission logic).
- [x] Create `utils/automation.py` (Selenium helpers).
- [x] Create `utils/media.py` (image processing and URL resolution).

## `deployment`
- [x] Create `Dockerfile`.
- [x] Create `start.sh` and make it executable.

## `validation`
- [x] Run `python manage.py check`.
- [x] Run `python manage.py test` to ensure test-specific database isolation.
- [x] Run `python manage.py makemigrations` and `python manage.py migrate`.
- [x] Run `python manage.py createsuperuser` (as needed).
