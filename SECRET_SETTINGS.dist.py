# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

import os

# MEDIA_ROOT works out of the box for Docker.
if 'DJANGO_ENV' in os.environ:
    if os.environ['DJANGO_ENV'] == 'development':
        MEDIA_ROOT = '/code/db/dev/data/'
    else:
        MEDIA_ROOT = '/code/db/prod/data/'
else:
    MEDIA_ROOT = '/code/db/dev/data/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT_SUFFIX = 'static/'
STATICFILES_DIR_SUFFIX = 'django_futils/static'

LOCALE_DIR_SUFFIX = 'locale/'

MEDIA_URL = '/media/'
INTERNAL_IPS = ['127.0.0.1', 'myhost']

# SECURITY WARNING: keep the secret key used in production secret!
# Use
# pipenv run python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
# to generate a new one.
SECRET_KEY = '^q9lj(7k@lws95p+syeju58#f#4w$03&5*1o&w)!1727%&ci%+'

# SECURITY WARNING: don't run with debug turned on in production!
if 'APP_DEBUG' in os.environ:
    DEBUG = False if os.environ['APP_DEBUG'] == 'False' else True
else:
    DEBUG = True

if DEBUG:
    USE_X_FORWARDED_HOST = False
    ALLOWED_HOSTS = ['127.0.0.1', 'myhost']
else:
    USE_X_FORWARDED_HOST = True
    ALLOWED_HOSTS = ['*']

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'it'
TIME_ZONE = 'Europe/Rome'

###############
# Other stuff #
###############
NOMINATIM_URL = 'https://nominatim.openstreetmap.org'

# 6 months = 60 * 60 * 24 * 30 * 6
NOMINATIM_CACHE_TTL_SECONDS = 15552000

OPENLAYERS_URL = 'https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'

# The way foreign keys and onetoone fields are displayed.
# 0=default
# 1=raw
# 2=autocomplete
FOREIGN_KEY_FIELDS = 1

# django-simple-history
SIMPLE_HISTORY_REVERT_DISABLED = True

############
# Database #
############
# Bare metal.

# DB_NAME = 'futils'
# DB_USER = 'futils'
# DB_PASSWORD = 'futils'
# DB_HOST = '127.0.0.1'
# DB_PORT = '5432'

# Docker.
if 'DJANGO_ENV' in os.environ:
    if os.environ['DJANGO_ENV'] == 'development':
        DB_NAME = 'postgres_dev'
    else:
        DB_NAME = 'postgres_prod'
else:
    DB_NAME = 'postgres_dev'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'db'
DB_PORT = '5432'
