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

##########
# Common #
##########
remove-migrations:
	rm -rf $(APP_NAME)/migrations

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

clean:
	rm -rf build dist *.egg-info static __pycache__ requirements.txt locale/django.po
	$(COMMAND_PREFIX) $(MAKE) -C docs clean

.PHONY: default doc install uninstall install-dev uninstall-dev test clean
