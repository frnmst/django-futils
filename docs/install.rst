Installation
============

Secret settings file
--------------------
First of copy these files and then edit them if needed:

- copy ``./SECRET_SETTINGS.dist.py`` into ``./SECRET_SETTINGS.py``
- copy ``./env.dist`` into ``./.env``

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


PostgreSQL
``````````

To have permission to read the local PostgreSQL volume, run the following as ``root``:


::


    # groupadd -g 102 postgis-docker
    # usermod -aG postgis-docker ${your_user}

Docker
``````

Add your user to the ``docker`` group and then start and enable the Docker service


::


    # usermod -aG docker ${your_user}
    # systemctl start docker
    # systemctl enable docker

Run ``make docker.build.dev`` or ``make docker.build.prod`` depending on what you have to do.

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

.. important:: You can change some of the docker-compose variables in the `./.env` file.
