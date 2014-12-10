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
