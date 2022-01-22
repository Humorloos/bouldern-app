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

from corsheaders.defaults import default_headers
from environ import Env, ImproperlyConfigured

env = Env(DEBUG=(bool, False))

# directory of python_anywhere project
PROJECT_DIR = Path(__file__).resolve().parent
# directory of bouldern-app
BASE_DIR = PROJECT_DIR.parent
# parent directory of bouldern-app
USER_HOME = BASE_DIR.parent
# directory of vue frontend
VUE_FRONTEND_DIR = BASE_DIR / 'frontend'
RESOURCES_DIR = VUE_FRONTEND_DIR / 'cypress' / 'fixtures'
# target of vue sources when building for production
VUE_OUTPUT_DIR = VUE_FRONTEND_DIR / 'dist'

sys.path = list({str(USER_HOME / project_name) for project_name in
                 ['googleCalendarApp', 'GoogleApiHelper'] + sys.path})

Env.read_env(str(USER_HOME / ".env"))

# Security

SECRET_KEY = env('SECRET_KEY')

DEVELOPMENT = env('DEBUG')
DEBUG = DEVELOPMENT
PIPELINE = env('PIPELINE') == 'True'
DOMAIN_NAME = 'humorloos.pythonanywhere.com'
BOULDERN_URL_SEGMENT = 'bouldern'

ALLOWED_HOSTS = [
    DOMAIN_NAME,
]

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

CORS_ALLOW_ALL_ORIGINS = False

# Allow access from android app
CORS_ALLOWED_ORIGINS = ['http://localhost']

# in debug, add django and vue dev server to allowed hosts
if DEVELOPMENT:
    HOST_NAME = 'localhost'
    VUE_DEV_SERVER_DOMAIN_NAME = f'{HOST_NAME}:8080'
    ALLOWED_HOSTS += [
        HOST_NAME,
    ]
    CORS_ALLOWED_ORIGINS = [f'https://{VUE_DEV_SERVER_DOMAIN_NAME}']
    CORS_ALLOW_HEADERS = list(default_headers)

# Application definition

INSTALLED_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'colorfield',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'python_anywhere.bouldern',
    'python_anywhere.accounts',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_gis',
    'sslserver',
    'webpack_loader',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'python_anywhere.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            VUE_OUTPUT_DIR,
        ],
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

TIME_ZONE = 'Europe/Berlin'

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    VUE_OUTPUT_DIR / 'assets',
]

STATIC_ROOT = USER_HOME / 'static'

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

# Authentication

AUTH_USER_MODEL = 'accounts.User'

if DEVELOPMENT:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = CYPRESS_DIR / 'logs' / 'email'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7

JWT_AUTH_RETURN_EXPIRATION = True
# only send jwt tokens via https
JWT_AUTH_SECURE = True
REST_SESSION_LOGIN = False

# Logging
if PIPELINE:
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

# Site settings
SITE_ID = 1

# Rest
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}
REST_USE_JWT = True
