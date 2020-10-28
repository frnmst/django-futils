#
# tests.py
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

from django.test import TestCase, TransactionTestCase
from .models import PersonTelephone, NominatimCache
from model_bakery import baker
import decimal
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from unittest import mock
from django.utils import timezone
from .utils import get_address_data, run_nominatim_request
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry


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
NOMINATIM_JSON_OK = {
    "features": [
        {
            "geometry": {
                "coordinates": [
                    DEFAULT_LON,
                    DEFAULT_LAT
                ],
                "type": "Point"
            },
            "properties": {
                "address": {
                    "city": DEFAULT_CITY,
                    "postcode": DEFAULT_POSTCODE,
                    "road": DEFAULT_STREET,
                },
            },
        },
    ],
}
NOMINATIM_JSON_MISSING_POSTCODE = {
    "features": [
        {
            "geometry": {
                "coordinates": [
                    DEFAULT_LON,
                    DEFAULT_LAT
                ],
                "type": "Point"
            },
            "properties": {
                "address": {
                    "city": DEFAULT_CITY,
                    "road": DEFAULT_STREET,
                },
            },
        },
    ],
}
NOMINATIM_URL = 'https://a/b'
NOMINATIM_CACHE_TTL_SECONDS_HIT = float('inf')
NOMINATIM_CACHE_TTL_SECONDS_MISS = 0


# Mocks.
def mock_date():
    return timezone.make_aware(timezone.datetime(year=1970, month=2, day=1))


def mock_run_nominatim_request_empty(**kwargs) -> tuple:
    return None, str()


def mock_requests_get_nominatim_ok(url):
    # See
    # https://stackoverflow.com/a/52971142
    return mock.Mock(status_code=200, json=lambda: NOMINATIM_JSON_OK)


def mock_requests_get_nominatim_missing_postcode(url):
    # See
    # https://stackoverflow.com/a/52971142
    return mock.Mock(status_code=200, json=lambda: NOMINATIM_JSON_MISSING_POSTCODE)


# Change the date function in the Django builtin modules (in this test module)
# and in the utils module.
@mock.patch('django.utils.timezone.now', mock_date)
class UtilsTestCase(TestCase):
    def setUp(self):
        self.city = DEFAULT_CITY
        self.street_number = DEFUALT_STREET_NUMBER
        self.street = DEFAULT_STREET

    def test_get_address_data_None(self):
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
        country = 'a'
        postal_code = None
        auto_fill = False
        point, postcode = get_address_data(country, self.city, self.street_number, self.street, postal_code, auto_fill)
        self.assertEqual(point, None)
        self.assertEqual(postcode, str())

    @mock.patch('django_futils.utils.run_nominatim_request', mock_run_nominatim_request_empty)
    @mock.patch('django.conf.settings.NOMINATIM_URL', NOMINATIM_URL)
    def test_get_address_data_autofill_new(self):
        # Cache miss because it is new.
        country = 'c'
        postal_code = None
        auto_fill = True
        point, postcode = get_address_data(country, self.city, self.street_number, self.street, postal_code, auto_fill)

        c = NominatimCache.objects.first()
        self.assertEqual(c.request_url, settings.NOMINATIM_URL + '/search?format=geojson&limit=1&addressdetails=1&city=' + self.city + '&street=' + self.street_number + '%2C%20' + self.street + '&country=' + country)
        self.assertEqual(c.cache_hits, 0)
        self.assertEqual(c.postal_code, str())
        self.assertEqual(c.map, None)
        self.assertEqual(point, None)
        self.assertEqual(postcode, str())

    @mock.patch('django_futils.utils.run_nominatim_request', mock_run_nominatim_request_empty)
    @mock.patch('django.conf.settings.NOMINATIM_URL', NOMINATIM_URL)
    @mock.patch('django.conf.settings.NOMINATIM_CACHE_TTL_SECONDS', NOMINATIM_CACHE_TTL_SECONDS_HIT)
    def test_get_address_data_autofill_cache_hit(self):
        country = 'c'
        postal_code = None
        auto_fill = True
        point, postcode = get_address_data(country, self.city, self.street_number, self.street, postal_code, auto_fill)
        c = NominatimCache.objects.first()
        # Get the pervious value.
        updated = c.updated
        country = 'c'
        postal_code = None
        auto_fill = True
        point, postcode = get_address_data(country, self.city, self.street_number, self.street, postal_code, auto_fill)

        c = NominatimCache.objects.first()
        self.assertEqual(c.request_url, settings.NOMINATIM_URL + '/search?format=geojson&limit=1&addressdetails=1&city=' + self.city + '&street=' + self.street_number + '%2C%20' + self.street + '&country=' + country)
        self.assertEqual(c.cache_hits, 1)
        self.assertEqual(c.postal_code, str())
        self.assertEqual(c.map, None)
        self.assertEqual(point, None)
        self.assertEqual(postcode, str())
        self.assertEqual(c.updated, updated)

    @mock.patch('django_futils.utils.run_nominatim_request', mock_run_nominatim_request_empty)
    @mock.patch('django.conf.settings.NOMINATIM_URL', NOMINATIM_URL)
    @mock.patch('django.conf.settings.NOMINATIM_CACHE_TTL_SECONDS', NOMINATIM_CACHE_TTL_SECONDS_MISS)
    def test_get_address_data_autofill_cache_miss(self):
        r"""Simulate a cache expiry."""
        country = 'c'
        postal_code = None
        auto_fill = True
        point, postcode = get_address_data(country, self.city, self.street_number, self.street, postal_code, auto_fill)

        c = NominatimCache.objects.first()
        # Get the pervious value.
        country = 'c'
        postal_code = None
        auto_fill = True
        point, postcode = get_address_data(country, self.city, self.street_number, self.street, postal_code, auto_fill)

        c = NominatimCache.objects.first()
        self.assertEqual(c.request_url, settings.NOMINATIM_URL + '/search?format=geojson&limit=1&addressdetails=1&city=' + self.city + '&street=' + self.street_number + '%2C%20' + self.street + '&country=' + country)
        self.assertEqual(c.cache_hits, 0)
        self.assertEqual(c.postal_code, str())
        self.assertEqual(c.map, None)
        self.assertEqual(point, None)
        self.assertEqual(postcode, str())

    @mock.patch('django_futils.utils.requests.get', mock_requests_get_nominatim_ok)
    def test_run_nominatim_request_ok(self):
        point, postcode = run_nominatim_request(str(), str())
        pnt = str({
            "coordinates": [
                DEFAULT_LON,
                DEFAULT_LAT
            ],
            "type": "Point",
        })
        self.assertEqual(point, GEOSGeometry(pnt, srid=4326))
        self.assertEqual(postcode, DEFAULT_POSTCODE)

    @mock.patch('django_futils.utils.requests.get', mock_requests_get_nominatim_missing_postcode)
    def test_run_nominatim_request_missing_postcode(self):
        point, postcode = run_nominatim_request(str(), str())
        pnt = str({
            "coordinates": [
                DEFAULT_LON,
                DEFAULT_LAT
            ],
            "type": "Point",
        })
        self.assertEqual(point, GEOSGeometry(pnt, srid=4326))
        self.assertEqual(postcode, str())
