from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_list_or_404

from .default_models import AddressType, TelephoneType, EmailType, Person, PersonAddress, PersonTelephone, PersonEmail, PersonAttachment, Company, CompanyAddress, CompanyTelephone, CompanyEmail, Municipality


class BasePermissions(LoginRequiredMixin):
    r"""See
        https://docs.djangoproject.com/en/3.1/topics/auth/default/#the-loginrequired-mixin
    """
    login_url = '/admin/login/'
    redirect_field_name = 'next'


################
# Detail Views #
################
# Type views #
##############
class AddressTypeDetailView(BasePermissions, generic.DetailView):
    model = AddressType
    template_name = 'django_futils/addresstype_detail.html'


class TelephoneTypeDetailView(BasePermissions, generic.DetailView):
    model = TelephoneType
    template_name = 'django_futils/telephonetype_detail.html'


class EmailTypeDetailView(BasePermissions, generic.DetailView):
    model = EmailType
    template_name = 'django_futils/emailtype_detail.html'


# Normal views #
################
# Person.
class PersonDetailView(BasePermissions, generic.DetailView):
    model = Person
    template_name = 'django_futils/person_detail.html'


class PersonAddressDetailView(BasePermissions, generic.DetailView):
    model = PersonAddress
    template_name = 'django_futils/personaddress_detail.html'


class PersonTelephoneDetailView(BasePermissions, generic.DetailView):
    model = PersonTelephone
    template_name = 'django_futils/persontelephone_detail.html'


class PersonEmailDetailView(BasePermissions, generic.DetailView):
    model = PersonEmail
    template_name = 'django_futils/personemail_detail.html'


class PersonAttachmentDetailView(BasePermissions, generic.DetailView):
    model = PersonAttachment
    template_name = 'django_futils/personattachment_detail.html'


# Company.
class CompanyDetailView(BasePermissions, generic.DetailView):
    model = Company
    template_name = 'django_futils/company_detail.html'


class CompanyAddressDetailView(BasePermissions, generic.DetailView):
    model = CompanyAddress
    template_name = 'django_futils/companyaddress_detail.html'


class CompanyTelephoneDetailView(BasePermissions, generic.DetailView):
    model = CompanyTelephone
    template_name = 'django_futils/companytelephone_detail.html'


class CompanyEmailDetailView(BasePermissions, generic.DetailView):
    model = CompanyEmail
    template_name = 'django_futils/companyemail_detail.html'


class MunicipalityDetailView(BasePermissions, generic.DetailView):
    model = Municipality
    template_name = 'django_futils/municipality_detail.html'


##############
# List views #
##############
# Person.
class PersonAddressListView(BasePermissions, generic.ListView):
    model = PersonAddress
    template_name = 'django_futils/personaddress_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.filter(person=self.kwargs['pk'])
        return get_list_or_404(queryset)

    def get_context_data(self, **kwargs):
        r"""Pass the person object."""
        context = super().get_context_data(**kwargs)
        context['person'] = Person.objects.get(id=self.kwargs['pk'])
        return context


class PersonTelephoneListView(generic.ListView):
    model = PersonTelephone
    template_name = 'django_futils/persontelephone_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.filter(person=self.kwargs['pk'])
        return get_list_or_404(queryset)

    def get_context_data(self, **kwargs):
        r"""Pass the person object."""
        context = super().get_context_data(**kwargs)
        context['person'] = Person.objects.get(id=self.kwargs['pk'])
        return context


class PersonEmailListView(generic.ListView):
    model = PersonEmail
    template_name = 'django_futils/personemail_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.filter(person=self.kwargs['pk'])
        return get_list_or_404(queryset)

    def get_context_data(self, **kwargs):
        r"""Pass the person object."""
        context = super().get_context_data(**kwargs)
        context['person'] = Person.objects.get(id=self.kwargs['pk'])
        return context


class CompanyAddressListView(BasePermissions, generic.ListView):
    model = CompanyAddress
    template_name = 'django_futils/companyaddress_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.filter(company=self.kwargs['pk'])
        return get_list_or_404(queryset)

    def get_context_data(self, **kwargs):
        r"""Pass the company object."""
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.get(id=self.kwargs['pk'])
        return context


# Company.
class CompanyTelephoneListView(generic.ListView):
    model = CompanyTelephone
    template_name = 'django_futils/companytelephone_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.filter(company=self.kwargs['pk'])
        return get_list_or_404(queryset)

    def get_context_data(self, **kwargs):
        r"""Pass the company object."""
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.get(id=self.kwargs['pk'])
        return context


class CompanyEmailListView(generic.ListView):
    model = CompanyEmail
    template_name = 'django_futils/companyemail_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.filter(company=self.kwargs['pk'])
        return get_list_or_404(queryset)

    def get_context_data(self, **kwargs):
        r"""Pass the company object."""
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.get(id=self.kwargs['pk'])
        return context
