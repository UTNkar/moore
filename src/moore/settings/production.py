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
SECRET_KEY = config('DJANGO_SECRET')

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

sentry_sdk.init(
    dsn=config("SENTRY_DSN"),
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

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

RECAPTCHA_PUBLIC_KEY = config("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = config("RECAPTCHA_PRIVATE_KEY")

KRONOS_PREFIX = (
    'export SENTRY_DSN="{0}" &&'.format(config("SENTRY_DSN"))
)
