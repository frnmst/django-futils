django-futils
=============

|buymeacoffee|

.. |buymeacoffee| image:: assets/buy_me_a_coffee.svg
                   :alt: Buy me a coffee
                   :target: https://buymeacoff.ee/frnmst

A set of models, an admin and utilities for frequently used patterns.

Description
-----------

This repository contains a fully functional Django app which is importable
in another Django project or standalone. To import django-futils into your
project you need to install it and add it to the ``INSTALLED_APPS``
variable (among other apps) in the settings file. See below:


::


    INSTALLED_APPS = [
       ...,
       'django_futils.apps.DjangoFutilsConfig',
       'simple_history',
       'vies',
       'phone_field',
       'leaflet',
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

https://docs.franco.net.eu.org/django-futils/

License
-------

Copyright (C) 2020-2021 frnmst (Franco Masotti) <franco.masotti@live.com>

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

Instructions, sources and keys can be found at `blog.franco.net.eu.org/software <https://blog.franco.net.eu.org/software/>`_.

Crypto donations
----------------

- Bitcoin: bc1qnkflazapw3hjupawj0lm39dh9xt88s7zal5mwu
- Dogecoin: DMB5h2GhHiTNW7EcmDnqkYpKs6Da2wK3zP
- Vertcoin: vtc1qd8n3jvkd2vwrr6cpejkd9wavp4ld6xfu9hkhh0
