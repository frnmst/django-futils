#
# views.py
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

from dal import autocomplete
from django.db.models import Q

from .models import AddressType, EmailType, TelephoneType, AttachmentType, Municipality, PersonTelephone, CompanyTelephone, PersonEmail, CompanyEmail, PersonAddress, CompanyAddress, PersonAttachment, Person, Company

################
# Autocomplete #
################

################
# Foreign keys #


class CompanyFKAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Company.objects.none()

        qs = Company.objects.all().order_by('id')

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class AddressTypeFKAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return AddressType.objects.none()

        qs = AddressType.objects.all().order_by('id')

        if self.q:
            qs = qs.filter(type__istartswith=self.q)

        return qs


class TelephoneTypeFKAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return TelephoneType.objects.none()

        qs = TelephoneType.objects.all().order_by('id')

        if self.q:
            qs = qs.filter(type__istartswith=self.q)

        return qs


class EmailTypeFKAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return EmailType.objects.none()

        qs = EmailType.objects.all().order_by('id')

        if self.q:
            qs = qs.filter(type__istartswith=self.q)

        return qs


class PersonFKAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Person.objects.none()

        qs = Person.objects.all().order_by('id')

        if self.q:
            qs = qs.filter(Q(first_name__istartswith=self.q) | Q(last_name__istartswith=self.q) | Q(fiscal_code__istartswith=self.q))

        return qs


class MunicipalityFKAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Municipality.objects.none()

        qs = Municipality.objects.all().order_by('id')

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class AttachmentTypeFKAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return AttachmentType.objects.none()

        qs = AttachmentType.objects.all().order_by('id')

        if self.q:
            qs = qs.filter(type__istartswith=self.q)

        return qs
