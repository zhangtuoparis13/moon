#!/usr/bin/env python


# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from setuptools import setup, find_packages

PROJECT = 'moonwebview'

VERSION = '0.1'

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Python Moon Web View',
    long_description=long_description,

    author='Thomas Duval',
    author_email='thomas.duval@orange.com',

    url='https://github.com/...',
    download_url='https://github.com/.../tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Intended Audience :: Developers',
                 'Environment :: Web',
                 ],

    platforms=['Any'],

    install_requires=['Django', 'django_compressor', 'django_openstack_auth'],

    packages=find_packages(),
    include_package_data=True,

    zip_safe=False,
)