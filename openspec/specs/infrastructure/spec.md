# infrastructure Specification

## Purpose
TBD - created by archiving change init-daridev-cal-project. Update Purpose after archive.
## Requirements
### Requirement: Environment Configuration Files
The project SHALL use environment-variable-first configuration using `.env`, `.env.dev`, and `.env.prod`.

#### Scenario: Global Environment File
- **Given** I am in the project root
- **When** I create `.env`
- **Then** it SHALL contain `ENV=dev`, a randomly generated `SECRET_KEY`, and shared SMTP settings.

#### Scenario: Environment Overrides
- **Given** I am in the project root
- **When** I create `.env.dev` and `.env.prod`
- **Then** they SHALL contain environment-specific `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, and database credentials.

### Requirement: Dependency Management
The project SHALL maintain a `requirements.txt` file with all necessary frameworks and libraries using pinned or minimum stable versions.

#### Scenario: Core Dependencies
- **Given** I am in the project root
- **When** I create `requirements.txt`
- **Then** it SHALL include `Django>=5.2`, `djangorestframework>=3.16.1`, `django-unfold==0.77.1`, `psycopg>=3.2.3`, `python-dotenv>=1.0.1`, and `whitenoise>=6.11.0`.

### Requirement: Version Control Initialization
The project SHALL be initialized as a Git repository with an appropriate `.gitignore`.

#### Scenario: Git Setup
- **Given** I am in the project root
- **When** I run `git init` and create `.gitignore`
- **Then** standard temporary files, virtual environments, and sensitive `.env` files SHALL be excluded from tracking.

