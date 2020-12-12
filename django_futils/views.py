from django.views import generic
from .default_models import AddressType, Person, PersonAddress, Company, Municipality


class PersonView(generic.DetailView):
    model = Person
    template_name = 'django_futils/person_object.html'


class PersonAddressView(generic.DetailView):
    model = PersonAddress
    template_name = 'django_futils/personaddress_object.html'


class CompanyView(generic.DetailView):
    model = Company
    template_name = 'django_futils/company_object.html'


class MunicipalityView(generic.DetailView):
    model = Municipality
    template_name = 'django_futils/municipality_object.html'


# Type views.
class AddressTypeView(generic.DetailView):
    model = AddressType
    template_name = 'django_futils/addresstype_object.html'
