Running
=======

Bare metal
----------

Set the ``DEBUG`` and ``DJANGO_ENV`` environment variables.

+----------------+---------------------------------+--------------------+
| Variable       | Values                          | Default value      |
+================+=================================+====================+
| ``DEBUG``      | ``True``, ``False``             | ``True``           |
+----------------+---------------------------------+--------------------+
| ``DJANGO_ENV`` | ``development``, ``production`` | ``development``    |
+----------------+---------------------------------+--------------------+

You can set the variables like this:

::


    export DEBUG=True
    export DJANGO_ENV=development


Development
```````````


::

    make serve-dev


Production
``````````


::

    make serve-prod


Docker
------

You have various options to manage the containers. Have a look at the Makefile in the root directory.

Docker related make targets have this name format:


::


    docker.{build,up,down,run,rm}.{dev,prod}[.{debug,no-debug},{volume,no-volume}.{init,shell,serve}]



If you want to have a quick look run ``make docker.up.dev.debug.volume.serve``

Tests
`````

To run the tests you need to build the image and initialize it, then:


::


    make docker.up.dev.debug.volume.test
