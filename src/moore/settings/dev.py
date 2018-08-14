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


if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
elif 'DOCKER' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'moore',
            'USER': 'moore',
            'HOST': 'moore-db',
            'PORT': 5432,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'moore',
            'USER': 'moore',
            'HOST': '127.0.0.1',
            'PORT': 5432,
        }
    }

# Base URL to use when referring to full URLs within the Wagtail admin
# backend - e.g. in notification emails. Don't include '/admin' or a
# trailing slash
BASE_URL = 'http://localhost:8000'

# Email
# https://docs.djangoproject.com/en/1.10/ref/settings/#email-backend

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'info@localhost'

# Membership API
MEMBERSHIP_API_USER = 'test'
MEMBERSHIP_API_PASSWORD = 'test'

# Google API
GOOGLE_API_KEY = 'my_google_api_key'

# Instagram API
INSTAGRAM_ACCESS_TOKEN = 'my_instagram_access_token'

# Facebook API
FACEBOOK_APP_ID = 'my_facebook_app_id'

try:
    from .local import *
except ImportError:
    pass
