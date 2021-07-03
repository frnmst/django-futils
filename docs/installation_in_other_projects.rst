Installation of django-futils in other projects
===============================================

You can run these commands in a Dockerfile. ``${VERSION}`` corresponds to a git tag or branch
such as ``0.0.3``.


::


    RUN pip3 install git+https://software.franco.net.eu.org/frnmst/django-futils.git@${VERSION}

    # Include translations for django-futils.
    RUN mkdir /code/django/django_futils && cp -aR /code/.local/lib/python*/site-packages/django_futils/locale /code/django/django_futils/. && chown -R django:django /code/django/django_futils
