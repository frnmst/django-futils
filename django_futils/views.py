from .default_models import AddressType, TelephoneType, EmailType, Person, PersonAddress, PersonTelephone, PersonEmail, PersonAttachment, Company, CompanyAddress, CompanyTelephone, CompanyEmail, Municipality
from .abstract_views import AbstractAddressTypeDetailView, AbstractTelephoneTypeDetailView, AbstractEmailTypeDetailView, AbstractPersonDetailView, AbstractPersonAddressDetailView, AbstractPersonTelephoneDetailView, AbstractPersonEmailDetailView, AbstractPersonAttachmentDetailView, AbstractCompanyDetailView, AbstractCompanyAddressDetailView, AbstractCompanyTelephoneDetailView, AbstractCompanyEmailDetailView, AbstractMunicipalityDetailView, AbstractPersonAddressListView, AbstractPersonTelephoneListView, AbstractPersonEmailListView, AbstractCompanyAddressListView, AbstractCompanyTelephoneListView, AbstractCompanyEmailListView


################
# Detail Views #
################
# Type views #
##############
class AddressTypeDetailView(AbstractAddressTypeDetailView):
    model = AddressType


class TelephoneTypeDetailView(AbstractTelephoneTypeDetailView):
    model = TelephoneType


class EmailTypeDetailView(AbstractEmailTypeDetailView):
    model = EmailType


# Normal views #
################
# Person.
class PersonDetailView(AbstractPersonDetailView):
    model = Person


class PersonAddressDetailView(AbstractPersonAddressDetailView):
    model = PersonAddress


class PersonTelephoneDetailView(AbstractPersonTelephoneDetailView):
    model = PersonTelephone


class PersonEmailDetailView(AbstractPersonEmailDetailView):
    model = PersonEmail


class PersonAttachmentDetailView(AbstractPersonAttachmentDetailView):
    model = PersonAttachment


# Company.
class CompanyDetailView(AbstractCompanyDetailView):
    model = Company


class CompanyAddressDetailView(AbstractCompanyAddressDetailView):
    model = CompanyAddress


class CompanyTelephoneDetailView(AbstractCompanyTelephoneDetailView):
    model = CompanyTelephone


class CompanyEmailDetailView(AbstractCompanyEmailDetailView):
    model = CompanyEmail


class MunicipalityDetailView(AbstractMunicipalityDetailView):
    model = Municipality


##############
# List views #
##############
# Person.
class PersonAddressListView(AbstractPersonAddressListView):
    model = PersonAddress
    context_model = Person


class PersonTelephoneListView(AbstractPersonTelephoneListView):
    model = PersonTelephone
    context_model = Person


class PersonEmailListView(AbstractPersonEmailListView):
    model = PersonEmail
    context_model = Person


# Company.
class CompanyAddressListView(AbstractCompanyAddressListView):
    model = CompanyAddress
    context_model = Company


class CompanyTelephoneListView(AbstractCompanyTelephoneListView):
    model = CompanyTelephone
    context_model = Company


class CompanyEmailListView(AbstractCompanyEmailListView):
    model = CompanyEmail
    context_model = Company
