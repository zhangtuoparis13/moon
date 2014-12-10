import os
import sys
from setuptools import setup, find_packages
from pkg_resources import resource_filename

confdir = resource_filename(__name__, "moon_server/samples/moon")

setup(
    name='Moon_server',
    version='0.1.0',
    packages=find_packages(),
    author='DThom',
    author_email="thomas.duval@orange.com",
    url="https://github.com/rebirthmonkey/moon",
    license='Apache License, Version 2.0',
    long_description=open('README.md').read(),
    # test_suite="tests",
    package_dir={'moon': './'},
    install_requires=['django_openstack_auth', 'python-keystoneclient', 'python-novaclient', 'pymongo'],
)

if sys.argv[1] == "install" and os.name == "posix":
    print("Copying {} to /etc".format(confdir))
    import shutil
    import subprocess
    # try:
    #     os.mkdir("/etc/moon")
    # except OSError:
    #     pass
    # except IOError:
    #     pass
    # print(os.getcwd())
    try:
        shutil.copytree(confdir, "/etc/moon")
    except OSError:
        pass
    # except IOError:
    #     shutil.copy(os.path.join(os.getcwd(), confdir, "api.json"), "/etc/moon/")
    # except OSError:
    #     shutil.copy(os.path.join(os.getcwd(), confdir, "api.json"), "/etc/moon/")
    print("Adding user 'moon'")
    subprocess.call("adduser --no-create-home --system  --disabled-password --disabled-login moon", shell=True)
    print("Populating MySQL database")
    import getpass
    root_password = getpass.getpass("MySQL password for user root ?")
    moon_password = "P4ssw0rd"
    while True:
        moon_password = getpass.getpass("MySQL password for user moonuser ?")
        moon_password_tmp = getpass.getpass("Again please")
        if moon_password == moon_password_tmp:
            break
    subprocess.call("""mysql -uroot -p{mysql_password} <<EOF
create database IF NOT EXISTS user_db;
create user moonuser identified by '{password}';
grant all privileges on user_db.* to 'moonuser'@'localhost' identified by "{password}" with grant option;
create database moon;
grant all privileges on moon.* to 'moonuser'@'localhost' identified by "{password}" with grant option;
EOF""".format(password=moon_password, mysql_password=root_password), shell=True)
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
