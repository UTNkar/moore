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
        'NAME': os.environ.get('DJANGO_DB'),
        'USER': os.environ.get('DJANGO_DB_USER'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASS'),
        'HOST': os.environ.get('DJANGO_DB_HOST', '127.0.0.1'),
        'PORT':  os.environ.get('DJANGO_DB_PORT', '5432'),
    }
}

# Admins - will be sent error messages
ADMINS = [('UTN System Administrator', 'admin@utn.se')]

try:
    from .local import *
except ImportError:
    pass
