# backend/project/settings.py
from pathlib import Path
import os
from datetime import timedelta

import environ

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # .../backend/project -> /backend
REPO_ROOT = BASE_DIR.parent                        # repo root (one level up)

# -----------------------------------------------------------------------------
# Environment
# -----------------------------------------------------------------------------
env = environ.Env()
# Load .env from repo root if present, otherwise from backend/.env (optional)
env_file_repo = REPO_ROOT / ".env"
env_file_backend = BASE_DIR / ".env"
if env_file_repo.exists():
    environ.Env.read_env(str(env_file_repo))
elif env_file_backend.exists():
    environ.Env.read_env(str(env_file_backend))

# -----------------------------------------------------------------------------
# Core
# -----------------------------------------------------------------------------
SECRET_KEY = env("SECRET_KEY", default="dev-secret-key-change-me")
DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=["http://localhost:5173"])

# In dev, allow all CORS if you prefer (comment out if not desired)
CORS_ALLOW_ALL_ORIGINS = DEBUG and not CORS_ALLOWED_ORIGINS

# -----------------------------------------------------------------------------
# Applications
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "rest_framework_simplejwt",
    # Local apps
    "apps.vendors",
    "apps.shops",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve static files in prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # add template dirs if needed
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

# -----------------------------------------------------------------------------
# Database (Django built-ins stay on SQLite)
# -----------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# -----------------------------------------------------------------------------
# Password validation
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------------------------------------
# Internationalization
# -----------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIME_ZONE", default="Asia/Kolkata")
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------------------
# Static files (WhiteNoise)
# -----------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Optional WhiteNoise optimization
WHITENOISE_MAX_AGE = 60 * 60 * 24 * 365  # 1 year

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------------------------------------------------
# DRF & JWT
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# JWT lifetimes from env
ACCESS_MIN = env.int("JWT_ACCESS_LIFETIME_MIN", default=10)
REFRESH_DAYS = env.int("JWT_REFRESH_LIFETIME_DAYS", default=7)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_MIN),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_DAYS),
    # You can override signing key via env if needed:
    "SIGNING_KEY": env("JWT_SIGNING_KEY", default=SECRET_KEY),
}

# -----------------------------------------------------------------------------
# CORS / CSRF
# -----------------------------------------------------------------------------
# If CORS_ALLOW_ALL_ORIGINS is True (dev), CORS_ALLOWED_ORIGINS list is ignored.
# For production, set DEBUG=False and populate CORS_ALLOWED_ORIGINS & CSRF_TRUSTED_ORIGINS.
CORS_ALLOW_CREDENTIALS = True

# -----------------------------------------------------------------------------
# MongoDB (MongoEngine) — for Shops domain data
# -----------------------------------------------------------------------------
MONGODB_URI = env("MONGODB_URI", default="")
if MONGODB_URI:
    try:
        from mongoengine import connect
        connect(host=MONGODB_URI, alias="default")
    except Exception as e:
        # Avoid crashing at import-time in case of ephemeral envs; log to stdout
        print(f"[MongoEngine] Connection deferred/failed: {e}")

# -----------------------------------------------------------------------------
# Production security hardening (safe defaults; tune per-host)
# -----------------------------------------------------------------------------
if not DEBUG:
    SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0)  # enable >0 when using HTTPS
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
    SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)
    CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=False)
    SECURE_REFERRER_POLICY = "same-origin"
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

# -----------------------------------------------------------------------------
# Optional: log which .env was loaded (useful in logs)
# -----------------------------------------------------------------------------
if env_file_repo.exists():
    ENV_FILE = env_file_repo
elif env_file_backend.exists():
    ENV_FILE = env_file_backend
else:
    ENV_FILE = None
print(f"[settings] DEBUG={DEBUG} | ENV_FILE={ENV_FILE} | BASE_DIR={BASE_DIR}")
