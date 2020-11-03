#!/usr/bin/env make
#
# Makefile
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

export PACKAGE_NAME=django_futils
export APP_NAME=django_futils
export MODELS=models.py

# Detect a Docker environment.
export DOCKER_ENV_FILE=/.dockerenv
ifneq ("$(wildcard $(DOCKER_ENV_FILE))","")
    export COMMAND_PREFIX=
else
    export COMMAND_PREFIX=pipenv run
endif

default: doc

##########
# Docker #
##########
docker.rm:
    # Remove stopped containers.
	docker-compose rm --stop


# Development #
###############
## Build the image.
gen-requirements:
	. ${CURDIR}/.env; pipenv lock --requirements > requirements.txt
	. ${CURDIR}/.env; pipenv lock --requirements --dev >> requirements.txt

docker.build.dev: gen-requirements
	docker-compose build --build-arg DJANGO_ENV=development

## Initialization.
docker.up.dev.debug.no-volume.init:
	docker-compose --file docker-compose.yml --file docker/docker-compose.dev.yml --file docker/docker-compose.debug.yml --file docker/docker-compose.init_dev.yml --file docker/docker-compose.db_name_dev.yml up --abort-on-container-exit

docker.up.dev.debug.volume.init:
	docker-compose --file docker-compose.yml --file docker/docker-compose.dev.yml --file docker/docker-compose.debug.yml --file docker/docker-compose.init_dev.yml --file docker/docker-compose.code_volume.yml --file docker/docker-compose.db_name_dev.yml up --abort-on-container-exit

## Server.
docker.up.dev.debug.volume.serve:
	docker-compose --file docker-compose.yml --file docker/docker-compose.dev.yml --file docker/docker-compose.debug.yml --file docker/docker-compose.code_volume.yml --file docker/docker-compose.db_name_dev.yml --file docker/docker-compose.serve_dev.yml up

## Stop.
docker.down.dev.debug.volume:
	docker-compose --file docker-compose.yml --file docker/docker-compose.dev.yml --file docker/docker-compose.debug.yml --file docker/docker-compose.code_volume.yml --file docker/docker-compose.serve_dev.yml --file docker/docker-compose.db_name_dev.yml down

## Shell.
docker.run.dev.debug.no-volume.shell:
	docker-compose --file docker-compose.yml --file docker/docker-compose.dev.yml --file docker/docker-compose.debug.yml --file docker/docker-compose.db_name_dev.yml run web bash

docker.run.dev.debug.volume.shell:
	docker-compose --file docker-compose.yml --file docker/docker-compose.dev.yml --file docker/docker-compose.debug.yml --file docker/docker-compose.code_volume.yml --file docker/docker-compose.db_name_dev.yml run web bash

docker.up.dev.debug.volume.test:
	docker-compose --file docker-compose.yml --file docker/docker-compose.dev.yml --file docker/docker-compose.debug.yml --file docker/docker-compose.code_volume.yml --file docker/docker-compose.db_name_dev.yml --file docker/docker-compose.test_dev.yml up  --abort-on-container-exit

## Db only.
docker.up.dev.db:
	docker-compose --file docker-compose.yml --file docker/docker-compose.dev.yml --file docker/docker-compose.db_name_dev.yml up db

# Production #
##############
## Build the image.
docker.build.prod:
	pipenv lock --requirements > requirements.txt
	docker-compose build --build-arg DJANGO_ENV=production

## Initialization.
docker.up.prod.no-debug.no-volume.init:
	docker-compose --file docker-compose.yml --file docker/docker-compose.prod.yml --file docker/docker-compose.no_debug.yml --file docker/docker-compose.init_prod.yml --file docker/docker-compose.db_name_prod.yml up --abort-on-container-exit

## Server.
docker.up.prod.no-debug.no-volume.serve:
	docker-compose --file docker-compose.yml --file docker/docker-compose.prod.yml --file docker/docker-compose.no_debug.yml --file docker/docker-compose.serve_prod.yml --file docker/docker-compose.db_name_prod.yml up

## Stop.
docker.down.prod.no-debug.no-volume.serve:
	docker-compose --file docker-compose.yml --file docker/docker-compose.prod.yml --file docker/docker-compose.no_debug.yml --file docker/docker-compose.serve_prod.yml --file docker/docker-compose.db_name_prod.yml down

## Shell.
docker.run.prod.no-debug.no-volume.shell:
	docker-compose --file docker-compose.yml --file docker/docker-compose.prod.yml --file docker/docker-compose.no_debug.yml --file docker/docker-compose.db_name_prod.yml run web bash

## Db only.
docker.up.prod.db:
	docker-compose --file docker-compose.yml --file docker/docker-compose.prod.yml --file docker/docker-compose.db_name_prod.yml up db

######################
# Inside docker only #
######################
# Development.
docker.init.dev: remove-migrations migrations migrate collectstatic syncdb docker.gen-superuser.dev initialize-translations compile-translations test doc check

docker.gen-superuser.dev:
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')" | python3 manage.py shell

docker.serve.dev: serve-dev

# Production.
docker.init.prod: migrations migrate collectstatic syncdb docker.gen-superuser.dev initialize-translations compile-translations check

docker.serve.prod: serve-production

###################
# Bare metal only #
###################
install:
	pip3 install . --user

uninstall:
	pip3 uninstall $(PACKAGE_NAME)

install-dev:
	pipenv install --dev
	pipenv run pre-commit install

uninstall-dev:
	pipenv --rm

dist: # clean
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel
	pipenv run twine check dist/*

init: install-dev remove-migrations migrations migrate collectstatic gen-superuser syncdb initialize-translations compile-translations

##########
# Common #
##########
remove-migrations:
	rm -rf $(APP_NAME)/migrations

# Run
# $(COMMAND_PREFIX) python3 manage.py makemessages -l ${LANGUAGE_CODE}
# to create a po file.
initialize-translations:
	$(COMMAND_PREFIX) python3 manage.py makemessages --all

compile-translations:
	$(COMMAND_PREFIX) python3 manage.py compilemessages

example-data:
	$(COMMAND_PREFIX) python3 manage.py runscript example_data

test:
	$(COMMAND_PREFIX) python3 manage.py test --verbosity 3 --failfast --no-input

shell:
	$(COMMAND_PREFIX) python3 manage.py shell

dbschema:
	$(COMMAND_PREFIX) python3 manage.py graph_models --include-models $$(grep '^class' $(APP_NAME)/$(MODELS) | awk '{print $$2}' | cut -d '(' -f 1 | tr '\n' ',') --arrow-shape normal --pygraphviz -g -o  docs/dbschema.svg $(APP_NAME)

collectstatic:
	$(COMMAND_PREFIX) python3 manage.py collectstatic --no-input

syncdb:
	$(COMMAND_PREFIX) python3 manage.py migrate --run-syncdb

gen-superuser:
	$(COMMAND_PREFIX) python3 manage.py createsuperuser

init-doc:
	$(COMMAND_PREFIX) python3 sphinx-quickstart docs

doc: dbschema
	$(COMMAND_PREFIX) $(MAKE) -C docs html

migrations:
	$(COMMAND_PREFIX) python3 manage.py makemigrations $(APP_NAME)

migrate:
	$(COMMAND_PREFIX) python3 manage.py migrate

serve-dev:
	$(COMMAND_PREFIX) python3 manage.py runserver 0.0.0.0:3050

# TODO
# Docker
# serve-production:
#	DEBUG="False" uwsgi --chdir=${CURDIR} --module=$(PROJECT_NAME).wsgi:application --env DJANGO_SETTINGS_MODULE=$(PROJECT_NAME).settings --master --pidfile=/run/project-master.pid --processes=5 --harakiri=20 --max-requests=5000 --vacuum --http=0.0.0.0:3050 --check-static ${CURDIR}
serve-production:
	$(COMMAND_PREFIX) uwsgi --chdir=${CURDIR} --module=$(PROJECT_NAME).wsgi:application --env DJANGO_SETTINGS_MODULE=$(PROJECT_NAME).settings --master --pidfile=/tmp/project-master.pid --http=0.0.0.0:3050 --processes=5 --uid=1019 --gid=1019 --harakiri=20 --max-requests=5000 --vacuum --check-static ${CURDIR}

check:
	$(COMMAND_PREFIX) python3 manage.py check --fail-level INFO

clean:
	rm -rf build dist *.egg-info static __pycache__ requirements.txt locale/django.po requirements.txt
	$(COMMAND_PREFIX) $(MAKE) -C docs clean

.PHONY: default doc install uninstall install-dev uninstall-dev test clean
