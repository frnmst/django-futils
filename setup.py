#
# setup.py
#
# Copyright (C) 2017-2020 frnmst (Franco Masotti) <franco.masotti@live.com>
#
# This file is part of django-futils.
#
# django-futils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django-futils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django-futils.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages

setup(
    name='django_futils',
    version='3.0.0',
    include_package_data=True,
    packages=find_packages(exclude=['*tests*']),
    license='GPL',
    description='A set of models, an admin and utilities for frequently used patterns.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    author='Franco Masotti',
    author_email='franco.masotti@live.com',
    keywords='django utilities',
    url='https://blog.franco.net.eu.org/software/#django-futils',
    python_requires='>=3.9, <4',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
    ],
    install_requires=[
        'Django>=3.2,<3.3',
        'requests>=2.25,<2.26',
        'uwsgi>=2.0,<2.1',
        'django-countries>=7.2,<7.3',
        'django-phone-field>=1.8,<1.9',
        'django-vies>=6.0,<6.1',
        'django-simple-history>=3.0,<3.1',
        'django-cleanup>=5.2,<5.3',
        'django-import-export>=2.5,<2.6',
        'psycopg2-binary>=2.9,<2.10',
        'django-extensions>=3.1,<3.2',
        'django-leaflet>=0.28,<0.29',
        'django-htmlmin>=0.11,<0.12',
        'geopy>=2.1,<2.2',
    ],
)
