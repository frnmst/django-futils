#
# abstract_models.py
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

from django.db import models
from django.contrib.gis.db import models as gis_models
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings
from phone_field import PhoneField
from vies.models import VATINField
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _
from hashid_field import Hashid
from .utils import personattachment_directory_path, get_address_data, save_primary
import django_futils.constants as const


class AbstractRecordTimestamps(models.Model):
    added = models.DateTimeField(_('added'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    history = HistoricalRecords(inherit=True)

    @property
    def serial_id(self):
        return Hashid(self.id, min_length=16, salt=settings.HASHID_FIELD_SALT)

    class Meta:
        abstract = True


class AbstractBasicElement(models.Model):
    code = models.CharField(_('code'),
                            max_length=const.CODE_LENGTH,
                            unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    history = HistoricalRecords(inherit=True)

    @property
    def serial_id(self):
        return Hashid(self.id, min_length=16, salt=settings.HASHID_FIELD_SALT)

    class Meta:
        abstract = True


########################
# AbstractType classes #
########################
class AbstractType(AbstractBasicElement):
    type = models.CharField(_('type'),
                            max_length=const.NAME_LENGTH,
                            db_index=True)

    def __str__(self):
        return self.type

    class Meta:
        abstract = True


class AbstractAddressType(AbstractType):
    class Meta:
        abstract = True
        verbose_name = _('address type')
        verbose_name_plural = _('address types')


class AbstractEmailType(AbstractType):
    class Meta:
        abstract = True
        verbose_name = _('email type')
        verbose_name_plural = _('email types')


class AbstractTelephoneType(AbstractType):
    class Meta:
        abstract = True
        verbose_name = _('telephone type')
        verbose_name_plural = _('telephone types')


class AbstractAttachmentType(AbstractType):
    class Meta:
        abstract = True
        verbose_name = _('attachment type')
        verbose_name_plural = _('attachment types')


###########################
# AbstractElement classes #
###########################
class AbstractElement(AbstractBasicElement):
    name = models.CharField(_('name'),
                            max_length=const.NAME_LENGTH,
                            db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class AbstractMunicipality(AbstractElement):
    r"""This is the equivalent of:
        'comune'    in 'IT'
    """
    country = CountryField(_('country'), default='IT')

    class Meta:
        abstract = True
        verbose_name = _('municipality')
        verbose_name_plural = _('municipalities')


##################
# Normal classes #
##################
class AbstractCommonAttachment(AbstractRecordTimestamps):
    name = models.CharField(_('name'), max_length=const.NAME_LENGTH)
    notes = models.TextField(_('notes'), blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AbstractHasPrimary(AbstractRecordTimestamps):
    is_primary = models.BooleanField(_('is primary'), default=False)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        if self.is_primary:
            raise ValidationError(_('cannot delete primary object'))
        else:
            super().delete(*args, **kwargs)


class AbstractTelephoneCommon(AbstractHasPrimary):
    number = PhoneField(_('number'), unique=True, db_index=True)
    has_whatsapp = models.BooleanField(_('has whatsapp'), default=False)
    has_telegram = models.BooleanField(_('has telegram'), default=False)
    is_primary = models.BooleanField(_('primary'), default=False)

    def __str__(self):
        return str(self.number)

    class Meta:
        abstract = True


class AbstractPersonTelephone(AbstractTelephoneCommon):
    class Meta:
        abstract = True
        verbose_name = _('person telephone')
        verbose_name_plural = _('person telephones')

    def save(self, *args, **kwargs):
        save_primary(self=self, field_name='person', field_value=self.person)
        super().save(*args, **kwargs)

    def clean(self):
        if self.pk and self.is_primary:
            if type(self).objects.get(pk=self.pk).person != self.person:
                raise ValidationError(_('cannot assign a primary telephone to a different person once it is set'))


class AbstractCompanyTelephone(AbstractTelephoneCommon):
    class Meta:
        abstract = True
        verbose_name = _('company telephone')
        verbose_name_plural = _('company telephones')

    def save(self, *args, **kwargs):
        save_primary(self=self, field_name='company', field_value=self.company)
        super().save(*args, **kwargs)

    def clean(self):
        if self.pk and self.is_primary:
            if type(self).objects.get(pk=self.pk).company != self.company:
                raise ValidationError(_('cannot assign a primary telephone to a different company once it is set'))


class AbstractEmailCommon(AbstractHasPrimary):
    email = models.EmailField(_('email'),
                              max_length=const.EMAIL_MAX_LENGTH,
                              unique=True,
                              db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.email)


class AbstractPersonEmail(AbstractEmailCommon):
    class Meta:
        abstract = True
        verbose_name = _('person email')
        verbose_name_plural = _('person emails')

    def save(self, *args, **kwargs):
        save_primary(self=self, field_name='person', field_value=self.person)
        super().save(*args, **kwargs)

    def clean(self):
        if self.pk and self.is_primary:
            if type(self).objects.get(pk=self.pk).person != self.person:
                raise ValidationError(_('cannot assign a primary email to a different person once it is set'))


class AbstractCompanyEmail(AbstractEmailCommon):
    class Meta:
        abstract = True
        verbose_name = _('company email')
        verbose_name_plural = _('company emails')

    def save(self, *args, **kwargs):
        save_primary(self=self, field_name='company', field_value=self.company)
        super().save(*args, **kwargs)

    def clean(self):
        if self.pk and self.is_primary:
            if type(self).objects.get(pk=self.pk).person != self.person:
                raise ValidationError(_('cannot assign a primary email to a different company once it is set'))


class AbstractAddressCommon(AbstractHasPrimary):
    map = gis_models.PointField(_('map'), blank=True, null=True)
    street_number = models.CharField(_('street number'),
                                     max_length=const.GENERIC_CHAR_FIELD_LENGTH,
                                     db_index=True)
    street = models.CharField(_('street'), max_length=const.GENERIC_CHAR_FIELD_LENGTH, db_index=True)
    city = models.CharField(_('city'), max_length=const.GENERIC_CHAR_FIELD_LENGTH, db_index=True)
    postal_code = models.CharField(_('postal code'),
                                   max_length=const.GENERIC_CHAR_FIELD_LENGTH,
                                   blank=True)
    auto_fill = models.BooleanField(_('auto fill'), default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.map, self.postal_code = get_address_data(
            self.municipality.country.code, self.city, self.street_number,
            self.street, self.postal_code, self.map, self.auto_fill)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.street + ', ' + self.street_number + ', ' + self.city


class AbstractPersonAddress(AbstractAddressCommon):
    class Meta:
        abstract = True
        verbose_name = _('person address')
        verbose_name_plural = _('person addresses')

    def save(self, *args, **kwargs):
        save_primary(self=self, field_name='person', field_value=self.person)
        super().save(*args, **kwargs)

    def clean(self):
        if self.pk and self.is_primary:
            if type(self).objects.get(pk=self.pk).person != self.person:
                raise ValidationError(_('cannot assign a primary address to a different person once it is set'))


class AbstractCompanyAddress(AbstractAddressCommon):
    class Meta:
        abstract = True
        verbose_name = _('company address')
        verbose_name_plural = _('company addresses')

    def save(self, *args, **kwargs):
        save_primary(self=self, field_name='company', field_value=self.company)
        super().save(*args, **kwargs)

    def clean(self):
        if self.pk and self.is_primary:
            if type(self).objects.get(pk=self.pk).company != self.company:
                raise ValidationError(_('cannot assign a primary address to a different company once it is set'))


class AbstractCompany(AbstractRecordTimestamps):
    name = models.CharField(_('name'), max_length=const.GENERIC_CHAR_FIELD_LENGTH)
    vat = VATINField(_('VAT'), unique=True)
    is_primary = models.BooleanField(_('is primary'), default=False)

    class Meta:
        abstract = True
        verbose_name = _('company')
        verbose_name_plural = _('companies')

    def save(self, *args, **kwargs):
        save_primary(self=self, field_name='person', field_value=self.person)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AbstractPerson(AbstractRecordTimestamps):
    first_name = models.CharField(_('first name'),
                                  max_length=const.GENERIC_CHAR_FIELD_LENGTH,
                                  db_index=True)
    last_name = models.CharField(_('last name'), max_length=const.GENERIC_CHAR_FIELD_LENGTH, db_index=True)
    date_of_birth = models.DateField(_('date of birth'), default=timezone.now)
    city_of_birth = models.CharField(_('city of birth'), max_length=const.GENERIC_CHAR_FIELD_LENGTH)
    fiscal_code = models.CharField(_('fiscal code'),
                                   max_length=const.GENERIC_CHAR_FIELD_LENGTH,
                                   unique=True,
                                   db_index=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + '[' + self.fiscal_code + ']'

    class Meta:
        abstract = True
        verbose_name = _('person')
        verbose_name_plural = _('people')


class AbstractPersonAttachment(AbstractCommonAttachment):
    file = models.FileField(_('file'),
                            upload_to=personattachment_directory_path,
                            null=True)

    class Meta:
        abstract = True
        verbose_name = _('person attachment')
        verbose_name_plural = _('person attachments')


class AbstractGeocoderCache(AbstractRecordTimestamps):
    r"""As required by the terms of use, Nominatim results must be cached.
        See
        https://operations.osmfoundation.org/policies/nominatim/
    """
    street_number = models.CharField(_('street number'),
                                     max_length=const.GENERIC_CHAR_FIELD_LENGTH,
                                     db_index=True)
    street = models.CharField(_('street'), max_length=const.GENERIC_CHAR_FIELD_LENGTH, db_index=True)
    city = models.CharField(_('city'), max_length=const.GENERIC_CHAR_FIELD_LENGTH, db_index=True)
    country_code = models.CharField(_('contry code'), max_length=const.GENERIC_CHAR_FIELD_LENGTH, db_index=True)
    postal_code = models.CharField(_('postal code'),
                                   max_length=const.GENERIC_CHAR_FIELD_LENGTH,
                                   blank=True, null=True)
    map = gis_models.PointField(_('map'), blank=True, null=True)
    cache_hits = models.IntegerField(_('cache hits'), default=0)

    class Meta:
        abstract = True
        verbose_name = _('Nominatim cache')
        verbose_name_plural = _('Nominatim caches')
