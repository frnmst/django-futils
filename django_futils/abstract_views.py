from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_list_or_404


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
class AbstractAddressTypeDetailView(BasePermissions, generic.DetailView):
    template_name = 'django_futils/addresstype_detail.html'


class AbstractTelephoneTypeDetailView(BasePermissions, generic.DetailView):
    template_name = 'django_futils/telephonetype_detail.html'


class AbstractEmailTypeDetailView(BasePermissions, generic.DetailView):
    template_name = 'django_futils/emailtype_detail.html'


class AbstractPersonDetailView(BasePermissions, generic.DetailView):
    template_name = 'django_futils/person_detail.html'


class AbstractPersonAddressDetailView(BasePermissions, generic.DetailView):
    template_name = 'django_futils/personaddress_detail.html'


class AbstractPersonTelephoneDetailView(BasePermissions, generic.DetailView):
    template_name = 'django_futils/persontelephone_detail.html'


class AbstractPersonEmailDetailView(BasePermissions, generic.DetailView):
    template_name = 'django_futils/personemail_detail.html'


class AbstractPersonAttachmentDetailView(BasePermissions, generic.DetailView):
    template_name = 'django_futils/personattachment_detail.html'


# Company.
class AbstractCompanyDetailView(BasePermissions, generic.DetailView):
    template_name = 'django_futils/company_detail.html'


class AbstractCompanyAddressDetailView(BasePermissions, generic.DetailView):
    template_name = 'django_futils/companyaddress_detail.html'


class AbstractCompanyTelephoneDetailView(BasePermissions, generic.DetailView):
    template_name = 'django_futils/companytelephone_detail.html'


class AbstractCompanyEmailDetailView(BasePermissions, generic.DetailView):
    template_name = 'django_futils/companyemail_detail.html'


class AbstractMunicipalityDetailView(BasePermissions, generic.DetailView):
    template_name = 'django_futils/municipality_detail.html'


##############
# List views #
##############
# Person.
class AbstractPersonAddressListView(BasePermissions, generic.ListView):
    template_name = 'django_futils/personaddress_list.html'
    extra_context_key = 'person'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.filter(person=self.kwargs['pk'])
        return get_list_or_404(queryset)

    def get_context_data(self, **kwargs):
        r"""Pass the person object."""
        context = super().get_context_data(**kwargs)
        context[self.extra_context_key] = self.context_model.objects.get(id=self.kwargs['pk'])
        print(context)
        return context


class AbstractPersonTelephoneListView(BasePermissions, generic.ListView):
    template_name = 'django_futils/persontelephone_list.html'
    extra_context_key = 'person'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.filter(person=self.kwargs['pk'])
        return get_list_or_404(queryset)

    def get_context_data(self, **kwargs):
        r"""Pass the person object."""
        context = super().get_context_data(**kwargs)
        context[self.extra_context_key] = self.context_model.objects.get(id=self.kwargs['pk'])
        return context


class AbstractPersonEmailListView(BasePermissions, generic.ListView):
    template_name = 'django_futils/personemail_list.html'
    extra_context_key = 'person'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.filter(person=self.kwargs['pk'])
        return get_list_or_404(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.extra_context_key] = self.context_model.objects.get(id=self.kwargs['pk'])
        return context


# Company.
class AbstractCompanyAddressListView(BasePermissions, generic.ListView):
    template_name = 'django_futils/companyaddress_list.html'
    extra_context_key = 'company'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.filter(company=self.kwargs['pk'])
        return get_list_or_404(queryset)

    def get_context_data(self, **kwargs):
        r"""Pass the company object."""
        context = super().get_context_data(**kwargs)
        context[self.extra_context_key] = self.context_model.objects.get(id=self.kwargs['pk'])
        return context


class AbstractCompanyTelephoneListView(BasePermissions, generic.ListView):
    template_name = 'django_futils/companytelephone_list.html'
    extra_context_key = 'company'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.filter(company=self.kwargs['pk'])
        return get_list_or_404(queryset)

    def get_context_data(self, **kwargs):
        r"""Pass the company object."""
        context = super().get_context_data(**kwargs)
        context[self.extra_context_key] = self.context_model.objects.get(id=self.kwargs['pk'])
        return context


class AbstractCompanyEmailListView(BasePermissions, generic.ListView):
    template_name = 'django_futils/companyemail_list.html'
    extra_context_key = 'company'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.filter(company=self.kwargs['pk'])
        return get_list_or_404(queryset)

    def get_context_data(self, **kwargs):
        r"""Pass the company object."""
        context = super().get_context_data(**kwargs)
        context[self.extra_context_key] = self.context_model.objects.get(id=self.kwargs['pk'])
        return context
