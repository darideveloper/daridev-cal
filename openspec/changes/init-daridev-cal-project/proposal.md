# Proposal: Project Setup - DariDevCal

Set up the core infrastructure, Django project, and application for the "DariDevCal" booking/schedule system.

## Problem
Currently, there is no project structure for the DariDevCal booking/schedule system. We need to initialize the project with a robust Django configuration following the project's standard setup guide.

## Solution
Initialize a Django project with:
- `requirements.txt` with all necessary dependencies (Django 5.2, DRF, Unfold, etc.).
- Environment-variable-first configuration using `python-dotenv`.
- Dynamic database selection (PostgreSQL for dev/prod, SQLite for testing).
- Conditional storage (Local or S3).
- Custom DRF settings, exception handling, and pagination.
- Modern Django Admin theme (Unfold).
- Deployment-ready Dockerfile and start script.

## Capabilities
- `infrastructure`: Core environment files, requirements (pinned versions), and Git initialization.
- `django-init`: Django project and `booking` app initialization.
- `django-settings`: Advanced settings configuration for security, API, and storage.
- `project-wiring`: Global URL patterns, pagination, handlers, and storage backends.
- `admin-theme`: Custom admin layouts, static assets (including Tailwind and Markdown scripts), and placeholders.
- `utilities`: Reusable helpers for admin permissions, media processing, and automation.
- `deployment`: Containerization scripts.

## Strategy
1.  Establish the basic file structure and dependencies with pinned versions.
2.  Initialize the Django project and the main `booking` app.
3.  Configure `settings.py` for flexibility and production readiness.
4.  Implement custom wiring files (pagination, handlers, etc.).
5.  Set up the modern admin theme and required static JavaScript assets.
6.  Implement reusable utility modules (`utils/`).
7.  Add deployment scripts for Docker.
8.  Perform final validation (including test isolation check).
