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

SECRET_KEY = 'django-insecure-g4%+x4o1=ojtwde@^_h81jp$2-71-oi5wp$4=+r+g!^7_2m@@w'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']

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

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Allow admin preview iframes
X_FRAME_OPTIONS = 'SAMEORIGIN'
