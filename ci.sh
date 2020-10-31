#!/usr/bin/env bash
#
# ci.sh
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

# Run a build in a fully clean environment using anonymous (non-mounted) volumes.
# Run this script like this:
# env --ignore-environment ENV="development" PATH=$PATH bash --noprofile --norc -c './ci.sh'
# or
# env --ignore-environment ENV="production" PATH=$PATH bash --noprofile --norc -c './ci.sh'

# WARNING: this script replaces the SECRET_SETTINGS.py file!

set -euo pipefail

[ -n "${ENV}" ]

CP=$(which cp)
CURL=$(which curl)
PYTHON3=$(which python3)
DOCKER_COMPOSE=$(which docker-compose)
MAKE=$(which make)

export BASE_CI_DIR=""$(pwd)"/ci"
export PYENV_HOME=""${BASE_CI_DIR}"/python_env"
export PIPENV_CACHE_DIR=""${BASE_CI_DIR}"/pipenv_cache"
export WORKON_HOME=""${BASE_CI_DIR}"/pipenv_venv_home"
export PIP_DOWNLOAD_CACHE=""${BASE_CI_DIR}"/pip_download_cache"
export PIP_CACHE_DIR=""${BASE_CI_DIR}"/pip_cache"

rm -rf "${BASE_CI_DIR}"
rm -rf requirements.txt

export SAVED_PATH=${PATH}
export PATH=.

${CP} SECRET_SETTINGS.dist.py SECRET_SETTINGS.py
${CP} env.dist .env
${PYTHON3} -m venv --clear --without-pip "${PYENV_HOME}"
source "${PYENV_HOME}"/bin/activate
${CURL} https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
pip3 install pipenv

pipenv lock --requirements > requirements.txt
if [ "${ENV}" = 'development' ]; then
    pipenv lock --requirements --dev >> requirements.txt
fi

if [ "${ENV}" = 'development' ]; then
    ${DOCKER_COMPOSE} build --force-rm --no-cache --memory=2GB --build-arg DJANGO_ENV=development

    # Do not enable named volumes and delete anonymous volumes when finished.
    ${DOCKER_COMPOSE} --file docker-compose.yml --file docker/docker-compose.debug.yml --file docker/docker-compose.init_dev.yml --file docker/docker-compose.db_name_dev.yml up --always-recreate-deps --renew-anon-volumes --abort-on-container-exit
else
    ${DOCKER_COMPOSE} build --force-rm --no-cache --memory=2GB --build-arg DJANGO_ENV=production

    # Do not enable named volumes and delete anonymous volumes when finished.
    ${DOCKER_COMPOSE} --file docker-compose.yml --file docker/docker-compose.no_debug.yml --file docker/docker-compose.init_prod.yml --file docker/docker-compose.db_name_prod.yml up --always-recreate-deps --renew-anon-volumes --abort-on-container-exit
fi

${DOCKER_COMPOSE} down --volumes