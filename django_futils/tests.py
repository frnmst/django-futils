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
def mock_date():
    return timezone.make_aware(timezone.datetime(year=1970, month=2, day=1))


def mock_run_nominatim_request_empty(**kwargs):
    return None, str()


# Change the date function in the Django builtin modules (in this test module)
# and in the utils module.
@mock.patch('django_futils.utils.localdate', mock_date)
@mock.patch('django.utils.timezone.now', mock_date)
class UtilsTestCase(TestCase):
    def setUp(self):
        self.city = 'c'
        self.street_number = '1'
        self.street = 's'

    def test_get_address_data_None(self):
        # Existing postal code.
        country = None
        postal_code = 'a'
        auto_fill = True
        point, postcode = get_address_data(country, self.city, self.street_number, self.street, postal_code, auto_fill)
        self.assertEqual(point, None)
        self.assertEqual(postcode, 'a')

        # Empty string postal code.
        country = None
        postal_code = str()
        auto_fill = True
        point, postcode = get_address_data(country, self.city, self.street_number, self.street, postal_code, auto_fill)
        self.assertEqual(point, None)
        self.assertEqual(postcode, str())

        # Empty postal code.
        country = None
        postal_code = None
        auto_fill = True
        point, postcode = get_address_data(country, self.city, self.street_number, self.street, postal_code, auto_fill)
        self.assertEqual(point, None)
        self.assertEqual(postcode, str())

    def test_get_address_data_no_autofill(self):
        country = 'a'
        postal_code = None
        auto_fill = False
        point, postcode = get_address_data(country, self.city, self.street_number, self.street, postal_code, auto_fill)
        self.assertEqual(point, None)
        self.assertEqual(postcode, str())

    @mock.patch('django_futils.utils.run_nominatim_request', mock_run_nominatim_request_empty)
    def test_get_address_data_autofill(self):
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
