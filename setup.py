import os
import sys
import subprocess
from setuptools import setup, find_packages
from pkg_resources import resource_filename
confdir = resource_filename(__name__, "samples/moon")

setup(
    name='Moon',
    version='0.1.0',
    packages=find_packages(),
    author='DThom',
    author_email="thomas.duval@orange.com",
    url="http://www.github.com/waitwaitwait/moon",
    license='Apache License, Version 2.0',
    long_description=open('README.md').read(),
    test_suite="tests",
    package_dir={'moon': '../'},
    install_requires=['django_openstack_auth', 'python-keystoneclient', 'python-novaclient', 'pymongo'],
)

if sys.argv[1] == "install" and os.name == "posix":
    print("Copying {} to /etc".format(confdir))
    import shutil
    shutil.copytree(confdir, "/etc")
    print("Adding user 'moon'")
    subprocess.call("adduser --no-create-home --system  --disabled-password --disabled-login moon", shell=True)
    print("Populating MySQL database")
    import getpass
    root_password = getpass.getpass("MySQL password for user root ?")
    moon_password = "P4ssw0rd"
    while True:
        moon_password = getpass.getpass("MySQL password for user moon ?")
        moon_password_tmp = getpass.getpass("Again please")
        if moon_password == moon_password_tmp:
            break
    subprocess.call("""mysql -uroot -p$MySQLPASSWD <<EOF
create database user_db;
create user moonuser identified by '{password}';
grant all privileges on user_db.* to 'moonuser'@'localhost' identified by "{password}" with grant option;
create database moon;
grant all privileges on moon.* to 'moonuser'@'localhost' identified by "{password}" with grant option;
EOF""".format(password=moon_password), shell=True)
    print("Configuring logs")
    try:
        os.mkdir("/var/log/moon/")
    except OSError:
        pass
    except IOError:
        pass
    subprocess.call("chown -R moon /var/log/moon/", shell=True)
    subprocess.call("""cat <<EOF > /etc/logrotate.d/moon
/var/log/moon/*.db {
       daily
       rotate 10
       copytruncate
       delaycompress
       compress
       notifempty
       missingok
}
EOF""", shell=True)
