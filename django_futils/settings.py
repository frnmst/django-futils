#
# settings.py
#
# Copyright (C) 2020-2021 frnmst (Franco Masotti) <franco.masotti@live.com>
#
# This file is part of django-futils.
#
# django-futils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django-futils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django-futils.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Django settings for django-futils project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import sys
from pathlib import Path

from django.utils.translation import gettext_lazy as _
# Required variables.
from SECRET_SETTINGS import (ALLOWED_HOSTS, DB_HOST, DB_NAME, DB_PASSWORD,
                             DB_PORT, DB_USER, DEBUG, INTERNAL_IPS,
                             LANGUAGE_CODE, LOCALE_DIR_SUFFIX, MEDIA_ROOT,
                             MEDIA_URL, SECRET_KEY, STATIC_ROOT_SUFFIX,
                             STATIC_URL, STATICFILES_DIR_SUFFIX, TIME_ZONE,
                             USE_X_FORWARDED_HOST)

import django_futils.constants as const

# Optional variables.
try:
    from SECRET_SETTINGS import GEOCODER_SCHEME
except ImportError:
    pass
try:
    from SECRET_SETTINGS import GEOCODER_DOMAIN
except ImportError:
    pass
try:
    from SECRET_SETTINGS import GEOCODER_USER_AGENT
except ImportError:
    pass
try:
    from SECRET_SETTINGS import GEOCODER_CACHE_TTL_SECONDS
except ImportError:
    pass
try:
    from SECRET_SETTINGS import OPENLAYERS_URL
except ImportError:
    pass
try:
    from SECRET_SETTINGS import FOREIGN_KEY_FIELDS
except ImportError:
    pass
try:
    from SECRET_SETTINGS import SIMPLE_HISTORY_REVERT_DISABLED
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

LOCALE_PATHS = [os.path.join(BASE_DIR, LOCALE_DIR_SUFFIX)]

LANGUAGES = [
    ('it', _('Italian')),
    ('en', _('English')),
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'leaflet',
    'django.contrib.contenttypes',
    'simple_history',
    'vies',
    'phone_field',
    'django_countries',
    'django.contrib.gis',
    'django_extensions',
    'import_export',
    'django_futils.apps.DjangoFutilsConfig',
    'django_futils.apps.DjangoFutilsDefaultAdminConfig',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'django_futils.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

# Disable caching for debug so we can test the templates without reloading
# the server.
if DEBUG:
    TEMPLATES[0]['APP_DIRS'] = True
else:
    TEMPLATES[0]['APP_DIRS'] = False
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        (
            'django.template.loaders.cached.Loader',
            [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        ),
    ]

WSGI_APPLICATION = 'django_futils.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'TEST': {
            'MIGRATE': True,
        },
    }
}

# See
# https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_ROOT_SUFFIX)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, STATICFILES_DIR_SUFFIX),
]

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

LEAFLET_CONFIG = {
    'RESET_VIEW': False,
    # 'TILES': 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'SCALE': 'metric',
    # 'ATTRIBUTION_PREFIX': 'django-leaflet. Maps OpenStreetMap contributors',
}

HTML_MINIFY = True

AUTH_USER_MODEL = 'django_futils.User'

# Unit tests.
if 'test' in sys.argv:
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.CryptPasswordHasher',
    ]
