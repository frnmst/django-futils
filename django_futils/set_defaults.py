#
# set_defaults.py
#
# Copyright (C) 2020 frnmst (Franco Masotti) <franco.masotti@live.com>
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

from django.conf import settings
import django_futils.constants as const

# Set variables if the user did not set them.
try:
    settings.NOMINATIM_MODEL_NAME
except AttributeError:
    settings.NOMINATIM_MODEL_NAME = 'NominatimCache'
try:
    settings.NOMINATIM_MODEL_APP
except AttributeError:
    settings.NOMINATIM_MODEL_APP = 'django_futils'
try:
    settings.NOMINATIM_URL
except AttributeError:
    settings.NOMINATIM_URL = 'https://nominatim.openstreetmap.org'
try:
    settings.NOMINATIM_CACHE_TTL_SECONDS
except AttributeError:
    # 6 months = 60 * 60 * 24 * 30 * 6
    settings.NOMINATIM_CACHE_TTL_SECONDS = 15552000
try:
    settings.OPENLAYERS_URL
except AttributeError:
    settings.OPENLAYERS_URL = 'https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'
try:
    settings.FOREIGN_KEY_FIELDS
except AttributeError:
    # The way foreign keys and onetoone fields are displayed.
    # 0=default
    # 1=raw
    # 2=autocomplete
    settings.FOREIGN_KEY_FIELDS = 1
try:
    settings.SIMPLE_HISTORY_REVERT_DISABLE
except AttributeError:
    settings.SIMPLE_HISTORY_REVERT_DISABLE = False

# Validate the custom secret settings.
if not isinstance(settings.NOMINATIM_MODEL_NAME, str):
    raise TypeError
if not isinstance(settings.NOMINATIM_MODEL_APP, str):
    raise TypeError
if not isinstance(settings.NOMINATIM_URL, str):
    raise TypeError
if not isinstance(settings.NOMINATIM_CACHE_TTL_SECONDS, int):
    raise TypeError
if not isinstance(settings.OPENLAYERS_URL, str):
    raise TypeError
if not isinstance(settings.FOREIGN_KEY_FIELDS, int):
    raise TypeError
if not isinstance(settings.SIMPLE_HISTORY_REVERT_DISABLE, bool):
    raise TypeError
if settings.NOMINATIM_CACHE_TTL_SECONDS <= 0:
    raise ValueError
if settings.FOREIGN_KEY_FIELDS != const.FOREIGN_KEY_FIELDS_DEFAULT and settings.FOREIGN_KEY_FIELDS != const.FOREIGN_KEY_FIELDS_RAW and settings.FOREIGN_KEY_FIELDS != const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
    raise ValueError
