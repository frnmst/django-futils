#!/bin/bash
#
# build.sh
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

set -euo pipefail

DJANGO_ENV="${1}"

apt-get update

# | dependecy name      | purpose                                |
# | --------------------|----------------------------------------|
# | gettext             | translations                           |
# | graphviz            | database schema                        |
# | libgraphviz-dev     | database schema                        |
# | postgis             | postgres extension                     |
# | postgresql-client   | poll database availability with `psql` |

DEPENDENCIES_DEV='graphviz libgraphviz-dev postgis gettext postgresql-client'
DEPENDENCIES_PROD='postgis gettext postgresql-client'

if [ "${DJANGO_ENV}" = 'development' ]; then
    apt-get install -y --no-install-recommends ${DEPENDENCIES_DEV}
else
    apt-get install -y --no-install-recommends ${DEPENDENCIES_PROD}
fi

rm -rf /var/cache/apt
apt-get clean
