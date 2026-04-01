# Spec Delta: Settings Configuration for `django-tenants`

## ADDED Requirements

### Requirement: Database Engine Update 
The Database Engine SHALL be updated.
Update `DATABASES['default']` to use `django_tenants.postgresql_backend`.

#### Scenario: `DATABASES` configuration
- Change `'ENGINE': 'django.db.backends.postgresql'` (or other) to `'django_tenants.postgresql_backend'`.

### Requirement: Middleware Configuration 
The Middleware Configuration SHALL be updated.
Add `TenantMainMiddleware` to the beginning of `MIDDLEWARE`.

#### Scenario: `MIDDLEWARE` order
- `django_tenants.middleware.main.TenantMainMiddleware` must be first.

### Requirement: Database Routers Configuration 
The Database Routers Configuration SHALL be updated.
Add `TenantSyncRouter` to `DATABASE_ROUTERS`.

#### Scenario: `DATABASE_ROUTERS` configuration
- `['django_tenants.routers.TenantSyncRouter']` must be in the list.

### Requirement: Application Separation 
The Application Separation SHALL be implemented.
Split `INSTALLED_APPS` into `SHARED_APPS` and `TENANT_APPS`.

#### Scenario: `SHARED_APPS` configuration
- Include `django_tenants`, `companies`, `django.contrib.admin`, `django.contrib.auth`, `django.contrib.contenttypes`, `django.contrib.sessions`, `django.contrib.messages`, `django.contrib.staticfiles`, `unfold`, `corsheaders`, `rest_framework`, `solo`, `storages`.

#### Scenario: `TENANT_APPS` configuration
- Include `scheduler`, `django.contrib.contenttypes`.

#### Scenario: `TENANT_MODEL` and `TENANT_DOMAIN_MODEL`
- `TENANT_MODEL = 'companies.Client'`.
- `TENANT_DOMAIN_MODEL = 'companies.Domain'`.
