"""
Django settings for the development environment of Project Moore.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l0gkw_q4rgex=0%ep84(yw$gx+mxr)u1e-x5yv@2j)a%(4=1!s'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin
# backend - e.g. in notification emails. Don't include '/admin' or a
# trailing slash
BASE_URL = 'http://127.0.0.1:8000'

# E-mail
# https://docs.djangoproject.com/en/1.10/ref/settings/#email-backend

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'info@localhost'

# Membership API
MEMBERSHIP_API_USER = 'test'
MEMBERSHIP_API_PASSWORD = 'test'

try:
    from .local import *
except ImportError:
    pass
