"""
Django settings for the production environment of Project Moore.

For more information regarding running in production see,
See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
from __future__ import absolute_import, unicode_literals
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET',
    'za7^0@54n&p-dg4)_l12q_3^o5awz_uym0osqaz2!myki_8kw0'
)

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DJANGO_DB_NAME', 'moore'),
        'USER': os.environ.get('DJANGO_DB_USER', 'moore'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASS'),
        'HOST': os.environ.get('DJANGO_DB_HOST', '127.0.0.1'),
        'PORT':  os.environ.get('DJANGO_DB_PORT', '5432'),
    }
}

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# CONN_MAX_AGE = 0

# Base URL to use when referring to full URLs within the Wagtail admin
# backend - e.g. in notification emails. Don't include '/admin' or a
# trailing slash
BASE_URL = 'https://utn.se'

ALLOWED_HOSTS = ['.utn.se', '.utnarm.se']

# Email settings
DEFAULT_FROM_EMAIL = 'info@utn.se'

EMAIL_SUBJECT_PREFIX = '[UTN] '

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

MELOS_URL = os.environ.get('MELOS_URL')
MELOS_ORG_ID = os.environ.get('MELOS_ORG_ID')
MELOS_ADMIN = os.environ.get('MELOS_ADMIN')

# Google API
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY", "")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY", "")

try:
    from .local import *
except ImportError:
    pass

KRONOS_PREFIX = (
    'export SENTRY_DSN="{0}" &&'.format(os.environ.get("SENTRY_DSN"))
)
