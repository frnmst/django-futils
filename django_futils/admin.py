#
# admin.py
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

from django.contrib import admin
from .models import AddressType, EmailType, TelephoneType, AttachmentType, CompanyAddress, CompanyEmail, CompanyTelephone, PersonAddress, PersonEmail, PersonTelephone, Company, PersonAttachment, Person, Municipality, NominatimCache
from .abstract_admin import AbstractAddressTypeAdmin, AbstractEmailTypeAdmin, AbstractTelephoneTypeAdmin, AbstractAttachmentTypeAdmin, AbstractMunicipalityAdmin, AbstractCompanyAddressAdmin, AbstractCompanyTelephoneAdmin, AbstractCompanyEmailAdmin, AbstractCompanyAdmin, AbstractCompanyEmailAdminInline, AbstractCompanyTelephoneAdminInline, AbstractCompanyAddressAdminInline, AbstractPersonEmailAdminInline, AbstractPersonTelephoneAdminInline, AbstractPersonAddressAdminInline, AbstractPersonAttachmentAdminInline, AbstractPersonAdmin, AbstractPersonAddressAdmin, AbstractPersonTelephoneAdmin, AbstractPersonEmailAdmin, AbstractPersonAttachmentAdmin, AbstractNominatimCacheAdmin, AbstractCompanyAdminInline
from .forms import CompanyAddressForm
from django.conf import settings
from . import constants as const

admin.site.register(AddressType, AbstractAddressTypeAdmin)
admin.site.register(EmailType, AbstractEmailTypeAdmin)
admin.site.register(TelephoneType, AbstractTelephoneTypeAdmin)
admin.site.register(AttachmentType, AbstractAttachmentTypeAdmin)
admin.site.register(Municipality, AbstractMunicipalityAdmin)


@admin.register(CompanyAddress)
class CompanyAddressAdmin(AbstractCompanyAddressAdmin):
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        form = CompanyAddressForm


admin.site.register(CompanyTelephone, AbstractCompanyTelephoneAdmin)
admin.site.register(CompanyEmail, AbstractCompanyEmailAdmin)
admin.site.register(PersonAddress, AbstractPersonAddressAdmin)
admin.site.register(PersonTelephone, AbstractPersonTelephoneAdmin)
admin.site.register(PersonEmail, AbstractPersonEmailAdmin)
admin.site.register(PersonAttachment, AbstractPersonAttachmentAdmin)
admin.site.register(NominatimCache, AbstractNominatimCacheAdmin)


class CompanyAdminInline(AbstractCompanyAdminInline):
    model = Company


class CompanyAddressAdminInline(AbstractCompanyAddressAdminInline):
    model = CompanyAddress
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        form = CompanyAddressForm


class CompanyEmailAdminInline(AbstractCompanyEmailAdminInline):
    model = CompanyEmail


class CompanyTelephoneAdminInline(AbstractCompanyTelephoneAdminInline):
    model = CompanyTelephone


class PersonAddressAdminInline(AbstractPersonAddressAdminInline):
    model = PersonAddress


class PersonEmailAdminInline(AbstractPersonEmailAdminInline):
    model = PersonEmail


class PersonTelephoneAdminInline(AbstractPersonTelephoneAdminInline):
    model = PersonTelephone


class PersonAttachmentAdminInline(AbstractPersonAttachmentAdminInline):
    model = PersonAttachment


@admin.register(Company)
class CompanyAdmin(AbstractCompanyAdmin):
    inlines = [
        CompanyAddressAdminInline,
        CompanyTelephoneAdminInline,
        CompanyEmailAdminInline,
    ]


@admin.register(Person)
class PersonAdmin(AbstractPersonAdmin):
    inlines = [
        PersonAddressAdminInline,
        PersonTelephoneAdminInline,
        PersonEmailAdminInline,
        PersonAttachmentAdminInline,
        CompanyAdminInline,
    ]
