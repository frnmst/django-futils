Extras
======

Translations
------------

Add this to the settings file of your project that uses django-futils.


::


    # Copy the locale files of django-futils.
    import shutil
    import django_futils
    DJANGO_FUTILS_LOCALE_DIR_SUFFIX = 'django_futils/locale'
    futils_path = os.path.dirname(django_futils.__file__)
    shutil.copytree(os.path.join(futils_path, 'locale'), os.path.join(BASE_DIR, DJANGO_FUTILS_LOCALE_DIR_SUFFIX), dirs_exist_ok=True)

    LOCALE_PATHS.append(os.path.join(BASE_DIR, DJANGO_FUTILS_LOCALE_DIR_SUFFIX))


.. important:: Don't forget to add ``/django_futils/`` to ``.gitignore``.

Continuous integration
----------------------

See https://github.com/frnmst/docker-debian-postgis-django/tree/master#continuous-integration

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

Borgmatic
~~~~~~~~~

Install `Borgmatic <https://torsion.org/borgmatic/>`_

You can make database backups using a
`specific feature of Borgmatic <https://torsion.org/borgmatic/docs/how-to/backup-your-databases/>`_

.. important:: In this example we will work locally. You should change file and directory paths
               accordingly.

First of all go into the ``borgmatic`` directory and run the following commands as ``root``:

1. create a new repository

   ::


        borg init -e repokey /tmp/test.borg


2. create a backup


   ::


        borgmatic --config borgmatic.docker_postgres_django_futils.dist.yaml


3. list the archives and select one


   ::


        borgmatic --config borgmatic.docker_postgres_django_futils.dist.yaml list


4. restore the database and the files


   ::


        borgmatic --config borgmatic.docker_postgres_django_futils.dist.yaml restore --archive ${archive_name}
        borgmatic --config borgmatic.docker_postgis_django_futils_dev.dist.yaml extract --archive ${archive_name} --destination ../ --path db/dev/data/attachments


Systemd unit files
~~~~~~~~~~~~~~~~~~

You can find sample systemd service and timer files here:

- https://projects.torsion.org/witten/borgmatic/raw/branch/master/sample/systemd/borgmatic.service
- https://projects.torsion.org/witten/borgmatic/raw/branch/master/sample/systemd/borgmatic.timer

Database replication
--------------------

Replication of the database must be done at the database level, not by docker.
See:

- https://cloud.google.com/community/tutorials/setting-up-postgres-hot-standby
- https://stackoverflow.com/questions/60220907/high-availability-database-postgresql-with-docker-swarm
- https://www.opsdash.com/blog/postgresql-streaming-replication-howto.html
