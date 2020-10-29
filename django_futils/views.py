#
# views.py
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

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from dal import autocomplete
from .models import Company

################
# Autocomplete #
################

################
# Foreign keys #


class CompanyFKAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Company.objects.none()

        qs = Company.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
