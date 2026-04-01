# Spec: Django Init - DariDevCal

This capability defines the initialization of the Django project structure and the main application.

## ADDED Requirements

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
