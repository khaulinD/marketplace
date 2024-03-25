from datetime import timedelta
from pathlib import Path
import os
from dotenv import load_dotenv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')



ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
# Application definition
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost"
]



AUTH_USER_MODEL = 'customers.Account'

INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # -----------------------------
    'rest_framework',
    'drf_spectacular',
    "debug_toolbar",
    'django_filters',
    "corsheaders",
    'rest_framework_simplejwt',
    "channels",
    # -----------------------------
    "customers",
    "users_work",
    "users_resume",
    "webchat"
]
SITE_ID = 1

REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # "customers.authenticate.JWTCookieAuthentication",
    )
}


MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # -------------------------------------------------------

]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # 'ROTATE_REFRESH_TOKENS': True,
    # 'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_COOKIE': 'Authorization',
    "TOKEN_OBTAIN_SERIALIZER": "customers.serializers.account_serializer.CustomTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "customers.serializers.account_serializer.JWTCookieTokenRefreshSerializer",
    'AUTH_TOKEN_CLASSES': (  # --new
        'rest_framework_simplejwt.tokens.AccessToken',  # --new
    ),
    "ACCESS_TOKEN_NAME": "access_token",
    "REFRESH_TOKEN_NAME": "refresh_token",
    "JWT_COOKIE_SAMESITE": "Lax"
    ""
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Marketplace API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
    # 'AUTHENTICATION_CLASSES': [
    #     'customers.openapi_auth_extensions.JWTCookieAuthenticationExtension',
    # ],
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

ROOT_URLCONF = 'django_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_api.wsgi.application'
ASGI_APPLICATION = "django_api.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    "formatters": {
        "main_format": {
            "format": "{asctime} - {levelname} - {module} - {filename}:{lineno} - {message}",
            "style": "{"
        },
    },
    'handlers': {  # where and how logging are being processed
        "console": {
            "class": "logging.StreamHandler"
        },
        "django_file": {
            "class": "logging.FileHandler",  # push logging in file
            "filename": "django_info.log",
            "formatter": "main_format"
        },

    },
    "loggers": {  # the main process of logging, doing main work
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG"
        },
        "django_api": {  # django.db.backends
                "handlers": ["django_file"],
                "level": "ERROR",  # Lvl of debugging: DEBUG, INFO, WARNING, ERROR, CRITICAL
                "propagate": True
            },
        },

}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}