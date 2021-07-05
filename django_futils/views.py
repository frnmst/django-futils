#
# views.py
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

from django.shortcuts import get_list_or_404
from .default_models import AddressType, TelephoneType, EmailType, AttachmentType, Person, PersonAddress, PersonTelephone, PersonEmail, PersonAttachment, Company, CompanyAddress, CompanyTelephone, CompanyEmail, Municipality
from . import abstract_views as DFU_abstract_views
from django.conf import settings

# Here you can override:
#   template_name
#   paginate_by


################
# Detail Views #
################
# Type views #
##############
class AddressTypeDetailView(DFU_abstract_views.AbstractAddressTypeDetailView):
    model = AddressType

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': settings.VIEWS_APP_LABEL, 'model_name': 'addresstype'},
        )


class TelephoneTypeDetailView(DFU_abstract_views.AbstractTelephoneTypeDetailView):
    model = TelephoneType

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': settings.VIEWS_APP_LABEL, 'model_name': 'telephonetype'},
        )


class EmailTypeDetailView(DFU_abstract_views.AbstractEmailTypeDetailView):
    model = EmailType

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': settings.VIEWS_APP_LABEL, 'model_name': 'emailtype'},
        )


class AttachmentTypeDetailView(DFU_abstract_views.AbstractAttachmentTypeDetailView):
    model = AttachmentType

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': settings.VIEWS_APP_LABEL, 'model_name': 'attachmenttype'},
        )


# Normal views #
################
# Person.
class PersonDetailView(DFU_abstract_views.AbstractPersonDetailView):
    model = Person

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': settings.VIEWS_APP_LABEL, 'model_name': 'person'},
            person_address_list_view_reverse_url=settings.reverse_urls['PersonAddressListView'],
            person_telephone_list_view_reverse_url=settings.reverse_urls['PersonTelephoneListView'],
            person_email_list_view_reverse_url=settings.reverse_urls['PersonEmailListView'],
            person_address_detail_view_reverse_url=settings.reverse_urls['PersonAddressDetailView'],
            person_telephone_detail_view_reverse_url=settings.reverse_urls['PersonTelephoneDetailView'],
            person_email_detail_view_reverse_url=settings.reverse_urls['PersonEmailDetailView'],
        )


class PersonAddressDetailView(DFU_abstract_views.AbstractPersonAddressDetailView):
    model = PersonAddress

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': settings.VIEWS_APP_LABEL, 'model_name': 'personaddress'},
            addresstype_detail_view_reverse_url=settings.reverse_urls['AddressTypeDetailView'],
            municipality_detail_view_reverse_url=settings.reverse_urls['MunicipalityDetailView'],
            person_detail_view_reverse_url=settings.reverse_urls['PersonDetailView'],
        )


class PersonTelephoneDetailView(DFU_abstract_views.AbstractPersonTelephoneDetailView):
    model = PersonTelephone

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': settings.VIEWS_APP_LABEL, 'model_name': 'persontelephone'},
            telephonetype_detail_view_reverse_url=settings.reverse_urls['TelephoneTypeDetailView'],
            person_detail_view_reverse_url=settings.reverse_urls['PersonDetailView'],
        )


class PersonEmailDetailView(DFU_abstract_views.AbstractPersonEmailDetailView):
    model = PersonEmail

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': settings.VIEWS_APP_LABEL, 'model_name': 'personemail'},
            emailtype_detail_view_reverse_url=settings.reverse_urls['EmailTypeDetailView'],
            person_detail_view_reverse_url=settings.reverse_urls['PersonDetailView'],
        )


class PersonAttachmentDetailView(DFU_abstract_views.AbstractPersonAttachmentDetailView):
    model = PersonAttachment

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': settings.VIEWS_APP_LABEL, 'model_name': 'personattachment'},
            attachmenttype_detail_view_reverse_url=settings.reverse_urls['AttachmentTypeDetailView'],
            person_detail_view_reverse_url=settings.reverse_urls['PersonDetailView'],
        )


# Company.
class CompanyDetailView(DFU_abstract_views.AbstractCompanyDetailView):
    model = Company

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': settings.VIEWS_APP_LABEL, 'model_name': 'company'},
            company_address_list_view_reverse_url=settings.reverse_urls['CompanyAddressListView'],
            company_telephone_list_view_reverse_url=settings.reverse_urls['CompanyTelephoneListView'],
            company_email_list_view_reverse_url=settings.reverse_urls['CompanyEmailListView'],
            company_address_detail_view_reverse_url=settings.reverse_urls['CompanyAddressDetailView'],
            company_telephone_detail_view_reverse_url=settings.reverse_urls['CompanyTelephoneDetailView'],
            company_email_detail_view_reverse_url=settings.reverse_urls['CompanyEmailDetailView'],
        )


class CompanyAddressDetailView(DFU_abstract_views.AbstractCompanyAddressDetailView):
    model = CompanyAddress

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': settings.VIEWS_APP_LABEL, 'model_name': 'companyaddress'},
            addresstype_detail_view_reverse_url=settings.reverse_urls['AddressTypeDetailView'],
            municipality_detail_view_reverse_url=settings.reverse_urls['MunicipalityDetailView'],
            company_detail_view_reverse_url=settings.reverse_urls['CompanyDetailView'],
        )


class CompanyTelephoneDetailView(DFU_abstract_views.AbstractCompanyTelephoneDetailView):
    model = CompanyTelephone

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': settings.VIEWS_APP_LABEL, 'model_name': 'companytelephone'},
            telephonetype_detail_view_reverse_url=settings.reverse_urls['TelephoneTypeDetailView'],
            company_detail_view_reverse_url=settings.reverse_urls['CompanyDetailView'],
        )


class CompanyEmailDetailView(DFU_abstract_views.AbstractCompanyEmailDetailView):
    model = CompanyEmail

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': settings.VIEWS_APP_LABEL, 'model_name': 'companyemail'},
            emailtype_detail_view_reverse_url=settings.reverse_urls['EmailTypeDetailView'],
            company_detail_view_reverse_url=settings.reverse_urls['CompanyDetailView'],
        )


# Other.
class MunicipalityDetailView(DFU_abstract_views.AbstractMunicipalityDetailView):
    model = Municipality

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': settings.VIEWS_APP_LABEL, 'model_name': 'municipality'},
        )


##############
# List views #
##############
# Person.
class PersonAddressListView(DFU_abstract_views.AbstractPersonAddressListView):
    model = PersonAddress

    def get_queryset(self):
        return get_list_or_404(self.model.objects.filter(person=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            person_detail_view_reverse_url=settings.reverse_urls['PersonDetailView'],
            person_address_detail_view_reverse_url=settings.reverse_urls['PersonAddressDetailView'],
            person=Person.objects.get(id=self.kwargs['pk']),
        )


class PersonTelephoneListView(DFU_abstract_views.AbstractPersonTelephoneListView):
    model = PersonTelephone

    def get_queryset(self):
        return get_list_or_404(self.model.objects.filter(person=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            person_detail_view_reverse_url=settings.reverse_urls['PersonDetailView'],
            person_telephone_detail_view_reverse_url=settings.reverse_urls['PersonTelephoneDetailView'],
            person=Person.objects.get(id=self.kwargs['pk']),
        )


class PersonEmailListView(DFU_abstract_views.AbstractPersonEmailListView):
    model = PersonEmail

    def get_queryset(self):
        return get_list_or_404(self.model.objects.filter(person=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            person_detail_view_reverse_url=settings.reverse_urls['PersonDetailView'],
            person_email_detail_view_reverse_url=settings.reverse_urls['PersonEmailDetailView'],
            person=Person.objects.get(id=self.kwargs['pk']),
        )


# Company.
class CompanyAddressListView(DFU_abstract_views.AbstractCompanyAddressListView):
    model = CompanyAddress

    def get_queryset(self):
        return get_list_or_404(self.model.objects.filter(company=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            company_detail_view_reverse_url=settings.reverse_urls['CompanyDetailView'],
            company_address_detail_view_reverse_url=settings.reverse_urls['CompanyAddressDetailView'],
            company=Company.objects.get(id=self.kwargs['pk']),
        )


class CompanyTelephoneListView(DFU_abstract_views.AbstractCompanyTelephoneListView):
    model = CompanyTelephone

    def get_queryset(self):
        return get_list_or_404(self.model.objects.filter(company=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            company_detail_view_reverse_url=settings.reverse_urls['CompanyDetailView'],
            company_telephone_detail_view_reverse_url=settings.reverse_urls['CompanyTelephoneDetailView'],
            company=Company.objects.get(id=self.kwargs['pk']),
        )


class CompanyEmailListView(DFU_abstract_views.AbstractCompanyEmailListView):
    model = CompanyEmail

    def get_queryset(self):
        return get_list_or_404(self.model.objects.filter(company=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            company_detail_view_reverse_url=settings.reverse_urls['CompanyDetailView'],
            company_email_detail_view_reverse_url=settings.reverse_urls['CompanyEmailDetailView'],
            company=Company.objects.get(id=self.kwargs['pk']),
        )
