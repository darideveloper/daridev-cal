# Design: Project Setup - DariDevCal

This design document outlines the architectural decisions and patterns for the "DariDevCal" Django project setup.

## Environment-Variable-First Configuration
We will use a multi-tiered environment configuration approach:
- `.env`: Global entry point (sets `ENV`, `SECRET_KEY`, and shared settings).
- `.env.dev`: Local development overrides (SQLite/Local Storage defaults).
- `.env.prod`: Production-ready placeholders (PostgreSQL/AWS S3 templates).

`python-dotenv` will be used at the start of `settings.py` to load these files sequentially.

## Dynamic Infrastructure
The project will dynamically switch between:
- **Database**: PostgreSQL for live environments, SQLite for isolated testing.
- **Storage**: Local filesystem for development, AWS S3 for production.
- **Security**: Environment-specific `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, and `CSRF_TRUSTED_ORIGINS`.

## Modern Admin Interface
We will integrate `django-unfold` for a modern, responsive administrative experience, including:
- Custom base templates to include external JS/CSS for markdown and date ranges.
- Enhanced `User` and `Group` model admins.
- Tailwind-styled admin components.

## API Architecture
- **Framework**: Django REST Framework (DRF).
- **Standardization**: Custom exception handlers and pagination to ensure consistent API responses.
- **Security**: Token-based and session-based authentication classes as defaults.

## Deployment Strategy
The project is containerized using a multi-stage-ready `Dockerfile` and a `start.sh` script to automate migrations and start Gunicorn. This setup is optimized for platforms like Coolify.
