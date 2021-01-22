#
# constants.py
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

############
# Settings #
############
FOREIGN_KEY_FIELDS_DEFAULT = 0
FOREIGN_KEY_FIELDS_RAW = 1
FOREIGN_KEY_FIELDS_AUTOCOMPLETE = 2

##########
# Models #
##########
NAME_LENGTH = 128
CODE_LENGTH = 16

EMAIL_MAX_LENGTH = 254
GENERIC_CHAR_FIELD_LENGTH = 128

#########
# Money #
MONEY_MAX_DIGITS = 19
MONEY_DECIMAL_PLACES = 4
MONEY_DEFAULT_CURRENCY = 'EUR'
