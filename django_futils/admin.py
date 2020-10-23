from django.contrib import admin
from django.db import models
from django.contrib.admin import site
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.admin import UserAdmin
from .models import AddressType, EmailType, TelephoneType, AttachmentType, CompanyAddress, CompanyEmail, CompanyTelephone, PersonAddress, PersonEmail, PersonTelephone, Company, PersonAttachment, Person, Municipality, NominatimCache
from .abstract_admin import AbstractAddressTypeAdmin, AbstractEmailTypeAdmin, AbstractTelephoneTypeAdmin, AbstractAttachmentTypeAdmin, AbstractMunicipalityAdmin, AbstractCompanyAddressAdmin, AbstractCompanyTelephoneAdmin, AbstractCompanyEmailAdmin, AbstractCompanyAdmin, AbstractCompanyEmailAdminInline, AbstractCompanyTelephoneAdminInline, AbstractCompanyAddressAdminInline, AbstractPersonEmailAdminInline, AbstractPersonTelephoneAdminInline, AbstractPersonAddressAdminInline, AbstractPersonAttachmentAdminInline, AbstractPersonAdmin, AbstractPersonAddressAdmin, AbstractPersonTelephoneAdmin, AbstractPersonEmailAdmin, AbstractPersonAttachmentAdmin, AbstractNominatimCacheAdmin, AbstractCompanyAdminInline


admin.site.register(AddressType, AbstractAddressTypeAdmin)
admin.site.register(EmailType, AbstractEmailTypeAdmin)
admin.site.register(TelephoneType, AbstractTelephoneTypeAdmin)
admin.site.register(AttachmentType, AbstractAttachmentTypeAdmin)
admin.site.register(Municipality, AbstractMunicipalityAdmin)
admin.site.register(CompanyAddress, AbstractCompanyAddressAdmin)
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
