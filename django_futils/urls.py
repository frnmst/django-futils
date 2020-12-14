#
# urls.py
#
# Copyright (C) 2020 frnmst (Franco Masotti) <franco.masotti@live.com>
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

# Detail views.
urlpatterns += [
    path('data/person/<int:pk>/', views.PersonView.as_view(), name='person'),
    path('data/personaddress/<int:pk>/', views.PersonAddressView.as_view(), name='personaddress'),
    path('data/persontelephone/<int:pk>/', views.PersonTelephoneView.as_view(), name='persontelephone'),
    path('data/personemail/<int:pk>/', views.PersonEmailView.as_view(), name='personemail'),
    path('data/municipality/<int:pk>/', views.MunicipalityView.as_view(), name='municipality'),
    path('data/company/<int:pk>/',
         views.CompanyView.as_view(),
         name='company'),
]
# Type views.
urlpatterns += [
    path('data/addresstype/<int:pk>/', views.AddressTypeView.as_view(), name='addresstype'),
    path('data/telephonetype/<int:pk>/', views.TelephoneTypeView.as_view(), name='telephonetype'),
]

# List views.
urlpatterns += [
    path('data/personaddress/person/<int:pk>/', views.PersonAddressListView.as_view(), name='personaddress-list'),
]
