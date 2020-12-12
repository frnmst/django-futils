from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .default_models import AddressType, Person, PersonAddress, Company, Municipality


class BasePermissions(LoginRequiredMixin):
    r"""See
        https://docs.djangoproject.com/en/3.1/topics/auth/default/#the-loginrequired-mixin
    """
    login_url = '/admin/login/'
    redirect_field_name = 'next'


class PersonView(BasePermissions, generic.DetailView):
    model = Person
    template_name = 'django_futils/person_object.html'


class PersonAddressView(BasePermissions, generic.DetailView):
    model = PersonAddress
    template_name = 'django_futils/personaddress_object.html'


class CompanyView(BasePermissions, generic.DetailView):
    model = Company
    template_name = 'django_futils/company_object.html'


class MunicipalityView(BasePermissions, generic.DetailView):
    model = Municipality
    template_name = 'django_futils/municipality_object.html'


##############
# Type views #
##############
class AddressTypeView(BasePermissions, generic.DetailView):
    model = AddressType
    template_name = 'django_futils/addresstype_object.html'
