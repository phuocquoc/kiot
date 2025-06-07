import os
from pathlib import Path
import environ
from datetime import timedelta


# Khởi tạo đối tượng `env` để đọc biến môi trường
env = environ.Env()

# Đọc file .env (nếu có)
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, '.env'))

# Khai báo thư mục gốc của dự án
BASE_DIR = Path(__file__).resolve().parent.parent

# Cài đặt thông tin SECRET_KEY (bảo mật)
SECRET_KEY = env("SECRET_KEY", default="django-insecure-your-secret-key")

# Cài đặt Debug (dành cho môi trường phát triển)
DEBUG = env.bool("DEBUG", default=True)

# Danh sách các host được phép
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

# Cài đặt cơ sở dữ liệu
# Kiểm tra nếu môi trường là production, sử dụng PostgreSQL. Nếu không, sử dụng SQLite.

if env("DJANGO_ENV", default="development") == "production":
    # Sử dụng PostgreSQL khi triển khai lên production
    DATABASES = {
        'default': env.db()  # Lấy thông tin từ DATABASE_URL trong file .env
    }
else:
    # Sử dụng SQLite khi phát triển trên localhost
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',  # Đường dẫn tới file db.sqlite3
        }
    }

# Cài đặt các ứng dụng đã cài đặt trong Django
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'rest_framework',
    'corsheaders',
    'customer',  # App api chính
    'invoice',
    'product',
    'stock',
    'user',
]

# Cài đặt các middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Cấu hình thông tin URL của project
ROOT_URLCONF = "kiot.urls"

# Cài đặt templates
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

# WSGI Application
WSGI_APPLICATION = "kiot.wsgi.application"

# Khai báo các trình xác thực mật khẩu
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
]

# Cài đặt internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Đường dẫn đến thư mục Media (nếu có)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Các cài đặt bảo mật
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "https://quanli-a392d0279e04.herokuapp.com",
]

# Chế độ CORS (cho phép tất cả trong môi trường phát triển)
CORS_ALLOW_ALL_ORIGINS = True

# Cấu hình JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# Sử dụng file .env để lưu các biến môi trường
SECRET_KEY = env("SECRET_KEY", default="django-insecure-your-secret-key")
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])



# Cấu hình Staticfiles Storage (WhiteNoise cho phép phục vụ static files)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Cấu hình SASS/SCSS hoặc TailwindCSS nếu sử dụng
TAILWIND_APP_NAME = 'theme'

# Cài đặt ứng dụng gửi email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Thay đổi khi triển khai

# Đảm bảo rằng Django biết về môi trường mà ứng dụng đang chạy
if env("DJANGO_ENV", default="development") == "development":
    print("App đang chạy ở môi trường development")
else:
    print("App đang chạy ở môi trường production")

AUTH_USER_MODEL = 'user.User'

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}