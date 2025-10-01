"""
Django settings for hmd project.
"""
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# One level above the project (override via env on server)
WORKSPACE_DIR = Path(os.environ.get("HMD_WORKSPACE_DIR", BASE_DIR.parent))

# External admin assets and templates
DEFAULT_ADMIN_ASSETS = BASE_DIR.parent / "admin_assets"
ADMIN_ASSETS_DIR = Path(os.environ.get("ADMIN_ASSETS_DIR") or DEFAULT_ADMIN_ASSETS)
ADMIN_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
ADMIN_TEMPLATES_DIR = WORKSPACE_DIR / "admin_templates"
TEMPLATE_DIRS = [BASE_DIR / "templates"]
if ADMIN_TEMPLATES_DIR.exists():
    TEMPLATE_DIRS.append(ADMIN_TEMPLATES_DIR)

# Security / environment-aware settings
# Read sensitive values from environment in production. For local development you can
# set DJANGO_DEBUG=True and optionally provide a DJANGO_SECRET_KEY. In production
# set DJANGO_DEBUG=False and provide DJANGO_SECRET_KEY and ALLOWED_HOSTS.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# DEBUG can be controlled with the DJANGO_DEBUG env var (default True for local dev)
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('1', 'true', 'yes')

# ALLOWED_HOSTS can be a comma-separated list provided via env (useful for deploys)
raw_allowed = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost,testserver')
ALLOWED_HOSTS = [h.strip() for h in raw_allowed.split(',') if h.strip()]

# Ensure a SECRET_KEY is present in production
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured('The DJANGO_SECRET_KEY environment variable must be set in production')
    # fallback development key (kept for convenience in local dev only)
    SECRET_KEY = 'django-insecure-g4%+x4o1=ojtwde@^_h81jp$2-71-oi5wp$4=+r+g!^7_2m@@w'

INSTALLED_APPS = [
    "analytics.apps.AnalyticsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pages",
    "core",
    "ai_engine",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hmd.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Use TEMPLATE_DIRS so project-level templates and optional admin_templates are found
        "DIRS": TEMPLATE_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# extra context processors
TEMPLATES[0]["OPTIONS"]["context_processors"] += [
    "core.context_processors.site_constants",
    "core.context_processors.diensten_ticker",
]

WSGI_APPLICATION = "hmd.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Amsterdam"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
if ADMIN_ASSETS_DIR.exists():
    STATICFILES_DIRS.append(ADMIN_ASSETS_DIR)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "justcodeworks@gmail.com"
EMAIL_HOST_PASSWORD = "your-16-char-app-password"
DEFAULT_FROM_EMAIL = "noreply@localhost"

# Allow admin preview iframes
X_FRAME_OPTIONS = 'SAMEORIGIN'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Allow admin preview iframes
# Where to redirect users after logout (safe default)
LOGOUT_REDIRECT_URL = '/'
# After login, redirect users to the admin dashboard by default
LOGIN_REDIRECT_URL = '/admin/'

# Production security recommendations when DEBUG is False
if not DEBUG:
    # Use HTTPS in production (set to True when you have TLS terminated)
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() in ('1', 'true', 'yes')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True').lower() in ('1', 'true', 'yes')
    SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', 'True').lower() in ('1', 'true', 'yes')
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
