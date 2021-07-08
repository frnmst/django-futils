#
# abstract_views.py
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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


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


class AbstractAttachmentTypeDetailView(BasePermissions, generic.DetailView):
    template_name = 'django_futils/attachmenttype_detail.html'


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
    paginate_by = 10


class AbstractPersonTelephoneListView(BasePermissions, generic.ListView):
    template_name = 'django_futils/persontelephone_list.html'
    paginate_by = 10


class AbstractPersonEmailListView(BasePermissions, generic.ListView):
    template_name = 'django_futils/personemail_list.html'
    paginate_by = 10


# Company.
class AbstractCompanyAddressListView(BasePermissions, generic.ListView):
    template_name = 'django_futils/companyaddress_list.html'
    paginate_by = 10


class AbstractCompanyTelephoneListView(BasePermissions, generic.ListView):
    template_name = 'django_futils/companytelephone_list.html'
    paginate_by = 10


class AbstractCompanyEmailListView(BasePermissions, generic.ListView):
    template_name = 'django_futils/companyemail_list.html'
    paginate_by = 10
