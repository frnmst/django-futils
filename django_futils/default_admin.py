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
from .default_models import AddressType, EmailType, TelephoneType, AttachmentType, CompanyAddress, CompanyEmail, CompanyTelephone, PersonAddress, PersonEmail, PersonTelephone, Company, PersonAttachment, Person, Municipality, NominatimCache
from .abstract_admin import AbstractAddressTypeAdmin, AbstractEmailTypeAdmin, AbstractTelephoneTypeAdmin, AbstractAttachmentTypeAdmin, AbstractMunicipalityAdmin, AbstractCompanyAddressAdmin, AbstractCompanyTelephoneAdmin, AbstractCompanyEmailAdmin, AbstractCompanyAdmin, AbstractCompanyEmailAdminInline, AbstractCompanyTelephoneAdminInline, AbstractCompanyAddressAdminInline, AbstractPersonEmailAdminInline, AbstractPersonTelephoneAdminInline, AbstractPersonAddressAdminInline, AbstractPersonAttachmentAdminInline, AbstractPersonAdmin, AbstractPersonAddressAdmin, AbstractPersonTelephoneAdmin, AbstractPersonEmailAdmin, AbstractPersonAttachmentAdmin, AbstractNominatimCacheAdmin, AbstractCompanyAdminInline
from django.conf import settings
from . import constants as const


# Specific stuff for this example.
# See
# https://stackoverflow.com/a/51503032
# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#customizing-the-adminsite-class
class MyAdminSite(admin.AdminSite):
    pass


admin_site = MyAdminSite(name='admin')


class CompanyAdminInline(AbstractCompanyAdminInline):
    model = Company


class CompanyAddressAdminInline(AbstractCompanyAddressAdminInline):
    model = CompanyAddress


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


class CompanyAdmin(AbstractCompanyAdmin):
    inlines = [
        CompanyAddressAdminInline,
        CompanyTelephoneAdminInline,
        CompanyEmailAdminInline,
    ]


class PersonAdmin(AbstractPersonAdmin):
    inlines = [
        PersonAddressAdminInline,
        PersonTelephoneAdminInline,
        PersonEmailAdminInline,
        PersonAttachmentAdminInline,
        CompanyAdminInline,
    ]


admin_site.register(AddressType, AbstractAddressTypeAdmin)
admin_site.register(EmailType, AbstractEmailTypeAdmin)
admin_site.register(TelephoneType, AbstractTelephoneTypeAdmin)
admin_site.register(AttachmentType, AbstractAttachmentTypeAdmin)
admin_site.register(Municipality, AbstractMunicipalityAdmin)
admin_site.register(PersonAddress, AbstractPersonAddressAdmin)
admin_site.register(PersonTelephone, AbstractPersonTelephoneAdmin)
admin_site.register(PersonAttachment, AbstractPersonAttachmentAdmin)
admin_site.register(PersonEmail, AbstractPersonEmailAdmin)
admin_site.register(CompanyAddress, AbstractCompanyAddressAdmin)
admin_site.register(CompanyTelephone, AbstractCompanyTelephoneAdmin)
admin_site.register(CompanyEmail, AbstractCompanyEmailAdmin)
admin_site.register(Company, CompanyAdmin)
admin_site.register(Person, PersonAdmin)
admin_site.register(NominatimCache, AbstractNominatimCacheAdmin)
