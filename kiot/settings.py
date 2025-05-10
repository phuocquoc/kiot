import os
from datetime import timedelta
from pathlib import Path
import dj_database_url
import sys

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Secret key (để đơn giản, bạn nên tự tạo mới khi deploy)
SECRET_KEY = "django-insecure-your-secret-key"

# Debug bật lên cho local
DEBUG = False

ALLOWED_HOSTS = ["http://127.0.0.1:8000","https://quanli-a392d0279e04.herokuapp.com"]

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
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "corsheaders.middleware.CorsMiddleware",
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


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


SESSION_COOKIE_SECURE = True  # Chỉ gửi cookie qua HTTPS
CSRF_COOKIE_SECURE = True     # Chỉ gửi cookie CSRF qua HTTPS
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000","https://quanli-a392d0279e04.herokuapp.com"]

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_SSL_REDIRECT = True