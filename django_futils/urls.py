#
# urls.py
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

from django.contrib import admin
from django.urls import path, re_path, reverse_lazy, include
# See https://overiq.com/django-1-10/handling-media-files-in-django/
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from .default_admin import admin_site
from . import views

# See https://stackoverflow.com/a/55723121
urlpatterns = [
    path('admin/', admin_site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('admin:index'))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

################
# Detail views #
################
# Type views.
urlpatterns += [
    path('data/addresstype/<int:pk>/', views.AddressTypeDetailView.as_view(), name=settings.reverse_urls['AddressTypeDetailView']),
    path('data/telephonetype/<int:pk>/', views.TelephoneTypeDetailView.as_view(), name=settings.reverse_urls['TelephoneTypeDetailView']),
    path('data/emailtype/<int:pk>/', views.EmailTypeDetailView.as_view(), name=settings.reverse_urls['EmailTypeDetailView']),
    path('data/attachmenttype/<int:pk>/', views.AttachmentTypeDetailView.as_view(), name=settings.reverse_urls['AttachmentTypeDetailView']),
]
# Normal views.
urlpatterns += [
    path('data/person/<int:pk>/', views.PersonDetailView.as_view(), name=settings.reverse_urls['PersonDetailView']),
    path('data/personaddress/<int:pk>/', views.PersonAddressDetailView.as_view(), name=settings.reverse_urls['PersonAddressDetailView']),
    path('data/persontelephone/<int:pk>/', views.PersonTelephoneDetailView.as_view(), name=settings.reverse_urls['PersonTelephoneDetailView']),
    path('data/personemail/<int:pk>/', views.PersonEmailDetailView.as_view(), name=settings.reverse_urls['PersonEmailDetailView']),
    path('data/personattachment/<int:pk>/', views.PersonAttachmentDetailView.as_view(), name=settings.reverse_urls['PersonAttachmentDetailView']),

    path('data/company/<int:pk>/', views.CompanyDetailView.as_view(), name=settings.reverse_urls['CompanyDetailView']),
    path('data/companyaddress/<int:pk>/', views.CompanyAddressDetailView.as_view(), name=settings.reverse_urls['CompanyAddressDetailView']),
    path('data/companytelephone/<int:pk>/', views.CompanyTelephoneDetailView.as_view(), name=settings.reverse_urls['CompanyTelephoneDetailView']),
    path('data/companyemail/<int:pk>/', views.CompanyEmailDetailView.as_view(), name=settings.reverse_urls['CompanyEmailDetailView']),

    path('data/municipality/<int:pk>/', views.MunicipalityDetailView.as_view(), name=settings.reverse_urls['MunicipalityDetailView']),
]

##############
# List views #
##############
urlpatterns += [
    path('data/personaddress/person/<int:pk>/', views.PersonAddressListView.as_view(), name=settings.reverse_urls['PersonAddressListView']),
    path('data/persontelephone/person/<int:pk>/', views.PersonTelephoneListView.as_view(), name=settings.reverse_urls['PersonTelephoneListView']),
    path('data/personemail/person/<int:pk>/', views.PersonEmailListView.as_view(), name=settings.reverse_urls['PersonEmailListView']),

    path('data/companyaddress/company/<int:pk>/', views.CompanyAddressListView.as_view(), name=settings.reverse_urls['CompanyAddressListView']),
    path('data/companytelephone/company/<int:pk>/', views.CompanyTelephoneListView.as_view(), name=settings.reverse_urls['CompanyTelephoneListView']),
    path('data/companyemail/company/<int:pk>/', views.CompanyEmailListView.as_view(), name=settings.reverse_urls['CompanyEmailListView']),
]
