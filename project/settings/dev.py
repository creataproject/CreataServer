from .base import *


# Default Settings

DEBUG = True
ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True

PROJECT_DIR = os.path.dirname(BASE_DIR)
ROOT_DIR = os.path.dirname(PROJECT_DIR)

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'creata',
        'USER': 'postgres',
        'PASSWORD': 'creataq!w@e#',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


INSTALLED_APPS = INSTALLED_APPS + [
    'django_extensions',
]


# WSGI

WSGI_APPLICATION = 'project.wsgi.dev.application'


# Email

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'id@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'creat0214@gmail.com'
DEFAULT_TO_EMAIL = 'creat0214@gmail.com'
DEFAULT_ADMIN_EMAIL = 'creat0214@gmail.net'


# Static Files

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')