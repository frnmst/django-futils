Extras
======

Continuous integration
----------------------

See https://software.franco.net.eu.org/frnmst/docker-debian-postgis-django/src/branch/master#user-content-continuous-integration

Connecting to the database and creatings backups
------------------------------------------------

Connecting
``````````

By default connection to the database is enabled for localhost only. Use the following command
to connect

::


    psql --hostname=127.0.0.1 --port=3051 --username=postgres


Credentials are stored in the ``./docker-compose.yml`` file. Since we are connecting
on the same machine we do not have to setup transport encryption.

Creating database backups
`````````````````````````

Once you know you can connect to the database you can proceed doing backups.

Although you can make and restore PostgreSQL backups with its own
commands  such as ``pg_dump`` and ``pg_restore``, I prefer to use a system that handles regular
and encrypted snapshots easily.

Install these packages from your package manager:

+----------------------+---------------------+------------------+
| Name                 | Binaries            | Version          |
+======================+=====================+==================+
| Borg backup          | - borg              | 1.1.9            |
+----------------------+---------------------+------------------+
| PostgreSQL           | - pg_dump           | == 13.3          |
+----------------------+---------------------+------------------+

Install these packages from PyPI:

+----------------------+---------------------+------------------+
| Name                 | Binaries            | Version          |
+======================+=====================+==================+
| Borgmatic            | - borgmatic         | 1.5.15           |
+----------------------+---------------------+------------------+

Debian GNU/Linux 10
~~~~~~~~~~~~~~~~~~~

These commands will help having everything working on Debian GNU/Linux.
You need to install PpostgreSQL 13 from an external repository. See
https://www.postgresql.org/download/linux/debian/


::


    # echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main"
    # wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    # apt-get install borgbackup postgresql-client-13
    $ pip3 install --user borgmatic


Running borgmatic
~~~~~~~~~~~~~~~~~

You can make database backups using a
`specific feature of Borgmatic <https://torsion.org/borgmatic/docs/how-to/backup-your-databases/>`_

.. important:: In this example we will work locally and on the dev example only.
               You should change file and directory paths accordingly.

First of all go into the ``borgmatic`` directory and run the following commands as ``root``:

1. create a new encrypted repository

   ::


        borg init -e repokey /tmp/backups/django_futils/dev.borg


2. create a backup


   ::


        borgmatic --config borgmatic.docker_postgis_django_futils_dev.yaml.dist


3. list the archives and select one


   ::


        borgmatic --config borgmatic.docker_postgis_django_futils_dev.yaml.dist list


4. restore the database and the files


   ::


        borgmatic --config borgmatic.docker_postgis_django_futils_dev.yaml.dist restore --archive ${archive_name}


5. extract


    ::


        borgmatic --config borgmatic.docker_postgis_django_futils_dev.yaml.dist extract --archive ${archive_name} --destination ../ --path db/dev/data/attachments


Systemd unit files
~~~~~~~~~~~~~~~~~~

You can find sample systemd service and timer files here:

- https://projects.torsion.org/witten/borgmatic/raw/branch/master/sample/systemd/borgmatic.service
- https://projects.torsion.org/witten/borgmatic/raw/branch/master/sample/systemd/borgmatic.timer
