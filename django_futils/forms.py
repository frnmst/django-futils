#
# forms.py
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

from .models import CompanyAddress
from django import forms
from dal import autocomplete

# See
# https://django-autocomplete-light.readthedocs.io/en/master/tutorial.html?highlight=data-minimum-input-length#passing-options-to-select2
# https://select2.org/configuration/options-api
# for options


class CompanyAddressForm(forms.ModelForm):
    class Meta:
        model = CompanyAddress
        fields = ('__all__')
        widgets = {
            'company': autocomplete.ModelSelect2(url='company-fk-autocomplete'),
        }
