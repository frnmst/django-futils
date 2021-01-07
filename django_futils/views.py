from django.shortcuts import get_list_or_404
from .default_models import AddressType, TelephoneType, EmailType, AttachmentType, Person, PersonAddress, PersonTelephone, PersonEmail, PersonAttachment, Company, CompanyAddress, CompanyTelephone, CompanyEmail, Municipality
from .abstract_views import AbstractAddressTypeDetailView, AbstractTelephoneTypeDetailView, AbstractEmailTypeDetailView, AbstractAttachmentTypeDetailView, AbstractPersonDetailView, AbstractPersonAddressDetailView, AbstractPersonTelephoneDetailView, AbstractPersonEmailDetailView, AbstractPersonAttachmentDetailView, AbstractCompanyDetailView, AbstractCompanyAddressDetailView, AbstractCompanyTelephoneDetailView, AbstractCompanyEmailDetailView, AbstractMunicipalityDetailView, AbstractPersonAddressListView, AbstractPersonTelephoneListView, AbstractPersonEmailListView, AbstractCompanyAddressListView, AbstractCompanyTelephoneListView, AbstractCompanyEmailListView
from django.conf import settings

# Here you can override:
#   template_name
#   paginate_by


################
# Detail Views #
################
# Type views #
##############
class AddressTypeDetailView(AbstractAddressTypeDetailView):
    model = AddressType

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': 'django_futils', 'model_name': 'addresstype'},
        )


class TelephoneTypeDetailView(AbstractTelephoneTypeDetailView):
    model = TelephoneType

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': 'django_futils', 'model_name': 'telephonetype'},
        )


class EmailTypeDetailView(AbstractEmailTypeDetailView):
    model = EmailType

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': 'django_futils', 'model_name': 'emailtype'},
        )


class AttachmentTypeDetailView(AbstractAttachmentTypeDetailView):
    model = AttachmentType

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': 'django_futils', 'model_name': 'attachmenttype'},
        )


# Normal views #
################
# Person.
class PersonDetailView(AbstractPersonDetailView):
    model = Person

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': 'django_futils', 'model_name': 'person'},
            person_address_list_view_reverse_url=settings.reverse_urls['PersonAddressListView'],
            person_telephone_list_view_reverse_url=settings.reverse_urls['PersonTelephoneListView'],
            person_email_list_view_reverse_url=settings.reverse_urls['PersonEmailListView'],
            person_address_detail_view_reverse_url=settings.reverse_urls['PersonAddressDetailView'],
            person_telephone_detail_view_reverse_url=settings.reverse_urls['PersonTelephoneDetailView'],
            person_email_detail_view_reverse_url=settings.reverse_urls['PersonEmailDetailView'],
        )


class PersonAddressDetailView(AbstractPersonAddressDetailView):
    model = PersonAddress

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': 'django_futils', 'model_name': 'personaddress'},
            addresstype_detail_view_reverse_url=settings.reverse_urls['AddressTypeDetailView'],
            municipality_detail_view_reverse_url=settings.reverse_urls['MunicipalityDetailView'],
            person_detail_view_reverse_url=settings.reverse_urls['PersonDetailView'],
        )


class PersonTelephoneDetailView(AbstractPersonTelephoneDetailView):
    model = PersonTelephone

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': 'django_futils', 'model_name': 'persontelephone'},
            telephonetype_detail_view_reverse_url=settings.reverse_urls['TelephoneTypeDetailView'],
            person_detail_view_reverse_url=settings.reverse_urls['PersonDetailView'],
        )


class PersonEmailDetailView(AbstractPersonEmailDetailView):
    model = PersonEmail

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': 'django_futils', 'model_name': 'personemail'},
            emailtype_detail_view_reverse_url=settings.reverse_urls['EmailTypeDetailView'],
            person_detail_view_reverse_url=settings.reverse_urls['PersonDetailView'],
        )


class PersonAttachmentDetailView(AbstractPersonAttachmentDetailView):
    model = PersonAttachment

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': 'django_futils', 'model_name': 'personattachment'},
            attachmenttype_detail_view_reverse_url=settings.reverse_urls['AttachmentTypeDetailView'],
            person_detail_view_reverse_url=settings.reverse_urls['PersonDetailView'],
        )


# Company.
class CompanyDetailView(AbstractCompanyDetailView):
    model = Company

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': 'django_futils', 'model_name': 'company'},
            company_address_list_view_reverse_url=settings.reverse_urls['CompanyAddressListView'],
            company_telephone_list_view_reverse_url=settings.reverse_urls['CompanyTelephoneListView'],
            company_email_list_view_reverse_url=settings.reverse_urls['CompanyEmailListView'],
            company_address_detail_view_reverse_url=settings.reverse_urls['CompanyAddressDetailView'],
            company_telephone_detail_view_reverse_url=settings.reverse_urls['CompanyTelephoneDetailView'],
            company_email_detail_view_reverse_url=settings.reverse_urls['CompanyEmailDetailView'],
        )


class CompanyAddressDetailView(AbstractCompanyAddressDetailView):
    model = CompanyAddress

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': 'django_futils', 'model_name': 'companyaddress'},
            addresstype_detail_view_reverse_url=settings.reverse_urls['AddressTypeDetailView'],
            municipality_detail_view_reverse_url=settings.reverse_urls['MunicipalityDetailView'],
            company_detail_view_reverse_url=settings.reverse_urls['CompanyDetailView'],
        )


class CompanyTelephoneDetailView(AbstractCompanyTelephoneDetailView):
    model = CompanyTelephone

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': 'django_futils', 'model_name': 'companytelephone'},
            telephonetype_detail_view_reverse_url=settings.reverse_urls['TelephoneTypeDetailView'],
            company_detail_view_reverse_url=settings.reverse_urls['CompanyDetailView'],
        )


class CompanyEmailDetailView(AbstractCompanyEmailDetailView):
    model = CompanyEmail

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': 'django_futils', 'model_name': 'companyemail'},
            emailtype_detail_view_reverse_url=settings.reverse_urls['EmailTypeDetailView'],
            company_detail_view_reverse_url=settings.reverse_urls['CompanyDetailView'],
        )


# Other.
class MunicipalityDetailView(AbstractMunicipalityDetailView):
    model = Municipality

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            opts={'app_label': 'django_futils', 'model_name': 'municipality'},
        )


##############
# List views #
##############
# Person.
class PersonAddressListView(AbstractPersonAddressListView):
    model = PersonAddress

    def get_queryset(self):
        return get_list_or_404(self.model.objects.filter(person=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            person_detail_view_reverse_url=settings.reverse_urls['PersonDetailView'],
            person_address_detail_view_reverse_url=settings.reverse_urls['PersonAddressDetailView'],
            person=Person.objects.get(id=self.kwargs['pk']),
        )


class PersonTelephoneListView(AbstractPersonTelephoneListView):
    model = PersonTelephone

    def get_queryset(self):
        return get_list_or_404(self.model.objects.filter(person=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            person_detail_view_reverse_url=settings.reverse_urls['PersonDetailView'],
            person_telephone_detail_view_reverse_url=settings.reverse_urls['PersonTelephoneDetailView'],
            person=Person.objects.get(id=self.kwargs['pk']),
        )


class PersonEmailListView(AbstractPersonEmailListView):
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
class CompanyAddressListView(AbstractCompanyAddressListView):
    model = CompanyAddress

    def get_queryset(self):
        return get_list_or_404(self.model.objects.filter(company=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            company_detail_view_reverse_url=settings.reverse_urls['CompanyDetailView'],
            company_address_detail_view_reverse_url=settings.reverse_urls['CompanyAddressDetailView'],
            company=Company.objects.get(id=self.kwargs['pk']),
        )


class CompanyTelephoneListView(AbstractCompanyTelephoneListView):
    model = CompanyTelephone

    def get_queryset(self):
        return get_list_or_404(self.model.objects.filter(company=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            company_detail_view_reverse_url=settings.reverse_urls['CompanyDetailView'],
            company_telephone_detail_view_reverse_url=settings.reverse_urls['CompanyTelephoneDetailView'],
            company=Company.objects.get(id=self.kwargs['pk']),
        )


class CompanyEmailListView(AbstractCompanyEmailListView):
    model = CompanyEmail

    def get_queryset(self):
        return get_list_or_404(self.model.objects.filter(company=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            company_detail_view_reverse_url=settings.reverse_urls['CompanyDetailView'],
            company_email_detail_view_reverse_url=settings.reverse_urls['CompanyEmailDetailView'],
            company=Company.objects.get(id=self.kwargs['pk']),
        )
