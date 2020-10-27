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
from .models import PersonTelephone
from model_bakery import baker
import decimal
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from unittest import mock
from django.utils import timezone
from vies.types import VATIN


##########
# Models #
##########
class PersonTelephoneTestCase(TestCase):
    def setUp(self):
        self.person = baker.make('Person')
        self.telephonetype = baker.make('TelephoneType')
        self.persontelephone_1 = baker.make('PersonTelephone',
                                   number='112233',
                                   is_primary=False,
                                   type=self.telephonetype,
                                   person=self.person)

    def test_constraints_duplicate_elements(self):
        # Same type, number and person.
        with self.assertRaises(IntegrityError):
            self.persontelephone_2 = baker.make('PersonTelephone',
                                       number='112233',
                                       type=self.telephonetype,
                                       person=self.person)

    def test_constraints_duplicate_is_primary(self):
        r"""This constraint should nevery be hit because of the save method
           which corrects the error.
        """

    def test_save_new(self):
        # Re-read the data from the database. If we read from
        # the local variables we cannot track the changes.
        t1 = PersonTelephone.objects.first()
        self.assertEqual(t1.is_primary, True)

    def test_save_new_primary(self):
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
        self.person_2 = baker.make('Person')
        self.persontelephone_1.person = self.person_2
        with self.assertRaises(ValidationError):
            self.persontelephone_1.full_clean()


class CompanyTelephoneTestCase(TestCase):
    r"""This works the same as the PersonTelephone."""


class PersonEmailTestCase(TestCase):
    r"""This works the same as the PersonTelephone."""


class CompanyEmailTestCase(TestCase):
    r"""This works the same as the PersonTelephone."""


class PersonAddressTestCase(TestCase):
    r"""This works the same as the PersonTelephone."""


class CompanyAddressTestCase(TestCase):
    r"""This works the same as the PersonTelephone."""


#########
# Utils #
#########
def mock_date():
    return timezone.make_aware(timezone.datetime(year=1970, month=2, day=1))


# Changed the date function in the Django builtin modules and in the utils module.
@mock.patch('django_futils.utils.localdate', mock_date)
@mock.patch('django.utils.timezone.now', mock_date)
class UtilsTestCase(TestCase):
    pass
