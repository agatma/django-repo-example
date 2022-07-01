"""
Django settings for Example project.
"""

from pathlib import Path
from typing import Any

from environ import Env  # type: ignore

env = Env()

BASE_DIR = Path(__file__).resolve().parent.parent
env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('EXAMPLE_SECRET_KEY')
DEBUG = env.bool('EXAMPLE_DEBUG', default=False)

ALLOWED_HOSTS: list[str] = env.list('EXAMPLE_ALLOWED_HOSTS', default=[])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'example.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES: dict[str, Any] = {
    'default': env.db('EXAMPLE_DB_URL', 'sqlite:////tmp/tmp-sqlite.db')
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'site-static'
STATICFILES_DIRS = ()

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'DEBUG' if DEBUG else 'INFO',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format':
                '%(asctime)s | %(levelname)s | %(name)s | '
                '%(filename)s %(funcName)s:%(lineno)d | %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'urllib3': {
            'level': 'INFO'
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': None,
    'VERSION_PARAM': 'version',
    'SEARCH_PARAM': 'q',
    'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser'],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

HEALTH_CHECKS = [
    'example.health.checks.postgres',
]
