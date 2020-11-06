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

from .default_models import Municipality, PersonTelephone, CompanyTelephone, PersonEmail, CompanyEmail, PersonAddress, CompanyAddress, PersonAttachment, Person, Company
from django import forms
from dal import autocomplete

# See
# https://django-autocomplete-light.readthedocs.io/en/master/tutorial.html?highlight=data-minimum-input-length#passing-options-to-select2
# https://select2.org/configuration/options-api
# for options


class PersonAddressForm(forms.ModelForm):
    class Meta:
        model = PersonAddress
        fields = ('__all__')
        widgets = {
            'type': autocomplete.ModelSelect2(url='addresstype-fk-autocomplete'),
            'municipality': autocomplete.ModelSelect2(url='municipality-fk-autocomplete'),
            'person': autocomplete.ModelSelect2(url='person-fk-autocomplete'),
        }


class PersonTelephoneForm(forms.ModelForm):
    class Meta:
        model = PersonTelephone
        fields = ('__all__')
        widgets = {
            'type': autocomplete.ModelSelect2(url='telephonetype-fk-autocomplete'),
            'person': autocomplete.ModelSelect2(url='person-fk-autocomplete'),
        }


class PersonEmailForm(forms.ModelForm):
    class Meta:
        model = PersonEmail
        fields = ('__all__')
        widgets = {
            'type': autocomplete.ModelSelect2(url='emailtype-fk-autocomplete'),
            'person': autocomplete.ModelSelect2(url='person-fk-autocomplete'),
        }


class PersonAttachmentForm(forms.ModelForm):
    class Meta:
        model = PersonAttachment
        fields = ('__all__')
        widgets = {
            'type': autocomplete.ModelSelect2(url='attachmenttype-fk-autocomplete'),
            'person': autocomplete.ModelSelect2(url='person-fk-autocomplete'),
        }


class CompanyAddressForm(forms.ModelForm):
    class Meta:
        model = CompanyAddress
        fields = ('__all__')
        widgets = {
            'type': autocomplete.ModelSelect2(url='addresstype-fk-autocomplete'),
            'municipality': autocomplete.ModelSelect2(url='municipality-fk-autocomplete'),
            'company': autocomplete.ModelSelect2(url='company-fk-autocomplete'),
        }


class CompanyTelephoneForm(forms.ModelForm):
    class Meta:
        model = CompanyTelephone
        fields = ('__all__')
        widgets = {
            'type': autocomplete.ModelSelect2(url='telephonetype-fk-autocomplete'),
            'company': autocomplete.ModelSelect2(url='company-fk-autocomplete'),
        }


class CompanyEmailForm(forms.ModelForm):
    class Meta:
        model = CompanyEmail
        fields = ('__all__')
        widgets = {
            'type': autocomplete.ModelSelect2(url='emailtype-fk-autocomplete'),
            'company': autocomplete.ModelSelect2(url='company-fk-autocomplete'),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('__all__')
        widgets = {
            'person': autocomplete.ModelSelect2(url='person-fk-autocomplete'),
        }
