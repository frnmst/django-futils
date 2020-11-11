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
    version='0.0.0',
    packages=find_packages(exclude=['*tests*']),
    license='GPL',
    description='A set of models, an admin and utilities for frequently used patterns.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    package_data={
        '': ['*.txt', '*.rst'],
    },
    author='Franco Masotti',
    author_email='franco.masotti@live.com',
    keywords='django',
    url='https://github.com/frnmst/django-futils',
    python_requires='>=3.8, <4',
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 3.1',
    ],
    install_requires=[
        'Django>=3.1,<3.2',
        'requests>=2.24,<2.25',
        'django-countries>=6.1,<6.2',
        'django-phone-field>=1.8,<1.9',
        'django-vies>=5.0,<5.1',
        'django-simple-history>=2.12,<2.13',
        'django-cleanup>=5.1,<5.2',
        'psycopg2-binary>=2.8,<2.9',
        'django-extensions>=3.0,<3.1',
    ],
)
