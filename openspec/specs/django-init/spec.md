# django-init Specification

## Purpose
TBD - created by archiving change init-daridev-cal-project. Update Purpose after archive.
## Requirements
### Requirement: Project Initialization
The Django project structure SHALL be created using `django-admin`.

#### Scenario: Start Project
- **Given** I am in the project root
- **When** I run `django-admin startproject project .`
- **Then** a `project/` directory containing `settings.py`, `urls.py`, `wsgi.py`, and `asgi.py` SHALL be created.

### Requirement: Application Creation
A main application named `booking` SHALL be created.

#### Scenario: Start App
- **Given** I am in the project root
- **When** I run `python manage.py startapp booking`
- **Then** a `booking/` directory SHALL be created.

