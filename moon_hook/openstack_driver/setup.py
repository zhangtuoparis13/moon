# Copyright 2014 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys
import os
from setuptools import setup, find_packages
from pkg_resources import resource_filename

confdir = resource_filename(__name__, "conf/moon")

setup(
    name='Moon_hook',
    version='0.1.2',
    packages=find_packages(),
    author='DThom',
    author_email="thomas.duval@orange.com",
    url="https://github.com/rebirthmonkey/moon",
    license='Apache License, Version 2.0',
    long_description=open('README.md').read(),
    # test_suite="tests",
    package_dir={'openstack_driver': './'},
    # install_requires=['django_openstack_auth', 'python-keystoneclient', 'python-novaclient'],
)

if sys.argv[1] == "install" and os.name == "posix":
    print("Copying {} to /etc/moon".format(confdir))
    import shutil
    try:
        os.mkdir("/etc/moon")
    except OSError:
        pass
    except IOError:
        pass
    print(os.getcwd())
    try:
        shutil.copytree(confdir, "/etc/moon")
    except IOError:
        shutil.copy(os.path.join(os.getcwd(), confdir, "api.json"), "/etc/moon/")
    except OSError:
        shutil.copy(os.path.join(os.getcwd(), confdir, "api.json"), "/etc/moon/")
