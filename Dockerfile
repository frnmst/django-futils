#
# Dockerfile
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

FROM docker_debian_postgis_django as builder

# Pass the environment variable from the docker-compose file.
ARG DJANGO_ENV
# Pass the running user and group.
ARG UID
ARG GID

# Unbuffered output.
ENV PYTHONUNBUFFERED 1

COPY --chown=django:django ./requirements.txt /code/django/
USER django:django
# Executable path for python binaries.
ENV PATH "$PATH:/code/.local/bin"
RUN pip3 install --user --no-cache-dir --requirement /code/django/requirements.txt && rm /code/django/requirements.txt
USER root

COPY --chown=django:django ./Makefile ./manage.py ./SECRET_SETTINGS.py ./.env ./uwsgi.ini /code/django/
COPY --chown=django:django ./docs/ /code/django/docs/
COPY --chown=django:django ./django_futils /code/django/django_futils/
COPY --chown=django:django --from=docker_debian_postgis_django /code/django/utils /code/django/utils/

RUN mkdir /code/django/data && chown -R django:django /code/django/data && chmod 700 /code && chown django:django /code && chown django:django /code/django

# This is necessary to avoid the root user.
USER django:django

WORKDIR /code/django
