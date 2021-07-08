#
# default_models.py
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

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from . import abstract_models as DFU_abstract_models


class User(AbstractUser):
    r"""Custom user class."""


class ProxyUser(User):
    r"""This is a virtual class used in the admin instead of User.

        See
        https://stackoverflow.com/a/61691173
    """
    class Meta:
        app_label = 'auth'
        proxy = True
        verbose_name = _('user')
        verbose_name_plural = _('users')


################
# Type classes #
################
class AddressType(DFU_abstract_models.AbstractAddressType):
    pass


class EmailType(DFU_abstract_models.AbstractEmailType):
    pass


class TelephoneType(DFU_abstract_models.AbstractTelephoneType):
    pass


class AttachmentType(DFU_abstract_models.AbstractAttachmentType):
    pass


###################
# Element classes #
###################
class Municipality(DFU_abstract_models.AbstractMunicipality):
    pass


class PersonTelephone(DFU_abstract_models.AbstractPersonTelephone):
    type = models.ForeignKey(
        'TelephoneType',
        related_name='persontelephone_of_this_telephonetype',
        on_delete=models.PROTECT,
        verbose_name=_('type'),
    )
    person = models.ForeignKey(
        'Person',
        related_name='persontelephone_of_this_person',
        on_delete=models.CASCADE,
        verbose_name=_('person'),
    )

    class Meta(DFU_abstract_models.AbstractPersonTelephone.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['number', 'type', 'person'],
                name='dfu_persontelephone_constraint'),
        ]


class CompanyTelephone(DFU_abstract_models.AbstractCompanyTelephone):
    type = models.ForeignKey(
        'TelephoneType',
        related_name='companytelephone_of_this_telephonetype',
        on_delete=models.PROTECT,
        verbose_name=_('type'),
    )
    company = models.ForeignKey(
        'Company',
        related_name='companytelephone_of_this_company',
        on_delete=models.CASCADE,
        verbose_name=_('company'),
    )

    class Meta(DFU_abstract_models.AbstractCompanyTelephone.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['number', 'type', 'company'],
                name='dfu_companytelephone_constraint'),
        ]


class PersonEmail(DFU_abstract_models.AbstractPersonEmail):
    type = models.ForeignKey(
        'EmailType',
        related_name='personemail_of_this_emailtype',
        on_delete=models.PROTECT,
        verbose_name=_('type'),
    )
    person = models.ForeignKey(
        'Person',
        related_name='personemail_of_this_person',
        on_delete=models.CASCADE,
        verbose_name=_('person'),
    )

    class Meta(DFU_abstract_models.AbstractPersonEmail.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'type', 'person'],
                name='dfu_personemail_constraint'),
        ]


class CompanyEmail(DFU_abstract_models.AbstractCompanyEmail):
    type = models.ForeignKey(
        'EmailType',
        related_name='companyemail_of_this_emailtype',
        on_delete=models.PROTECT,
        verbose_name=_('type'),
    )
    company = models.ForeignKey(
        'Company',
        related_name='companyemail_of_this_company',
        on_delete=models.CASCADE,
        verbose_name=_('company'),
    )

    class Meta(DFU_abstract_models.AbstractCompanyEmail.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'type', 'company'],
                name='dfu_companyemail_constraint'),
        ]


class PersonAddress(DFU_abstract_models.AbstractPersonAddress):
    type = models.ForeignKey(
        'AddressType',
        related_name='personaddress_of_this_addresstype',
        on_delete=models.PROTECT,
        verbose_name=_('type'),
    )
    municipality = models.ForeignKey(
        'Municipality',
        related_name='personaddress_address_of_this_municipality',
        on_delete=models.PROTECT,
        verbose_name=_('municipality'),
    )
    person = models.ForeignKey(
        'Person',
        related_name='personaddress_of_this_person',
        on_delete=models.CASCADE,
        verbose_name=_('person'),
    )

    class Meta(DFU_abstract_models.AbstractPersonAddress.Meta):
        constraints = [
            # See
            # https://stackoverflow.com/questions/55044802/django-admin-inline-unique-constraint-violation-on-edit
            # https://stackoverflow.com/questions/40891574/how-can-i-set-a-table-constraint-deferrable-initially-deferred-in-django-model
            # https://docs.djangoproject.com/en/3.1/ref/models/constraints/#deferrable
            models.UniqueConstraint(
                fields=['street_number', 'street', 'city', 'municipality', 'type', 'person'],
                name='dfu_personaddress_constraint'),
        ]


class CompanyAddress(DFU_abstract_models.AbstractCompanyAddress):
    type = models.ForeignKey(
        'AddressType',
        related_name='companyaddress_of_this_addresstype',
        on_delete=models.PROTECT,
        verbose_name=_('type'),
    )
    municipality = models.ForeignKey(
        'Municipality',
        related_name='companyaddress_of_this_municipality',
        on_delete=models.PROTECT,
        verbose_name=_('municipality'),
    )
    company = models.ForeignKey(
        'Company',
        related_name='companyaddress_of_this_company',
        on_delete=models.CASCADE,
        verbose_name=_('company'),
    )

    class Meta(DFU_abstract_models.AbstractCompanyAddress.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['street_number', 'street', 'city', 'municipality', 'type', 'company'],
                name='dfu_companyaddress_constraint'),
        ]


class PersonAttachment(DFU_abstract_models.AbstractPersonAttachment):
    type = models.ForeignKey(
        'AttachmentType',
        related_name='personattachment_of_this_attachmenttype',
        on_delete=models.PROTECT,
        verbose_name=_('attachment type'),
    )
    person = models.ForeignKey(
        'Person',
        related_name='personattachment_of_this_person',
        on_delete=models.CASCADE,
        verbose_name=_('person'),
    )


class Person(DFU_abstract_models.AbstractPerson):
    pass


class Company(DFU_abstract_models.AbstractCompany):
    person = models.ForeignKey(
        'Person',
        related_name='company_of_this_person',
        on_delete=models.CASCADE,
        verbose_name=_('person'),
    )

    class Meta(DFU_abstract_models.AbstractCompany.Meta):
        constraints = [
            models.UniqueConstraint(fields=['person'],
                                    condition=Q(is_primary=True),
                                    name='dfu_is_primary_company_costraint')
        ]


class GeocoderCache(DFU_abstract_models.AbstractGeocoderCache):
    pass
