"""
Django settings for python_anywhere project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import sys
from pathlib import Path

from environ import Env, ImproperlyConfigured

env = Env(DEBUG=(bool, False))

# directory of python_anywhere project
PROJECT_DIR = Path(__file__).resolve().parent
# directory of bouldern-app
BASE_DIR = PROJECT_DIR.parent
# parent directory of bouldern-app
USER_HOME = BASE_DIR.parent
RESOURCES_DIR = BASE_DIR / 'frontend' / 'cypress' / 'fixtures'

sys.path = list({str(USER_HOME / project_name) for project_name in
                 ['googleCalendarApp', 'GoogleApiHelper'] + sys.path})

Env.read_env(str(USER_HOME / ".env"))

# Security

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

DOMAIN_NAME = 'api.humorloos.pythonanywhere.com'

ALLOWED_HOSTS = [
    DOMAIN_NAME,
]

# in debug, add django and vue dev server to allowed hosts
if DEBUG:
    ALLOWED_HOSTS += [
        '127.0.0.1',
    ]

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

CORS_ORIGIN_ALLOW_ALL = False
if DEBUG:
    CORS_ORIGIN_WHITELIST = (f'https://{VUE_DEV_SERVER_DOMAIN_NAME}',)

# Application definition

INSTALLED_APPS = [
    'colorfield',
    'dj_rest_auth',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'python_anywhere.bouldern',
    'python_anywhere.registration',
    'rest_framework',
    'rest_framework.authtoken',
    'sslserver',
    'webpack_loader',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'python_anywhere.middleware.MoveJWTRefreshCookieIntoTheBody'
]

ROOT_URLCONF = 'python_anywhere.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_DIR / 'templates'],
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

WSGI_APPLICATION = 'python_anywhere.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    PROJECT_DIR / 'static',
    PROJECT_DIR / 'bouldern' / 'static',
]

STATIC_ROOT = USER_HOME / 'static'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# Spatialite
try:
    SPATIALITE_LIBRARY_PATH = env('SPATIALITE_LIBRARY_PATH')
except ImproperlyConfigured:
    pass

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Vue
VUE_FRONTEND_DIR = BASE_DIR / 'frontend'

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'vue/',  # must end with slash
        'STATS_FILE': VUE_FRONTEND_DIR / 'webpack-stats.json',
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}

# Authentication
BOULDERN_URL_SEGMENT = 'bouldern'

LOGIN_REDIRECT_URL = '/' + BOULDERN_URL_SEGMENT

LOGOUT_REDIRECT_URL = '/' + BOULDERN_URL_SEGMENT

AUTH_USER_MODEL = 'registration.User'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django_server.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Rest
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'auth-token'
JWT_AUTH_REFRESH_COOKIE = 'refresh-token'
REST_SESSION_LOGIN = False
JWT_AUTH_SECURE = True
