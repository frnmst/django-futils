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
from django.http import HttpResponseRedirect
from django.urls import reverse
from .default_models import AddressType, EmailType, TelephoneType, AttachmentType, CompanyAddress, CompanyEmail, CompanyTelephone, PersonAddress, PersonEmail, PersonTelephone, Company, PersonAttachment, Person, Municipality, GeocoderCache
from .abstract_admin import AbstractAddressTypeAdmin, AbstractEmailTypeAdmin, AbstractTelephoneTypeAdmin, AbstractAttachmentTypeAdmin, AbstractMunicipalityAdmin, AbstractCompanyAddressAdmin, AbstractCompanyTelephoneAdmin, AbstractCompanyEmailAdmin, AbstractCompanyAdmin, AbstractCompanyEmailAdminInline, AbstractCompanyTelephoneAdminInline, AbstractCompanyAddressAdminInline, AbstractPersonEmailAdminInline, AbstractPersonTelephoneAdminInline, AbstractPersonAddressAdminInline, AbstractPersonAttachmentAdminInline, AbstractPersonAdmin, AbstractPersonAddressAdmin, AbstractPersonTelephoneAdmin, AbstractPersonEmailAdmin, AbstractPersonAttachmentAdmin, AbstractGeocoderCacheAdmin, AbstractCompanyAdminInline
from django.conf import settings
from . import constants as const


def abstract_response_change(self, request, obj, reverse_url):
    res = super(type(self), self).response_change(request, obj)
    if "_printable" in request.POST:
        self.hide_message = True
        return HttpResponseRedirect(
            request.build_absolute_uri(reverse(reverse_url,
                                               args=(obj.pk, ))))
    else:
        return res


# Specific stuff for this example.
# See
# https://stackoverflow.com/a/51503032
# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#customizing-the-adminsite-class
class MyAdminSite(admin.AdminSite):
    pass


admin_site = MyAdminSite(name='admin')


###########
# Inlines #
###########
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


##########
# Normal #
##########
class CompanyAdmin(AbstractCompanyAdmin):
    inlines = [
        CompanyAddressAdminInline,
        CompanyTelephoneAdminInline,
        CompanyEmailAdminInline,
    ]

    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['CompanyDetailView'])


class PersonAdmin(AbstractPersonAdmin):
    inlines = [
        PersonAddressAdminInline,
        PersonTelephoneAdminInline,
        PersonEmailAdminInline,
        PersonAttachmentAdminInline,
        CompanyAdminInline,
    ]

    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['PersonDetailView'])


class AddressTypeAdmin(AbstractAddressTypeAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['AddressTypeDetailView'])


class EmailTypeAdmin(AbstractEmailTypeAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['EmailTypeDetailView'])


class TelephoneTypeAdmin(AbstractTelephoneTypeAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['TelephoneTypeDetailView'])


class AttachmentTypeAdmin(AbstractAttachmentTypeAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['AttachmentTypeDetailView'])


class MunicipalityAdmin(AbstractMunicipalityAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['MunicipalityDetailView'])


class PersonAddressAdmin(AbstractPersonAddressAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['PersonAddressDetailView'])


class PersonTelephoneAdmin(AbstractPersonTelephoneAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['PersonTelephoneDetailView'])


class PersonAttachmentAdmin(AbstractPersonAttachmentAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['PersonAttachmentDetailView'])


class PersonEmailAdmin(AbstractPersonEmailAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['PersonEmailDetailView'])


class CompanyAddressAdmin(AbstractCompanyAddressAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['CompanyAddressDetailView'])


class CompanyTelephoneAdmin(AbstractCompanyTelephoneAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['CompanyTelephoneDetailView'])


class CompanyEmailAdmin(AbstractCompanyEmailAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['CompanyEmailDetailView'])


class GeocoderCacheAdmin(AbstractGeocoderCacheAdmin):
    def response_change(self, request, obj):
        return abstract_response_change(self, request, obj, settings.reverse_urls['GeocoderCacheDetailView'])


admin_site.register(AddressType, AddressTypeAdmin)
admin_site.register(EmailType, EmailTypeAdmin)
admin_site.register(TelephoneType, TelephoneTypeAdmin)
admin_site.register(AttachmentType, AttachmentTypeAdmin)
admin_site.register(Municipality, MunicipalityAdmin)
admin_site.register(PersonAddress, PersonAddressAdmin)
admin_site.register(PersonTelephone, PersonTelephoneAdmin)
admin_site.register(PersonAttachment, PersonAttachmentAdmin)
admin_site.register(PersonEmail, PersonEmailAdmin)
admin_site.register(CompanyAddress, CompanyAddressAdmin)
admin_site.register(CompanyTelephone, CompanyTelephoneAdmin)
admin_site.register(CompanyEmail, CompanyEmailAdmin)
admin_site.register(Company, CompanyAdmin)
admin_site.register(Person, PersonAdmin)
admin_site.register(GeocoderCache, GeocoderCacheAdmin)
