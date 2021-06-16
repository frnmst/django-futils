Installation
============

Secret settings file
--------------------

First of copy these files and then edit them if needed:

- copy ``./SECRET_SETTINGS.dist.py`` into ``./SECRET_SETTINGS.py``
- copy ``./env.dist`` into ``./.env``

.. important:: Generate a new secret key and replace the once in the ``./SECRET_SETTINGS.py`` file. Run:


  ::


      pipenv run python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'



Have a look at the bottom of ``./SECRET_SETTINGS.py``. You will see the database settings
both for Docker and to be able to run the the app on *bare metal*.
By default the Docker credential are enabled so . Change them if needed.

Makefile
--------

Follow these instructions to download the makefile:

- https://software.franco.net.eu.org/frnmst/docker-debian-postgis-django/src/branch/master#the-makefile

Installation in another project
-------------------------------

You can run this command, where ``${VERSION}`` corresponds to a git tag or branch,
such as ``0.0.3``.

::


    pip3 install git+https://software.franco.net.eu.org/frnmst/django-futils.git@${VERSION}


Bare metal
----------

Prerequsites
````````````

Install these packages from your package manager or from PyPI:

+----------------------+---------------------+------------------+
| Name                 | Binaries            | Version          |
+======================+=====================+==================+
| GNU make             | - make              | 4.3              |
+----------------------+---------------------+------------------+
| PostgreSQL           | - postgres          | 12.4             |
+----------------------+---------------------+------------------+
| Postgis              |                     | 3.0.2            |
+----------------------+---------------------+------------------+
| Graphviz             |                     | 2.44.1           |
+----------------------+---------------------+------------------+
| pipenv               | - pipenv            |                  |
+----------------------+---------------------+------------------+
| Python               | - python3           | 3.8              |
+----------------------+---------------------+------------------+

Debian GNU/Linux
~~~~~~~~~~~~~~~~


::


    # apt-get install libgraphviz-dev


PostgreSQL
``````````

Initialize PostgreSQL


::


    # This applies to the first start of PostgreSQL only
    initdb --locale=en_US.UTF-8 -E UTF8 -D /var/lib/postgres/data

    sudo -i -u postgres

    # We will call the newly created user ${DB_USER}
    createuser --interactive


Add the PostGIS extension to the template. From now on every new database,
including test databases, will have this extension enabled.


::


    psql template1
    CREATE EXTENSION postgis;
    exit


Create the database with the new user:


::


    createdb -O ${DB_USER} ${DB_NAME}


where the ``DB_USER`` and ``DB_NAME`` variables must be the same as the ones reported in ``./SECRET_SETTINGS.py``.

Initialization
``````````````

Run ``make init``


Docker
------

Prerequsites
````````````

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
~~~~~~~~~~~~~~~~


::


    # apt-get install libgraphviz-dev
    $ pip3 install docker-compose graphviz


Docker
``````

Start and enable the Docker service


::


    # systemctl start docker
    # systemctl enable docker


User
````

A new user, ``postgis-docker``, needs to be created to run the app.

::


    # useradd -m -s /bin/bash -u 999 -U postgis-docker
    # usermod -aG ${developer_group} postgis-docker
    # cd django-futils/..
    # chmod 770 django-futils
    # usermod -aG docker postgis-docker
    # sudo -i -u postgis-docker
    $ cd django-futils


Finally, run ``make docker.build.dev`` or ``make docker.build.prod`` depending on what you have to do.

Run ``# chown postgis-docker:postgis-docker ./db/dev/data`` if you have persmission problems when saving files.

Default credentials and variables
`````````````````````````````````

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
