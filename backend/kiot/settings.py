import os
from datetime import timedelta
from pathlib import Path
import dj_database_url
import sys


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key (để đơn giản, bạn nên tự tạo mới khi deploy)
SECRET_KEY = "django-insecure-your-secret-key"

# Debug bật lên cho local
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "customer",  # App api chính
    "invoice",
    "product",
    "stock",
    "user",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "kiot.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "kiot.wsgi.application"


DATABASES = {
    'default': dj_database_url.config(
        default="postgres://postgres.xlenlfgqsqqsvhasbfcr:bKUb9QaNqFz08ZOh@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"

# Default auto field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model (nếu dùng sau này)
# AUTH_USER_MODEL = 'users.User'

# Django REST Framework Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

# JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True


AUTH_USER_MODEL = "user.User"

SESSION_COOKIE_DOMAIN = '192.168.1.7'

CSRF_TRUSTED_ORIGINS = [
    'http://192.168.1.7:8000',  # Thay IP bằng IP LAN máy bạn
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
