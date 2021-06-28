Installation
============

Distribution files
------------------

django-futils uses `dist` files for some configurations. These files end
with the `dist` suffix and are example files for configurations. What
you need to do is to copy them to new files without the `.dist` suffix and edit
them as you like:

- ``./SECRET_SETTINGS.py.dist``
- ``./env.dist``
- ``./docker/docker-compose.dev.yml.dist``
- ``./docker/docker-compose.prod.yml.dist``
- ``./docker/docker-compose.serve_dev.yml.dist``
- ``./docker/docker-compose.serve_prod.yml.dist``
- ``./docker/docker-compose.test_dev.yml.dist``

.. important:: Once everything is installed and working generate a new secret key and replace the once in the ``./SECRET_SETTINGS.py`` file. Run:


  ::


      pipenv run python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'



Makefile and uwsgi.ini
----------------------

Follow these instructions to download some required files:

-  https://software.franco.net.eu.org/frnmst/docker-debian-postgis-django/src/branch/master#other-files

Prerequsites
------------

Install these packages from your package manager or from PyPI:

+----------------------+---------------------+------------------+
| Name                 | Binaries            | Version          |
+======================+=====================+==================+
| GNU make             | - make              | 4.3              |
+----------------------+---------------------+------------------+
| Docker               | - docker            | >= 19.03.0       |
+----------------------+---------------------+------------------+
| docker-compose       | - docker-compose    | >= 1.25.5        |
+----------------------+---------------------+------------------+
| pipenv               | - pipenv            |                  |
+----------------------+---------------------+------------------+
| Python               | - python3           | 3.8              |
+----------------------+---------------------+------------------+
| Graphviz             |                     | 2.44.1           |
+----------------------+---------------------+------------------+

Debian GNU/Linux
````````````````

These commands will help having everything working, including
building the documentation on Debian GNU/Linux:


::


    # apt-get install libgdal-dev libgraphviz-dev graphviz
    $ pip3 install docker-compose graphviz
    $ make install-dev


Start and enable the Docker service


::


    # systemctl start docker
    # systemctl enable docker


A new user, ``postgis-docker``, needs to be created to run the app.
Moreover, all the needed directories must be created **before** running the app.

::


    # useradd -m -s /bin/bash -u 999 -U postgis-docker
    # mkdir -p /home/postgis-docker/django-futils/dev/data
    # mkdir -p ./db/dev/data
    # chown -R postgis-docker:postgis-docker /home/postgis-docker/django-futils
    # chown -R ${developer}:${developer_group} ./db/dev/data
    # chmod 700 -R /home/postgis-docker/django-futils
    # chmod 700 -R ./db

Finally, run ``make docker.build.dev`` or ``make docker.build.prod`` depending on what you have to do.

Default credentials and variables
---------------------------------

+---------------------------+---------------------+
| Description               | Value               |
+===========================+=====================+
| Django admin user         | ``admin``           |
+---------------------------+---------------------+
| Django admin password     | ``adminpassword``   |
+---------------------------+---------------------+
| Postgres user             | ``postgres``        |
+---------------------------+---------------------+
| Postgres password         | ``postgres``        |
+---------------------------+---------------------+

.. warning:: Change the django credentials immediately! The Django admin user is infact a superuser.

.. important:: You can change some of the docker-compose variables in the ``./.env`` file.
