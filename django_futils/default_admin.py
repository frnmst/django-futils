#
# default_admin.py
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

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group

from . import abstract_admin as DFU_abstract_admin
from . import constants as const
from . import default_models as DFU_default_models
from .utils import abstract_response_change


# Specific stuff for this example.
# See
# https://stackoverflow.com/a/51503032
# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#customizing-the-adminsite-class
class MyAdminSite(admin.AdminSite):
    pass


# Avoid:
#     ImportError: Module "django_futils.default_admin"
#     does not define a "MyAdminSite" attribute/class.
from django.contrib.auth.admin import UserAdmin

admin_site = MyAdminSite(name='admin')
admin_site.register(DFU_default_models.ProxyUser, UserAdmin)
admin_site.register(Group)


###########
# Inlines #
###########
class CompanyAdminInline(DFU_abstract_admin.AbstractCompanyAdminInline):
    model = DFU_default_models.Company


class CompanyAddressAdminInline(DFU_abstract_admin.AbstractCompanyAddressAdminInline):
    model = DFU_default_models.CompanyAddress


class CompanyEmailAdminInline(DFU_abstract_admin.AbstractCompanyEmailAdminInline):
    model = DFU_default_models.CompanyEmail


class CompanyTelephoneAdminInline(DFU_abstract_admin.AbstractCompanyTelephoneAdminInline):
    model = DFU_default_models.CompanyTelephone


class PersonAddressAdminInline(DFU_abstract_admin.AbstractPersonAddressAdminInline):
    model = DFU_default_models.PersonAddress


class PersonEmailAdminInline(DFU_abstract_admin.AbstractPersonEmailAdminInline):
    model = DFU_default_models.PersonEmail


class PersonTelephoneAdminInline(DFU_abstract_admin.AbstractPersonTelephoneAdminInline):
    model = DFU_default_models.PersonTelephone


class PersonAttachmentAdminInline(DFU_abstract_admin.AbstractPersonAttachmentAdminInline):
    model = DFU_default_models.PersonAttachment


##########
# Normal #
##########
class CompanyAdmin(DFU_abstract_admin.AbstractCompanyAdmin):
    inlines = [
        CompanyAddressAdminInline,
        CompanyTelephoneAdminInline,
        CompanyEmailAdminInline,
    ]

    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['CompanyDetailView'])


class PersonAdmin(DFU_abstract_admin.AbstractPersonAdmin):
    inlines = [
        PersonAddressAdminInline,
        PersonTelephoneAdminInline,
        PersonEmailAdminInline,
        PersonAttachmentAdminInline,
        CompanyAdminInline,
    ]

    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['PersonDetailView'])


class AddressTypeAdmin(DFU_abstract_admin.AbstractAddressTypeAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['AddressTypeDetailView'])


class EmailTypeAdmin(DFU_abstract_admin.AbstractEmailTypeAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['EmailTypeDetailView'])


class TelephoneTypeAdmin(DFU_abstract_admin.AbstractTelephoneTypeAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['TelephoneTypeDetailView'])


class AttachmentTypeAdmin(DFU_abstract_admin.AbstractAttachmentTypeAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['AttachmentTypeDetailView'])


class MunicipalityAdmin(DFU_abstract_admin.AbstractMunicipalityAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['MunicipalityDetailView'])


class PersonAddressAdmin(DFU_abstract_admin.AbstractPersonAddressAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['PersonAddressDetailView'])


class PersonTelephoneAdmin(DFU_abstract_admin.AbstractPersonTelephoneAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['PersonTelephoneDetailView'])


class PersonAttachmentAdmin(DFU_abstract_admin.AbstractPersonAttachmentAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['PersonAttachmentDetailView'])


class PersonEmailAdmin(DFU_abstract_admin.AbstractPersonEmailAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['PersonEmailDetailView'])


class CompanyAddressAdmin(DFU_abstract_admin.AbstractCompanyAddressAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['CompanyAddressDetailView'])


class CompanyTelephoneAdmin(DFU_abstract_admin.AbstractCompanyTelephoneAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['CompanyTelephoneDetailView'])


class CompanyEmailAdmin(DFU_abstract_admin.AbstractCompanyEmailAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['CompanyEmailDetailView'])


class GeocoderCacheAdmin(DFU_abstract_admin.AbstractGeocoderCacheAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['GeocoderCacheDetailView'])


# Register like this and not with the decorator because we are
# not using the default admin: we are admin_site instead
admin_site.register(DFU_default_models.AddressType, AddressTypeAdmin)
admin_site.register(DFU_default_models.EmailType, EmailTypeAdmin)
admin_site.register(DFU_default_models.TelephoneType, TelephoneTypeAdmin)
admin_site.register(DFU_default_models.AttachmentType, AttachmentTypeAdmin)
admin_site.register(DFU_default_models.Municipality, MunicipalityAdmin)
admin_site.register(DFU_default_models.PersonAddress, PersonAddressAdmin)
admin_site.register(DFU_default_models.PersonTelephone, PersonTelephoneAdmin)
admin_site.register(DFU_default_models.PersonAttachment, PersonAttachmentAdmin)
admin_site.register(DFU_default_models.PersonEmail, PersonEmailAdmin)
admin_site.register(DFU_default_models.CompanyAddress, CompanyAddressAdmin)
admin_site.register(DFU_default_models.CompanyTelephone, CompanyTelephoneAdmin)
admin_site.register(DFU_default_models.CompanyEmail, CompanyEmailAdmin)
admin_site.register(DFU_default_models.Company, CompanyAdmin)
admin_site.register(DFU_default_models.Person, PersonAdmin)
admin_site.register(DFU_default_models.GeocoderCache, GeocoderCacheAdmin)
