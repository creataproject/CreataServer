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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'db.sqlite3'),
    }
}


INSTALLED_APPS = INSTALLED_APPS + [
    'django_extensions',
]



# WSGI

WSGI_APPLICATION = 'project.wsgi.dev.application'


# Static Files

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')