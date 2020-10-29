Extras
======

Primary objects
---------------

Primary objects are instances with the ``is_primary`` attribute set to ``True``.
Usually these objects are not deletable because they are used to keep data
integrity. For example a person must have at least one address and telephone
number and if you want to delete the address, or the telephone number
you must delete the whole person. If you have multiple addresses you can change
the primary address and then execute a deletion.

Abstract models
---------------

TODO

Continuous integration
----------------------

The ``./ci.sh`` script is intendend to get reproducible build for development and production environments.

Select one of the two environments:

::

    env --ignore-environment ENV="development" PATH=$PATH bash --noprofile --norc -c './ci.sh'
    env --ignore-environment ENV="production" PATH=$PATH bash --noprofile --norc -c './ci.sh'

You can use `Jenkins <https://jenkins.io>`_ for these tasks.

.. warning: The ``SECRET_SETTINGS.py`` file is replaced by ``SECRET_SETTINGS.dist.py`` file once you run the script.

See also https://stackoverflow.com/a/49669361

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
