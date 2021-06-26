Running
=======

Development
-----------

The first time you run django-futils you need to initialize the database:


::


    make docker.up.dev.debug.volume.init


To serve the app:


::


    make docker.up.dev.debug.volume.serve



Production
----------

The first time you run django-futils you need to initialize the database:


::


    make docker.up.prod.no-debug.no-volume.init


To serve the app:


::


    make docker.up.prod.no-debug.no-volume.serve


Tests
-----


To run the tests you need to build the image and initialize it, then:


::


    make docker.up.dev.debug.volume.test


Shell
-----

Development
```````````


::


    make docker.run.dev.debug.volume.shell


Production
``````````


::


    make docker.run.prod.no-debug.no-volume.shell



Docker makefile target structure
````````````````````````````````

Docker related make targets have this name format:


::


    docker.{build,up,down,run,rm}.{dev,prod}[.{debug,no-debug},{volume,no-volume}.{init,shell,serve}]
