from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_list_or_404

from .default_models import AddressType, TelephoneType, EmailType, Person, PersonAddress, PersonTelephone, PersonEmail, PersonAttachment, Company, Municipality


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
class AddressTypeDetailView(BasePermissions, generic.DetailView):
    model = AddressType
    template_name = 'django_futils/addresstype_detail.html'


class TelephoneTypeDetailView(BasePermissions, generic.DetailView):
    model = TelephoneType
    template_name = 'django_futils/telephonetype_detail.html'


class EmailTypeDetailView(BasePermissions, generic.DetailView):
    model = EmailType
    template_name = 'django_futils/emailtype_detail.html'


# Normal views.
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


class CompanyDetailView(BasePermissions, generic.DetailView):
    model = Company
    template_name = 'django_futils/company_detail.html'


class MunicipalityDetailView(BasePermissions, generic.DetailView):
    model = Municipality
    template_name = 'django_futils/municipality_detail.html'


##############
# List views #
##############
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
