django-futils
=============

A set of models, an admin and utilities for frequently used patterns.

Description
-----------

This repository contains a fully functional Django app which is importable
in another Django project or standalone. To import django-futils into your
project add it to your ``INSTALLED_APPS`` in the settings file.


::


    INSTALLED_APPS = [
       ...,
       'django_futils',
       ...
    ]


Abstract models contain all the necessary variables, attributes and methods,
except foreign keys which are implemented in the concrete models: concrete
models inherit everything from the abstract models. You can use these concrete
models directly or override them. The admin part follows this same philosophy.

Primary objects are instances with the ``is_primary`` attribute set to ``True``.
Usually these objects are not deletable because they are used to keep data
integrity. For example a person must have at least one address and telephone
number and if you want to delete the address, or the telephone number
you must delete the whole person. If you have multiple addresses you can change
the primary address and then execute a deletion.

Documentation
-------------

See the documentation in ``./docs``

License
-------

Copyright (C) 2020 frnmst (Franco Masotti) <franco.masotti@live.com>

django-futils is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

django-futils is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with django-futils.  If not, see <http://www.gnu.org/licenses/>.

Trusted source
--------------

You can check the authenticity of new releases using my public key.

Instructions, sources and keys can be found at `frnmst.gitlab.io/software <https://frnmst.gitlab.io/software/>`_.
