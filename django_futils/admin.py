from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
from django.contrib.gis.admin import OSMGeoAdmin
from django.db.models import Sum, Avg
from django.db.models.functions import Coalesce
from django.contrib.admin import site
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin
from djmoney.models.fields import MoneyField

from .models import (AttachmentType, PersonAttachment,
                     PersonTelephone, CompanyTelephone, TelephoneType,
                     PersonEmail, CompanyEmail, EmailType, PersonAddress,
                     AddressType, Municipality, Person, Company,
                     CompanyAddress, NominatimCache)
from .formsets import HasPrimaryInlineFormSet
from django_futils.settings import OPENLAYERS_URL, FOREIGN_KEY_FIELDS
# from grantmeapp.widgets import MoneyHiddenCurrencyWidget
# from .forms import ServiceForm
import django_futils.constants as const

# Remove the delete action globally. See
# https://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/#disabling-a-site-wide-action
site.disable_action('delete_selected')


################
# Base classes #
################
class BaseAdmin(SimpleHistoryAdmin):
    list_per_page = 10
    readonly_fields = ('id',)


class TypeBaseAdmin(BaseAdmin):
    actions = ['delete_selected']
    readonly_fields = ('id', )
    list_display = (
        'id',
        'type',
    )


class NameBaseAdmin(BaseAdmin):
    actions = ['delete_selected']
    readonly_fields = ('id', )
    list_display = (
        'id',
        'name',
    )


class BaseAdminInline(admin.StackedInline):
    SHOW_IDS = True
    if SHOW_IDS:
        readonly_fields = ('id', )
    else:
        readonly_fields = ()

    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={
                'rows': 2,
                'cols': 20
            })
        },
    }
    extra = 0
#    classes = ['collapse']

    # Show the link with the pencil icon in the inline element that
    # opens a new change window.
    show_change_link = True


class BaseOneElementMandatoryAdminInline(BaseAdminInline):
    r"""At least one element must be present.
        See https://stackoverflow.com/a/53868121
    """
    min_num = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


class BaseMapAdmin(OSMGeoAdmin, BaseAdmin):
    default_zoom = 10
    default_lon = -90
    default_lat = 10
    modifiable = False
    openlayers_url = OPENLAYERS_URL


class AddressCommonAdmin(BaseMapAdmin):
    # See
    # https://stackoverflow.com/a/50007302
    def get_form(self, request, obj=None, **kwargs):
        help_texts = {
            'auto_fill':
            _('fill the postal code and the map data automatically')
        }
        kwargs.update({'help_texts': help_texts})
        return super().get_form(request, obj, **kwargs)


##########
# Leaves #
##########
@admin.register(CompanyAddress)
class CompanyAddressAdmin(AddressCommonAdmin):
    actions = ['delete_selected']
    readonly_fields = ('id', )
    list_display = (
        'id',
        'company',
    )
    list_select_related = ('company', )
    list_per_page = 10

    raw_id_fields = (
        'type',
        'municipality',
        'company',
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            if obj.is_primary:
                return self.readonly_fields + ('is_primary', 'company',)
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        delete = True
        if obj is not None:
            if obj.is_primary:
                delete = False
        return delete


@admin.register(AddressType)
class AddressTypeAdmin(TypeBaseAdmin):
    pass


@admin.register(EmailType)
class EmailTypeAdmin(TypeBaseAdmin):
    pass


@admin.register(TelephoneType)
class TelephoneTypeAdmin(TypeBaseAdmin):
    pass


@admin.register(AttachmentType)
class AttachmentTypeAdmin(TypeBaseAdmin):
    pass


@admin.register(Municipality)
class MunicipalityAdmin(NameBaseAdmin):
    pass


@admin.register(NominatimCache)
class NominatimCacheAdmin(OSMGeoAdmin, BaseAdmin):
    actions = ['delete_selected']
    readonly_fields = (
        'id',
        'added',
        'updated',
        'cache_hits',
    )
    list_display = (
        'id',
        'request_url',
    )


###########
# Inlines #
###########
class CompanyAddressAdminInline(BaseOneElementMandatoryAdminInline):
    model = CompanyAddress
    formset = HasPrimaryInlineFormSet
    if FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        form = CompanyAddressForm
    elif FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = (
            'company',
            'type',
            'municipality',
        )
    exclude = ('map', )


class CompanyAdminInline(BaseAdminInline):
    model = Company


class PersonAddressAdminInline(BaseOneElementMandatoryAdminInline):
    model = PersonAddress
    formset = HasPrimaryInlineFormSet
    readonly_fields = BaseAdminInline.readonly_fields + (
        'is_primary',
    )
    if FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        form = CompanyAddressForm
    elif FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = (
            'type',
            'municipality',
        )

    exclude = ('map', )

    def get_formset(self, request, obj=None, **kwargs):
        help_texts = {
            'auto_fill': _('fill the postal code and the map data automatically'),
        }
        kwargs.update({'help_texts': help_texts})
        return super().get_formset(request, obj, **kwargs)


class PersonEmailAdminInline(BaseAdminInline):
    model = PersonEmail
    formset = HasPrimaryInlineFormSet
    readonly_fields = (
        'id',
        'is_primary',
    )
    list_display = ('id', )
    raw_id_fields = ('type', )


class CompanyEmailAdminInline(BaseAdminInline):
    model = CompanyEmail
    formset = HasPrimaryInlineFormSet
    readonly_fields = (
        'id',
        'is_primary',
    )
    list_display = ('id', )
    raw_id_fields = ('type', )


class PersonTelephoneAdminInline(BaseOneElementMandatoryAdminInline):
    model = PersonTelephone
    formset = HasPrimaryInlineFormSet
    readonly_fields = (
        'id',
        'is_primary',
    )
    list_display = ('id', )
    raw_id_fields = ('type', )


class CompanyTelephoneAdminInline(BaseOneElementMandatoryAdminInline):
    model = CompanyTelephone
    formset = HasPrimaryInlineFormSet
    readonly_fields = (
        'id',
        'is_primary',
    )
    list_display = ('id', )
    raw_id_fields = ('type', )


class PersonAdminInline(BaseAdminInline):
    model = Person
    readonly_fields = (
        'id',
    )
    list_display = ('id', )


class PersonAttachmentAdminInline(BaseAdminInline):
    model = PersonAttachment
    readonly_fields = ('id', )
    raw_id_fields = ('attachment_type', )


########
# Main #
########
@admin.register(PersonAddress)
class PersonAddressAdmin(AddressCommonAdmin):
    readonly_fields = (
        'id',
        'added',
        'updated',
    )
    list_display = (
        'id',
        'street_number',
        'street',
        'city',
        'person',
        'type',
        'is_primary',
    )
    list_select_related = (
        'person',
        'type',
        'municipality',
    )
    raw_id_fields = ('person', 'type', 'municipality')
    search_fields = (
        'id',
        'street_number',
        'street',
        'city',
        'person__first_name',
        'person__last_name',
    )
    list_filter = ('is_primary', )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            if obj.is_primary:
                return self.readonly_fields + ('is_primary', 'person',)
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        delete = True
        if obj is not None:
            if obj.is_primary:
                delete = False
        return delete


@admin.register(PersonEmail)
class PersonEmailAdmin(BaseAdmin):
    readonly_fields = (
        'id',
        'added',
        'updated',
    )
    list_display = (
        'id',
        'email',
        'person',
        'type',
        'is_primary',
    )
    list_select_related = (
        'person',
        'type',
    )
    raw_id_fields = (
        'person',
        'type',
    )
    search_fields = (
        'id',
        'email',
        'person__first_name',
        'person__last_name',
    )
    list_filter = ('is_primary', )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            if obj.is_primary:
                return self.readonly_fields + ('is_primary', 'person',)
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        change = True
        if obj is not None:
            if obj.is_primary:
                change = False
        return change


@admin.register(CompanyEmail)
class CompanyEmailAdmin(BaseAdmin):
    readonly_fields = (
        'id',
        'added',
        'updated',
    )
    list_display = (
        'id',
        'email',
        'company',
        'type',
        'is_primary',
    )
    list_select_related = (
        'company',
        'type',
    )
    raw_id_fields = (
        'company',
        'type',
    )
    search_fields = (
        'id',
        'email',
        'company__name',
    )
    list_filter = ('is_primary', )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            if obj.is_primary:
                return self.readonly_fields + ('is_primary', 'company', )
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        change = True
        if obj is not None:
            if obj.is_primary:
                change = False
        return change


@admin.register(PersonTelephone)
class PersonTelephoneAdmin(BaseAdmin):
    readonly_fields = (
        'id',
        'added',
        'updated',
    )
    list_display = (
        'id',
        'number',
        'person',
        'type',
        'is_primary',
    )
    list_select_related = (
        'person',
        'type',
    )
    raw_id_fields = (
        'person',
        'type',
    )
    search_fields = (
        'id',
        'number',
        'person__first_name',
        'person__last_name',
    )
    list_filter = ('is_primary', )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            if obj.is_primary:
                return self.readonly_fields + ('is_primary', 'person',)
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        delete = True
        if obj is not None:
            if obj.is_primary:
                delete = False
        return delete


@admin.register(CompanyTelephone)
class CompanyTelephoneAdmin(BaseAdmin):
    readonly_fields = (
        'id',
        'added',
        'updated',
    )
    list_display = (
        'id',
        'number',
        'company',
        'type',
        'is_primary',
    )
    list_select_related = (
        'company',
        'type',
    )
    raw_id_fields = (
        'company',
        'type',
    )
    search_fields = (
        'id',
        'number',
        'company__name',
    )
    list_filter = ('is_primary', )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            if obj.is_primary:
                return self.readonly_fields + ('is_primary', 'company', )
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        change = True
        if obj is not None:
            if obj.is_primary:
                change = False
        return change


@admin.register(PersonAttachment)
class PersonAttachmentAdmin(BaseAdmin):
    readonly_fields = (
        'id',
        'added',
        'updated',
    )
    list_display = ('id', 'person', 'file', 'added', 'updated')
    list_select_related = ('person', )
    raw_id_fields = ('person', 'attachment_type')


@admin.register(Person)
class PersonAdmin(BaseAdmin):
    readonly_fields = (
        'id',
        'added',
        'updated',
    )
    list_display = ('id', 'first_name', 'last_name')
    search_fields = (
        'id',
        'first_name',
        'last_name',
    )

    inlines = [
        PersonAddressAdminInline,
        PersonTelephoneAdminInline,
        PersonEmailAdminInline,
        PersonAttachmentAdminInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        help_texts = {
            'use_company_data':
            _('if available use company data in invoices along with the registry data'
              )
        }
        kwargs.update({'help_texts': help_texts})
        return super().get_form(request, obj, **kwargs)

    def get_deleted_objects(self, objs, request):
        r"""
        See
        https://stackoverflow.com/a/59303533
        Allow deleting related objects if their model is present in admin_site
        and user does not have permissions to delete them from admin web
        """
        deleted_objects, model_count, perms_needed, protected = \
            super().get_deleted_objects(objs, request)
        return deleted_objects, model_count, set(), protected


@admin.register(Company)
class CompanyAdmin(BaseAdmin):
    readonly_fields = (
        'id',
        'added',
        'updated',
    )
    list_display = (
        'id',
    )

    search_fields = ('id', )

    inlines = [
        CompanyAddressAdminInline,
        CompanyTelephoneAdminInline,
        CompanyEmailAdminInline,
    ]
