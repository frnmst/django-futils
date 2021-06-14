#
# utils.py
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
import django.apps
import geopy
from django.http import HttpResponseRedirect
from django.urls import reverse


def abstract_response_change(self, request, obj, reverse_url):
    r"""Create an admin button which opens a detail view of an object."""
    res = super(type(self), self).response_change(request, obj)
    if "_printable" in request.POST:
        self.hide_message = True
        return HttpResponseRedirect(
            request.build_absolute_uri(reverse(reverse_url,
                                               args=(obj.pk, ))))
    else:
        return res


def save_primary(self, field_name: str, field_value: str):
    r"""One object must always be primary.

        This function avoids the need of implementing this constraint which has
        been remove after commit d67dc41. If needed call the save_primary
        function manually.

        constraints = [
            # This constraint should nevery be hit because of the save method
            # which corrects the error.
            models.UniqueConstraint(
                fields=['person'],
                condition=Q(is_primary=True),
                name='is_primary_persontelephone_costraint'),
    """
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


def run_geocoder_request(street_number: str, street: str, city: str, country_code: str, postal_code: str = str(), provider: str = 'Nominatim') -> tuple:
    r"""See
        https://docs.djangoproject.com/en/3.1/ref/contrib/gis/geos/#geosgeometry
        https://docs.djangoproject.com/en/3.1/ref/contrib/gis/geos/#creating-a-geometry
        https://tools.ietf.org/html/rfc7946#section-9
        https://en.wikipedia.org/wiki/World_Geodetic_System

        Do not get the database dirty if there is a problem reaching the geocoders' servers.
    """
    error = False
    postcode = None
    if provider == 'Nominatim':
        try:
            query_string = {
                'street': street_number + ' ' + street,
                'city': city,
                'country': country_code,
            }
            result = geopy.geocoders.Nominatim(
                timeout=30,
                scheme=settings.GEOCODER_SCHEME,
                domain=settings.GEOCODER_DOMAIN,
                user_agent=settings.GEOCODER_USER_AGENT,
            ).geocode(query=query_string, exactly_one=True, country_codes=country_code, addressdetails=True, geometry='geojson')

            if result is None:
                # No results found.
                # Case 6.
                error = True
            else:
                # Case 0.
                point = GEOSGeometry(str({'type': 'Point', 'coordinates': [result.longitude, result.latitude]}), srid=4326)

                if 'address' in result.raw and 'postcode' in result.raw['address']:
                    # Case 0.
                    postcode = result.raw['address']['postcode']
                else:
                    # case 1.
                    postcode = None

        except geopy.exc.GeopyError as e:
            # Case 5.
            print(e)
            error = True

    if error:
        point = None
    if postcode is None:
        if postal_code is None:
            # Case 3.
            postal_code = str()
        # Case 4.
        postcode = postal_code

    return point, postcode


def get_address_data(country: str, city: str, street_number: str,
                     street: str, postal_code: str,
                     map: django.contrib.gis.geos.point.Point, auto_fill: bool) -> tuple:
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
        country_code = country.lower()
        geocoder_model = django.apps.apps.get_model(settings.GEOCODER_MODEL_APP, settings.GEOCODER_MODEL_NAME)
        try:
            cache = geocoder_model.objects.get(city=city, street_number=street_number, street=street, country_code=country_code)
            if (timezone.now() - cache.updated).seconds >= settings.GEOCODER_CACHE_TTL_SECONDS:
                # Update the cache once it expires.
                point, postcode = run_geocoder_request(street_number, street, city, country_code, postal_code)
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

                # Since we are not changing neither the map nor the postal_code values,
                # replace the updated field with its original value.
                geocoder_model.objects.filter(pk=cache.pk).update(cache_hits=hit, updated=updated)
        except ObjectDoesNotExist:
            # Create the cache.
            point, postcode = run_geocoder_request(street_number, street, city, country_code, postal_code)
            cache = geocoder_model(city=city, street_number=street_number, street=street, country_code=country_code, map=point, postal_code=postcode)
            cache.save()

    # Get the point from the map if the user
    # selected it manually or if the function returns None.
    # In the latter case the point value will remain undefined.
    if point is None:
        point = map

    return point, postcode
