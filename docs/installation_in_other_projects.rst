Installation of django-futils in other projects
===============================================

To import django-futils into your
project you need to install it and add it to the ``INSTALLED_APPS``
variable among other apps in the settings file. See below:


::


    INSTALLED_APPS = [
       ...,
       'django_futils.apps.DjangoFutilsConfig',
       'simple_history',
       'vies',
       'phone_field',
       'leaflet',
       'import_export',
       ...
    ]


You can run these commands in a Dockerfile. ``${VERSION}`` corresponds to a git tag or branch
such as ``0.0.3``.


::


    RUN pip3 install git+https://software.franco.net.eu.org/frnmst/django-futils.git@${VERSION}

    # Include translations for django-futils.
    RUN mkdir /code/django/django_futils && cp -aR /code/.local/lib/python*/site-packages/django_futils/locale /code/django/django_futils/. && chown -R django:django /code/django/django_futils


Django templates of django-futils included apps are not loaded automatically.
You need to install them manually in your app. This is an example of an
extract of a Pipfile:


::


    # Models.
    django-phone-field = "~=1.8"
    django-vies = "~=6.0"
    ## Model history.
    django-simple-history = "~=3.0"
    ## Remove dangling files.
    django-import-export = "~=2.5"


Models, admin, views, etc...
----------------------------

These files contain the concrete classes and data that you
can use in other projects. You just need to copy the files and change
the import paths:

- ``./django_futils/default_models.py``
- ``./django_futils/default_admin.py``
- ``./django_futils/views.py``

For example, instead of:


::


    from . import abstract_views as DFU_abstract_views


use:


::


    import django_futils.abstract_views as DFU_abstract_views


In case of ``./django_futils/set_defaults.py`` just add this to the imports:


::


    from django_futils import set_defaults


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
