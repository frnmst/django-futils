from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_list_or_404

from .default_models import AddressType, TelephoneType, Person, PersonAddress, PersonTelephone, PersonEmail, Company, Municipality


class BasePermissions(LoginRequiredMixin):
    r"""See
        https://docs.djangoproject.com/en/3.1/topics/auth/default/#the-loginrequired-mixin
    """
    login_url = '/admin/login/'
    redirect_field_name = 'next'


################
# Detail Views #
################


# Type views.
class AddressTypeView(BasePermissions, generic.DetailView):
    model = AddressType
    template_name = 'django_futils/addresstype_object.html'


class TelephoneTypeView(BasePermissions, generic.DetailView):
    model = TelephoneType
    template_name = 'django_futils/telephonetype_object.html'


# Normal views.
class PersonView(BasePermissions, generic.DetailView):
    model = Person
    template_name = 'django_futils/person_object.html'


class PersonAddressView(BasePermissions, generic.DetailView):
    model = PersonAddress
    template_name = 'django_futils/personaddress_object.html'


class PersonTelephoneView(BasePermissions, generic.DetailView):
    model = PersonTelephone
    template_name = 'django_futils/persontelephone_object.html'


class PersonEmailView(BasePermissions, generic.DetailView):
    model = PersonEmail
    template_name = 'django_futils/personemail_object.html'


class CompanyView(BasePermissions, generic.DetailView):
    model = Company
    template_name = 'django_futils/company_object.html'


class MunicipalityView(BasePermissions, generic.DetailView):
    model = Municipality
    template_name = 'django_futils/municipality_object.html'


# List views.
class PersonAddressListView(BasePermissions, generic.ListView):
    model = PersonAddress
    template_name = 'django_futils/personaddress_list.html'

    def get_queryset(self):
        queryset = PersonAddress.objects.filter(person=self.kwargs['pk'])[:10]
        return get_list_or_404(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person'] = Person.objects.get(id=self.kwargs['pk'])
        return context
