#
# Dockerfile
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

FROM docker_debian_postgis_django as builder

# Pass the environment variable from the docker-compose file.
ARG DJANGO_ENV

# Unbuffered output.
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY ./Makefile ./manage.py ./SECRET_SETTINGS.py ./requirements.txt /code/
COPY ./docs/ /code/docs/
COPY ./django_futils /code/django_futils/
COPY --from=docker_debian_postgis_django /code/utils /code/utils

RUN pip3 install --no-cache-dir --requirement requirements.txt
