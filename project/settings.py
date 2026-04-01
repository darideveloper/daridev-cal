import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env first to get ENV value
load_dotenv(BASE_DIR / ".env")
ENV = os.getenv("ENV", "dev")

# Load environment-specific file
load_dotenv(BASE_DIR / f".env.{ENV}")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")


# Application definition

# Shared Apps (Public Schema)
SHARED_APPS = (
    # unfold
    "unfold",  # Modern admin theme
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    # Multi-tenant apps
    "django_tenants",  # mandatory
    "companies",  # your public app
    # Third party apps
    "corsheaders",
    "rest_framework",
    "solo",
    "storages",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)

# Tenant Apps (Isolated Schemas)
TENANT_APPS = (
    # The following Django apps are required in TENANT_APPS
    "django.contrib.contenttypes",
    # Isolated apps
    "scheduler",
    "booking",
)

# Combined INSTALLED_APPS for Django
INSTALLED_APPS = list(SHARED_APPS) + [
    app for app in TENANT_APPS if app not in SHARED_APPS
]

# Tenancy Settings
TENANT_MODEL = "companies.Client"
TENANT_DOMAIN_MODEL = "companies.Domain"
DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)

MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",  # Mandatory first
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static file serving
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS handling
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
PUBLIC_SCHEMA_URLCONF = "project.urls_public"
ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "project" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "project.context_processors.branding",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

import sys

IS_TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

if IS_TESTING:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "testing.sqlite3"),
        }
    }
else:
    options = {}
    if os.environ.get("DB_ENGINE") == "django.db.backends.mysql":
        options = {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        }

    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.sqlite3"),
            "NAME": os.environ.get("DB_NAME", os.path.join(BASE_DIR, "db.sqlite3")),
            "USER": os.environ.get("DB_USER", ""),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", ""),
            "OPTIONS": options,
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Mexico_City"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
MEDIA_URL = "/media/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Conditional Storage (AWS S3 vs Local)
STORAGE_AWS = os.getenv("STORAGE_AWS") == "True"

if STORAGE_AWS:
    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
    AWS_PROJECT_FOLDER = os.getenv("AWS_PROJECT_FOLDER")

    STATIC_LOCATION = "static"
    PUBLIC_MEDIA_LOCATION = "media"
    PRIVATE_MEDIA_LOCATION = "private"

    STORAGES = {
        "default": {
            "BACKEND": "project.storage_backends.PublicMediaStorage",
        },
        "staticfiles": {
            "BACKEND": "project.storage_backends.StaticStorage",
        },
        "private": {
            "BACKEND": "project.storage_backends.PrivateMediaStorage",
        },
    }
else:
    # Local Storage Configuration
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

# CORS & CSRF Configuration
cors_allowed = os.getenv("CORS_ALLOWED_ORIGINS")
if cors_allowed and cors_allowed != "None":
    CORS_ALLOWED_ORIGINS = [
        origin.strip().rstrip("/")
        for origin in cors_allowed.split(",")
        if origin.strip()
    ]

csrf_trusted = os.getenv("CSRF_TRUSTED_ORIGINS")
if csrf_trusted and csrf_trusted != "None":
    CSRF_TRUSTED_ORIGINS = [
        origin.strip().rstrip("/")
        for origin in csrf_trusted.split(",")
        if origin.strip()
    ]

# Django REST Framework Setup
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "project.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 12,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "EXCEPTION_HANDLER": "project.handlers.custom_exception_handler",
}

# Global DateTime Formatting
DATE_FORMAT = "d/b/Y"
TIME_FORMAT = "H:i"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"

# Email SMTP Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL") == "True"
EMAIL_FROM = EMAIL_HOST_USER
EMAILS_NOTIFICATIONS = os.getenv("EMAILS_NOTIFICATIONS", "").split(",")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

from django.templatetags.static import static
from django.urls import reverse, NoReverseMatch
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _


def safe_reverse(viewname, *args, **kwargs):
    try:
        return reverse(viewname, *args, **kwargs)
    except NoReverseMatch:
        return "#"


safe_reverse_lazy = lazy(safe_reverse, str)

UNFOLD = {
    "SITE_TITLE": "utils.callbacks.site_title_callback",
    "SITE_HEADER": "utils.callbacks.site_header_callback",
    "SITE_SUBHEADER": "utils.callbacks.site_subheader_callback",
    "SITE_URL": "/",
    "SITE_ICON": "utils.callbacks.site_icon_callback",
    "SITE_SYMBOL": "calendar_today",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png",
            "href": lambda request: static("favicon.ico"),
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "utils.callbacks.environment_callback",
    "THEME": "light",
    "COLORS": {
        "primary": {
            "50": "oklch(0.98 0.02 236)",
            "100": "oklch(0.95 0.04 236)",
            "200": "oklch(0.91 0.07 236)",
            "300": "oklch(0.86 0.09 236)",
            "400": "var(--brand-primary-400, oklch(0.83 0.10 236))",
            "500": "var(--brand-primary-500, oklch(0.81 0.11 236))",
            "600": "var(--brand-primary-600, oklch(0.72 0.10 236))",
            "700": "oklch(0.63 0.09 236)",
            "800": "oklch(0.54 0.08 236)",
            "900": "oklch(0.45 0.07 236)",
            "950": "oklch(0.36 0.06 236)",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("System"),
                "separator": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": safe_reverse_lazy("admin:auth_user_changelist"),
                        "permission": lambda request: request.tenant.schema_name
                        == "public",
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": safe_reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.tenant.schema_name
                        == "public",
                    },
                ],
            },
            {
                "title": _("Multi-Tenancy"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Clients (Tenants)"),
                        "icon": "corporate_fare",
                        "link": safe_reverse_lazy("admin:companies_client_changelist"),
                        "permission": lambda request: request.tenant.schema_name
                        == "public",
                    },
                    {
                        "title": _("Domains"),
                        "icon": "public",
                        "link": safe_reverse_lazy("admin:companies_domain_changelist"),
                        "permission": lambda request: request.tenant.schema_name
                        == "public",
                    },
                ],
            },
            {
                "title": _("Booking App"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Company Profile"),
                        "icon": "settings",
                        "link": safe_reverse_lazy(
                            "admin:scheduler_companyprofile_changelist"
                        ),
                        "permission": lambda request: request.tenant.schema_name
                        != "public",
                    },
                    {
                        "title": _("Event Types"),
                        "icon": "event_note",
                        "link": safe_reverse_lazy(
                            "admin:scheduler_eventtype_changelist"
                        ),
                        "permission": lambda request: request.tenant.schema_name
                        != "public",
                    },
                    {
                        "title": _("Bookings"),
                        "icon": "calendar_month",
                        "link": safe_reverse_lazy("admin:scheduler_booking_changelist"),
                        "permission": lambda request: request.tenant.schema_name
                        != "public",
                    },
                ],
            },
        ],
    },
}
