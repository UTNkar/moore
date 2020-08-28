"""
Django settings for Project Moore.

This file contains the shared settings. See development.py
and production.py for environment specific settings.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

from __future__ import absolute_import, unicode_literals

from django.conf.global_settings import LOGIN_URL
from django.utils.translation import ugettext_lazy as _

import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Application definition

INSTALLED_APPS = [
    'blocks',
    'branding',
    'google',
    'home',
    'involvement',
    'instagram',
    'materialize',
    'members',
    'news',
    'search',
    'moore',  # include for templatetags

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.settings',
    'wagtail.contrib.modeladmin',
    "wagtail.contrib.routable_page",
    'wagtail.api.v2',
    'wagtailmedia',

    'compressor',
    'kronos',
    'modelcluster',
    'raven.contrib.django.raven_compat',
    'rules.apps.AutodiscoverRulesConfig',
    'simple_email_confirmation',
    'taggit',
    'wagtailfontawesome',
    'django_instagram',

    'django.contrib.admin',  # Used for wagtail admin filters
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'moore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
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

WSGI_APPLICATION = 'moore.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Stockholm'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en', _('English')),
    ('sv', _('Swedish'))
]

LOCALE_PATHS = ['locale']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # Compressor
    'compressor.finders.CompressorFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

FILE_UPLOAD_PERMISSIONS = 0o644

# Compressor
# https://django-compressor.readthedocs.io/en/latest/settings/

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

COMPRESS_FILTERS = {
    "css": [
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.rCSSMinFilter'
    ]
}

# Authentication settings

AUTH_USER_MODEL = 'members.Member'

AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]

# Password hashers
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# Email address used to send errors.
# https://docs.djangoproject.com/en/1.10/ref/settings/#server-email
SERVER_EMAIL = 'moore@utn.se'

# Wagtail settings

WAGTAIL_SITE_NAME = "Uppsala teknolog- och naturvetarkår"
WAGTAIL_FRONTEND_LOGIN_URL = LOGIN_URL

WAGTAIL_USER_EDIT_FORM = 'members.forms.CustomUserEditForm'
WAGTAIL_USER_CREATION_FORM = 'members.forms.CustomUserCreationForm'
WAGTAIL_USER_CUSTOM_FIELDS = ['registration_year', 'study',
                              'status', 'section']

IS_RUNNING_TEST = 'test' in sys.argv

INSTAGRAM_APP_ID = os.environ.get('INSTAGRAM_APP_ID')
INSTAGRAM_APP_SECRET = os.environ.get('INSTAGRAM_APP_SECRET')
INSTAGRAM_REDIRECT_URL = os.environ.get('INSTAGRAM_REDIRECT_URL')
