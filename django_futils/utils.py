#
# utils.py
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

from django.utils.timezone import localdate
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Q
import requests
import uuid
import urllib.parse
import django_futils.set_defaults


def save_primary(self, field_name: str, field_value: str):
    r"""One object must always be primary."""
    try:
        obj = type(self).objects.get(Q(**{field_name: field_value}) & Q(is_primary=True))
        if self.is_primary:
            # Change value on the fly.
            type(self).objects.filter(Q(id=obj.id)).update(is_primary=False)
            self.is_primary = True
    except ObjectDoesNotExist:
        self.is_primary = True


# In case of renaming these functions you must change the migration files. See:
# https://groups.google.com/d/msg/django-users/LK8zq-3tDnA/yTF_3XXcl5gJ
def personattachment_directory_path(instance, filename: str) -> str:
    # pk and id do not work on a new object so we use a safe random string.
    return 'personattachments/' + str(uuid.uuid4()) + '/' + filename


def run_nominatim_request(request_url: str, postal_code: str) -> tuple:
    # Do not get the database dirty if there is a problem reaching Nominatims' servers.
    try:
        r = requests.get(request_url)
        j = r.json()
        if j['features'] == list():
            point = None
            postcode = postal_code
        else:
            data = j['features']
            if len(data) > 0:
                if 'geometry' in data[0]:
                    pnt = str(data[0]['geometry'])
                    # See
                    # https://docs.djangoproject.com/en/3.1/ref/contrib/gis/geos/#geosgeometry
                    # https://docs.djangoproject.com/en/3.1/ref/contrib/gis/geos/#creating-a-geometry
                    # https://tools.ietf.org/html/rfc7946#section-9
                    # https://en.wikipedia.org/wiki/World_Geodetic_System
                    point = GEOSGeometry(pnt, srid=4326)
                else:
                    point = None

                if 'properties' in data[0] and 'address' in data[0]['properties'] and 'postcode' in data[0]['properties']['address']:
                    postcode = str(j['features'][0]['properties']['address']['postcode'])
                else:
                    postcode = str()
            else:
                raise ValueError

    except (requests.RequestException, ValueError):
        point = None
        if postal_code is None:
            postal_code = str()
        postcode = postal_code

    return point, postcode


def get_address_data(country: str, city: str, street_number: str,
                     street: str, postal_code: str, auto_fill: bool) -> tuple:
    r"""See
        https://nominatim.org/release-docs/latest/api/Search/
    """
    # To be able to execute the request we need to have all the elements.
    # If something is missing or the user did not opt for auto filling,
    # use the postal code provided by the user and ignore saving the map data.
    if (None in [city, street_number, street, country] or str() in [
            city, street_number, street, country
    ]) or not auto_fill:
        point = None
        if postal_code is None:
            postal_code = str()
        postcode = postal_code
    else:
        # Escape variables and special characters of the url so that it can be validated as a URLField.
        osm_request_url = (settings.NOMINATIM_URL + '/' + urllib.parse.quote('search?format=geojson&limit=1&addressdetails=1&city=' \
            + city + '&street=' + street_number + ', ' + street + '&country=' + country.lower(), safe='?&=/'))

        # Defer  to avoid cirular imports.
        from .models import NominatimCache
        try:
            cache = NominatimCache.objects.get(request_url=osm_request_url)
            if (timezone.now() - cache.updated).seconds > settings.NOMINATIM_CACHE_TTL_SECONDS:
                # Update the cache once it expires.
                point, postcode = run_nominatim_request(request_url=osm_request_url, postal_code=postal_code)
                cache.map = point
                cache.postal_code = postcode
                cache.cache_hits = 0
                cache.save()
            else:
                # Cache hit: get data from cache.
                point = cache.map
                postcode = cache.postal_code
                hit = cache.cache_hits + 1
                updated = cache.updated

                # Replace the updated field with its original value.
                NominatimCache.objects.filter(pk=cache.pk).update(cache_hits=hit, updated=updated)

        except ObjectDoesNotExist:
            # Create the cache.
            point, postcode = run_nominatim_request(request_url=osm_request_url, postal_code=postal_code)
            cache = NominatimCache(request_url=osm_request_url, map=point, postal_code=postcode)
            cache.save()

    return point, postcode
