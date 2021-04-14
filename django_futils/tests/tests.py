#
# tests.py
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

from django.test import TestCase, TransactionTestCase
from ..default_models import PersonTelephone, GeocoderCache
from model_bakery import baker
import decimal
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from unittest import mock
from django.utils import timezone
from ..utils import get_address_data, run_geocoder_request
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
import geopy


##########
# Models #
##########
class PersonTelephoneTestCase(TestCase):
    r"""test
        CompanyTelephoneTestCase
        PersonEmailTestCase
        CompanyEmailTestCase
        PersonAddressTestCase
        CompanyAddressTestCase
        Company
    """
    def setUp(self):
        self.person = baker.make('Person')
        self.telephonetype = baker.make('TelephoneType')
        self.persontelephone_1 = baker.make('PersonTelephone',
                                   number='112233',
                                   is_primary=False,
                                   type=self.telephonetype,
                                   person=self.person)

    def test_constraints_duplicate_elements(self):
        r"""Same type, number and person."""
        with self.assertRaises(IntegrityError):
            self.persontelephone_2 = baker.make('PersonTelephone',
                                       number='112233',
                                       type=self.telephonetype,
                                       person=self.person)

    def test_constraints_duplicate_is_primary(self):
        r"""This constraint should nevery be hit because of the save method which corrects the error."""

    def test_save_new(self):
        # Re-read the data from the database. If we read from
        # the local variables we cannot track the changes.
        # Get the data from the setUp method.
        t1 = PersonTelephone.objects.first()
        self.assertEqual(t1.is_primary, True)

    def test_save_new_as_non_primary(self):
        self.persontelephone_2 = baker.make('PersonTelephone',
                                       number='112234',
                                       is_primary=False,
                                       type=self.telephonetype,
                                       person=self.person)

        # Re-read the data from the database. If we read from
        # the local variables we cannot track the changes.
        t1 = PersonTelephone.objects.first()
        t2 = PersonTelephone.objects.last()
        self.assertEqual(t1.is_primary, True)
        self.assertEqual(t2.is_primary, False)

    def test_save_new_as_primary(self):
        self.persontelephone_2 = baker.make('PersonTelephone',
                                       number='112234',
                                       is_primary=True,
                                       type=self.telephonetype,
                                       person=self.person)

        # Re-read the data from the database. If we read from
        # the local variables we cannot track the changes.
        t1 = PersonTelephone.objects.first()
        t2 = PersonTelephone.objects.last()
        self.assertEqual(t1.is_primary, False)
        self.assertEqual(t2.is_primary, True)

    def test_clean(self):
        r"""Test assignment to a new Person."""
        self.person_2 = baker.make('Person')
        self.persontelephone_1.person = self.person_2
        with self.assertRaises(ValidationError):
            self.persontelephone_1.full_clean()


#########
# Utils #
#########

DEFAULT_CITY = 'c'
DEFAULT_STREET = 's'
DEFUALT_STREET_NUMBER = '1'
DEFAULT_POSTCODE = '1234'
DEFAULT_LON = -10.0000001
DEFAULT_LAT = -20.0000001
DEFAULT_COUNTRY = 'c'
DEFAULT_COUNTRY_CODE = 'c'

NOMINATIM_JSON_OK = {
    "geojson": {
        "coordinates": [
            DEFAULT_LON,
            DEFAULT_LAT
        ],
        "type": "Point"
    },
    "address": {
        "city": DEFAULT_CITY,
        "postcode": DEFAULT_POSTCODE,
        "road": DEFAULT_STREET,
    }
}
NOMINATIM_JSON_MISSING_POSTCODE_0 = {
    "geojson": {
        "coordinates": [
            DEFAULT_LON,
            DEFAULT_LAT
        ],
        "type": "Point"
    },
    "address": {
        "city": DEFAULT_CITY,
        "road": DEFAULT_STREET,
    }
}
NOMINATIM_JSON_MISSING_POSTCODE_1 = {
    "geojson": {
        "coordinates": [
            DEFAULT_LON,
            DEFAULT_LAT
        ],
        "type": "Point"
    },
}
NOMINATIM_JSON_MISSING_GEOJSON = {
    "address": {
        "city": DEFAULT_CITY,
        "postcode": DEFAULT_POSTCODE,
        "road": DEFAULT_STREET,
    }
}
NOMINATIM_JSON_MISSING = {}

GEOCODER_CACHE_TTL_SECONDS_HIT = float('inf')
GEOCODER_CACHE_TTL_SECONDS_MISS = 0


# Mocks.
def mock_date():
    return timezone.make_aware(timezone.datetime(year=1970, month=2, day=1))


# Change the date function in the Django builtin modules (in this test module)
# and in the utils module.
@mock.patch('django.utils.timezone.now', mock_date)
class UtilsTestCase(TestCase):
    def setUp(self):
        self.city = DEFAULT_CITY
        self.street_number = DEFUALT_STREET_NUMBER
        self.street = DEFAULT_STREET
        self.country = DEFAULT_COUNTRY
        self.country_code = DEFAULT_COUNTRY_CODE

    def test_get_address_data_no_data_returned(self):
        # case: None (no data returned)
        x = 'a',
        y = None
        z = str()
        # Some permutations of possible values in the first function conditional
        # statement.
        perms = [[x, x, x, y], [x, x, y, x], [x, y, x, x], [y, x, x, x], [x, x, x, z], [x, x, z, x], [x, z, x, x], [z, x, x, x]]

        i = 0
        for e in perms:
            country = perms[i][0]
            city = perms[i][1]
            street = perms[i][2]
            street_number = perms[i][3]

            # Existing postal code.
            postal_code = 'a'
            auto_fill = True
            point, postcode = get_address_data(country, city, street_number, street, postal_code, auto_fill)
            self.assertEqual(point, None)
            self.assertEqual(postcode, 'a')

            # Empty string postal code.
            postal_code = str()
            auto_fill = True
            point, postcode = get_address_data(country, city, street_number, street, postal_code, auto_fill)
            self.assertEqual(point, None)
            self.assertEqual(postcode, str())

            # Empty postal code.
            postal_code = None
            auto_fill = True
            point, postcode = get_address_data(country, city, street_number, street, postal_code, auto_fill)
            self.assertEqual(point, None)
            self.assertEqual(postcode, str())

            i += 1

    def test_get_address_data_no_autofill(self):
        postal_code = None
        auto_fill = False
        point, postcode = get_address_data(self.country, self.city, self.street_number, self.street, postal_code, auto_fill)
        self.assertEqual(point, None)
        self.assertEqual(postcode, str())

    def test_get_address_data_cache_miss_mew_autofill(self):
        # Case: autofill new.
        # Cache miss because it is new.
        postal_code = None
        auto_fill = True
        with mock.patch('django_futils.utils.run_geocoder_request', return_value=(None, str())):
            point, postcode = get_address_data(self.country, self.city, self.street_number, self.street, postal_code, auto_fill)

        c = GeocoderCache.objects.first()
        self.assertEqual(c.street, self.street)
        self.assertEqual(c.street_number, self.street_number)
        self.assertEqual(c.street, self.street)
        self.assertEqual(c.country_code, self.country.lower())
        self.assertEqual(c.cache_hits, 0)
        self.assertEqual(c.postal_code, str())
        self.assertEqual(c.map, None)
        self.assertEqual(point, None)
        self.assertEqual(postcode, str())

    def test_get_address_data_cache_hit_autofill(self):
        postal_code = None
        auto_fill = True
        with mock.patch('django_futils.utils.run_geocoder_request', return_value=(None, str())):
            with mock.patch('django.conf.settings.GEOCODER_CACHE_TTL_SECONDS', GEOCODER_CACHE_TTL_SECONDS_HIT):
                point, postcode = get_address_data(self.country, self.city, self.street_number, self.street, postal_code, auto_fill)

        c = GeocoderCache.objects.first()
        # Get the pervious value.
        updated = c.updated
        postal_code = None
        auto_fill = True
        with mock.patch('django_futils.utils.run_geocoder_request', return_value=(None, str())):
            with mock.patch('django.conf.settings.GEOCODER_CACHE_TTL_SECONDS', GEOCODER_CACHE_TTL_SECONDS_HIT):
                point, postcode = get_address_data(self.country, self.city, self.street_number, self.street, postal_code, auto_fill)

        c = GeocoderCache.objects.first()
        self.assertEqual(c.street, self.street)
        self.assertEqual(c.street_number, self.street_number)
        self.assertEqual(c.street, self.street)
        self.assertEqual(c.country_code, self.country.lower())
        self.assertEqual(c.cache_hits, 1)
        self.assertEqual(c.postal_code, str())
        self.assertEqual(c.map, None)
        self.assertEqual(point, None)
        self.assertEqual(postcode, str())
        self.assertEqual(c.updated, updated)

    def test_get_address_data_cache_miss_expiry_autofill(self):
        postal_code = None
        auto_fill = True
        with mock.patch('django_futils.utils.run_geocoder_request', return_value=(None, str())):
            with mock.patch('django.conf.settings.GEOCODER_CACHE_TTL_SECONDS', GEOCODER_CACHE_TTL_SECONDS_MISS):
                point, postcode = get_address_data(self.country, self.city, self.street_number, self.street, postal_code, auto_fill)

        c = GeocoderCache.objects.first()
        # Get the pervious value.
        postal_code = None
        auto_fill = True
        # Simulate a cache expiry also by returning None.
        with mock.patch('django_futils.utils.run_geocoder_request', return_value=(None, str())):
            with mock.patch('django.conf.settings.GEOCODER_CACHE_TTL_SECONDS', GEOCODER_CACHE_TTL_SECONDS_MISS):
                import django.conf
                point, postcode = get_address_data(self.country, self.city, self.street_number, self.street, postal_code, auto_fill)

        c = GeocoderCache.objects.first()
        self.assertEqual(c.street, self.street)
        self.assertEqual(c.street_number, self.street_number)
        self.assertEqual(c.street, self.street)
        self.assertEqual(c.country_code, self.country.lower())
        self.assertEqual(c.cache_hits, 0)
        self.assertEqual(c.postal_code, str())
        self.assertEqual(c.map, None)
        self.assertEqual(point, None)
        self.assertEqual(postcode, str())

    # Case 0.
    def test_run_geocoder_request_ok(self):
        pnt = GEOSGeometry(str(NOMINATIM_JSON_OK['geojson']), srid=4326)
        with mock.patch('django_futils.utils.geopy.geocoders.Nominatim.geocode', return_value=mock.Mock(address=DEFUALT_STREET_NUMBER + ' ' + DEFAULT_STREET, point=geopy.Point(DEFAULT_LAT, DEFAULT_LON), raw=NOMINATIM_JSON_OK)):
            point, postcode = run_geocoder_request(self.street_number, self.street, self.city, self.country_code)
        self.assertEqual(point, pnt)
        self.assertEqual(postcode, DEFAULT_POSTCODE)

    # Case 1.
    def test_run_geocoder_request_missing_postcode(self):
        pnt = GEOSGeometry(str(NOMINATIM_JSON_MISSING_POSTCODE_0['geojson']), srid=4326)
        with mock.patch('django_futils.utils.geopy.geocoders.Nominatim.geocode', return_value=mock.Mock(address=DEFUALT_STREET_NUMBER + ' ' + DEFAULT_STREET, point=geopy.Point(DEFAULT_LAT, DEFAULT_LON), raw=NOMINATIM_JSON_MISSING_POSTCODE_0)):
            point, postcode = run_geocoder_request(self.street_number, self.street, self.city, self.country_code)
        self.assertEqual(point, pnt)
        self.assertEqual(postcode, str())

        pnt = GEOSGeometry(str(NOMINATIM_JSON_MISSING_POSTCODE_1['geojson']), srid=4326)
        with mock.patch('django_futils.utils.geopy.geocoders.Nominatim.geocode', return_value=mock.Mock(address=DEFUALT_STREET_NUMBER + ' ' + DEFAULT_STREET, point=geopy.Point(DEFAULT_LAT, DEFAULT_LON), raw=NOMINATIM_JSON_MISSING_POSTCODE_1)):
            point, postcode = run_geocoder_request(self.street_number, self.street, self.city, self.country_code, str())
        self.assertEqual(point, pnt)
        self.assertEqual(postcode, str())

    # Case 2.
    def test_run_nominatim_request_missing_geojson(self):
        with mock.patch('django_futils.utils.geopy.geocoders.Nominatim.geocode', return_value=mock.Mock(address=DEFUALT_STREET_NUMBER + ' ' + DEFAULT_STREET, point=geopy.Point(DEFAULT_LAT, DEFAULT_LON), raw=NOMINATIM_JSON_MISSING_GEOJSON)):
            point, postcode = run_geocoder_request(self.street_number, self.street, self.city, self.country_code, str())
        self.assertEqual(point, None)
        self.assertEqual(postcode, DEFAULT_POSTCODE)

    # Case 1 and 2.
    def test_run_nominatim_request_missing_raw(self):
        with mock.patch('django_futils.utils.geopy.geocoders.Nominatim.geocode', return_value=mock.Mock(address=DEFUALT_STREET_NUMBER + ' ' + DEFAULT_STREET, point=geopy.Point(DEFAULT_LAT, DEFAULT_LON), raw=NOMINATIM_JSON_MISSING)):
            point, postcode = run_geocoder_request(self.street_number, self.street, self.city, self.country_code, str())
        self.assertEqual(point, None)
        self.assertEqual(postcode, str())

    # Case 3.
    def test_run_geocoder_request_input_postal_code_none(self):
        pnt = GEOSGeometry(str(NOMINATIM_JSON_MISSING_POSTCODE_0['geojson']), srid=4326)
        with mock.patch('django_futils.utils.geopy.geocoders.Nominatim.geocode', return_value=mock.Mock(address=DEFUALT_STREET_NUMBER + ' ' + DEFAULT_STREET, point=geopy.Point(DEFAULT_LAT, DEFAULT_LON), raw=NOMINATIM_JSON_MISSING_POSTCODE_0)):
            point, postcode = run_geocoder_request(self.street_number, self.street, self.city, self.country_code, None)
        self.assertEqual(point, pnt)
        self.assertEqual(postcode, str())

    # Case 4.
    def test_run_geocoder_request_input_postal_code_override(self):
        pnt = GEOSGeometry(str(NOMINATIM_JSON_MISSING_POSTCODE_0['geojson']), srid=4326)
        with mock.patch('django_futils.utils.geopy.geocoders.Nominatim.geocode', return_value=mock.Mock(address=DEFUALT_STREET_NUMBER + ' ' + DEFAULT_STREET, point=geopy.Point(DEFAULT_LAT, DEFAULT_LON), raw=NOMINATIM_JSON_MISSING_POSTCODE_0)):
            point, postcode = run_geocoder_request(self.street_number, self.street, self.city, self.country_code, DEFAULT_POSTCODE)
        self.assertEqual(point, pnt)
        self.assertEqual(postcode, DEFAULT_POSTCODE)

    # Case 5.
    def test_run_geocoder_request_input_postal_raise_geopy_exception(self):
        with mock.patch('django_futils.utils.geopy.geocoders.Nominatim.geocode', return_value=mock.Mock(address=DEFUALT_STREET_NUMBER + ' ' + DEFAULT_STREET, point=geopy.Point(DEFAULT_LAT, DEFAULT_LON), raw=NOMINATIM_JSON_MISSING_POSTCODE_0), side_effect=geopy.exc.GeopyError('')):
            point, postcode = run_geocoder_request(self.street_number, self.street, self.city, self.country_code)
        self.assertEqual(point, None)
        self.assertEqual(postcode, str())

    # Case 6.
    def test_run_geocoder_no_match(self):
        with mock.patch('django_futils.utils.geopy.geocoders.Nominatim.geocode', return_value=None):
            point, postcode = run_geocoder_request(self.street_number, self.street, self.city, self.country_code)
        self.assertEqual(point, None)
        self.assertEqual(postcode, str())
