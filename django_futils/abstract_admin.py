#
# abstract_admin.py
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
from import_export import resources
from . import abstract_models
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from .formsets import HasPrimaryInlineFormSet
from django.conf import settings
from . import constants as const


#################
# Import Export #
#################
class AbstractRecordTimestampsResource(resources.ModelResource):
    class Meta:
        model = abstract_models.AbstractRecordTimestamps


class AbstractBasicElementResource(resources.ModelResource):
    class Meta:
        model = abstract_models.AbstractBasicElement


################
# Base classes #
################
class BaseAdmin(SimpleHistoryAdmin, ImportExportActionModelAdmin):
    list_per_page = 10
    readonly_fields = ('id', 'serial_id', )
    ordering = ('id',)
    change_form_template = "django_futils/detail_change_form.html"
    list_display_links = ('id', 'serial_id', )


class TypeBaseAdmin(BaseAdmin):
    readonly_fields = ('id', 'serial_id', )
    list_display = (
        'id',
        'serial_id',
        'code',
        'type',
    )


class NameBaseAdmin(BaseAdmin):
    readonly_fields = ('id', 'serial_id', )
    list_display = (
        'id',
        'serial_id',
        'code',
        'name',
    )


class BaseAdminInline(admin.StackedInline):
    SHOW_IDS = True
    if SHOW_IDS:
        readonly_fields = ('id', 'serial_id', )
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
    modifiable = True
    openlayers_url = settings.OPENLAYERS_URL


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

class AbstractCompanyAddressAdmin(AddressCommonAdmin):
    readonly_fields = (
        'id',
        'serial_id',
        'added',
        'updated',
    )
    list_display = (
        'id',
        'serial_id',
        'street_number',
        'street',
        'city',
        'company',
        'type',
        'is_primary',
    )
    list_select_related = ('company', )
    list_per_page = 10
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = (
            'company',
            'type',
            'municipality',
        )
    elif settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        autocomplete_fields = (
            'company',
            'type',
            'municipality',
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

    search_fields = (
        'id',
        'street_number',
        'street',
        'city',
        'company__name',
    )


class AbstractAddressTypeAdmin(TypeBaseAdmin):
    search_fields = ('type',)


class AbstractEmailTypeAdmin(TypeBaseAdmin):
    search_fields = ('type',)


class AbstractTelephoneTypeAdmin(TypeBaseAdmin):
    search_fields = ('type',)


class AbstractAttachmentTypeAdmin(TypeBaseAdmin):
    search_fields = ('type',)


class AbstractMunicipalityAdmin(NameBaseAdmin):
    search_fields = ('name',)


class AbstractGeocoderCacheAdmin(OSMGeoAdmin, BaseAdmin):
    readonly_fields = (
        'id',
        'serial_id',
        'added',
        'updated',
        'cache_hits',
    )
    list_display = (
        'id',
        'serial_id',
        'street_number',
        'street',
        'city',
        'country_code',
    )


###########
# Inlines #
###########
class AbstractCompanyAddressAdminInline(BaseOneElementMandatoryAdminInline):
    formset = HasPrimaryInlineFormSet
    readonly_fields = BaseAdminInline.readonly_fields + (
        'is_primary',
    )
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = (
            'company',
            'type',
            'municipality',
        )
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        autocomplete_fields = (
            'company',
            'type',
            'municipality',
        )
    exclude = ('map', )


class AbstractCompanyAdminInline(BaseAdminInline):
    readonly_fields = BaseAdminInline.readonly_fields + (
        'is_primary',
    )


class AbstractPersonAddressAdminInline(BaseOneElementMandatoryAdminInline):
    formset = HasPrimaryInlineFormSet
    readonly_fields = BaseAdminInline.readonly_fields + (
        'is_primary',
    )
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = (
            'type',
            'municipality',
        )
    elif settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        autocomplete_fields = (
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


class AbstractPersonEmailAdminInline(BaseAdminInline):
    formset = HasPrimaryInlineFormSet
    readonly_fields = (
        'id',
        'serial_id',
        'is_primary',
    )
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = ('type', )
    elif settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        autocomplete_fields = ('type', )


class AbstractCompanyEmailAdminInline(BaseAdminInline):
    formset = HasPrimaryInlineFormSet
    readonly_fields = (
        'id',
        'serial_id',
        'is_primary',
    )
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = ('type', )
    elif settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        autocomplete_fields = ('type', )


class AbstractPersonTelephoneAdminInline(BaseOneElementMandatoryAdminInline):
    formset = HasPrimaryInlineFormSet
    readonly_fields = (
        'id',
        'serial_id',
        'is_primary',
    )
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = ('type', )
    elif settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        autocomplete_fields = ('type', )


class AbstractCompanyTelephoneAdminInline(BaseOneElementMandatoryAdminInline):
    formset = HasPrimaryInlineFormSet
    readonly_fields = (
        'id',
        'serial_id',
        'is_primary',
    )
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = ('type', )
    elif settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        autocomplete_fields = ('type', )


class AbstractPersonAdminInline(BaseAdminInline):
    readonly_fields = (
        'id',
        'serial_id',
    )


class AbstractPersonAttachmentAdminInline(BaseAdminInline):
    readonly_fields = ('id', 'serial_id', )
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = (
            'type',
        )
    elif settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        autocomplete_fields = (
            'type',
        )


########
# Main #
########
class AbstractPersonAddressAdmin(AddressCommonAdmin):
    readonly_fields = (
        'id',
        'serial_id',
        'added',
        'updated',
    )
    list_display = (
        'id',
        'serial_id',
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
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = (
            'person',
            'type',
            'municipality',
        )
    elif settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        autocomplete_fields = (
            'person',
            'type',
            'municipality',
        )
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


class AbstractPersonEmailAdmin(BaseAdmin):
    readonly_fields = (
        'id',
        'serial_id',
        'added',
        'updated',
    )
    list_display = (
        'id',
        'serial_id',
        'email',
        'person',
        'type',
        'is_primary',
    )
    list_select_related = (
        'person',
        'type',
    )
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = (
            'person',
            'type',
        )
    elif settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        autocomplete_fields = (
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


class AbstractCompanyEmailAdmin(BaseAdmin):
    readonly_fields = (
        'id',
        'serial_id',
        'added',
        'updated',
    )
    list_display = (
        'id',
        'serial_id',
        'email',
        'company',
        'type',
        'is_primary',
    )
    list_select_related = (
        'company',
        'type',
    )
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = (
            'company',
            'type',
        )
    elif settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        autocomplete_fields = (
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


class AbstractPersonTelephoneAdmin(BaseAdmin):
    readonly_fields = (
        'id',
        'serial_id',
        'added',
        'updated',
    )
    list_display = (
        'id',
        'serial_id',
        'number',
        'person',
        'type',
        'is_primary',
    )
    list_select_related = (
        'person',
        'type',
    )
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = (
            'person',
            'type',
        )
    elif settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        autocomplete_fields = (
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


class AbstractCompanyTelephoneAdmin(BaseAdmin):
    readonly_fields = (
        'id',
        'serial_id',
        'added',
        'updated',
    )
    list_display = (
        'id',
        'serial_id',
        'number',
        'company',
        'type',
        'is_primary',
    )
    list_select_related = (
        'company',
        'type',
    )
    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = (
            'company',
            'type',
        )
    elif settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        autocomplete_fields = (
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


class AbstractPersonAttachmentAdmin(BaseAdmin):
    readonly_fields = (
        'id',
        'serial_id',
        'added',
        'updated',
    )
    list_display = ('id', 'serial_id', 'person', 'file', 'added', 'updated')
    list_select_related = ('person', )
    search_fields = (
        'id',
        'person__first_name',
        'person__last_name',
    )

    if settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_RAW:
        raw_id_fields = (
            'person',
            'type',
        )
    elif settings.FOREIGN_KEY_FIELDS == const.FOREIGN_KEY_FIELDS_AUTOCOMPLETE:
        autocomplete_fields = (
            'person',
            'type',
        )


class AbstractPersonAdmin(BaseAdmin):
    readonly_fields = (
        'id',
        'serial_id',
        'added',
        'updated',
    )
    list_display = (
        'id',
        'serial_id',
        'first_name',
        'last_name',
        'fiscal_code',
    )
    search_fields = (
        'first_name',
        'last_name',
        'fiscal_code',
    )

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


class AbstractCompanyAdmin(BaseAdmin):
    readonly_fields = (
        'id',
        'serial_id',
        'serial_id',
        'added',
        'updated',
        'is_primary',
    )
    list_display = (
        'id',
        'serial_id',
        'name',
        'vat',
    )
    search_fields = ('name', 'vat', )
