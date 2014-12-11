import os
import sys
from setuptools import setup, find_packages
from pkg_resources import resource_filename

# In order to make the sdist, we have to delete os.link
# from http://bugs.python.org/issue8876#msg208792
del os.link

# In python < 2.7.4, a lazy loading of package `pbr` will break
# setuptools if some other modules registered functions in `atexit`.
# solution from: http://bugs.python.org/issue15881#msg170215
try:
    import multiprocessing # noqa
except ImportError:
    pass


confdir = resource_filename(__name__, "moon_server/samples/moon")

setup(
    setup_requires=['pbr'],
    pbr=True
)

if sys.argv[1] == "install" and os.name == "posix":
    if not os.path.isfile("/usr/bin/mysql"):
        print("MySQL must be installed, please run "
              "'apt-get install mysql-server mysql-client mongodb-server python-pip python-dev libmysqlclient-dev' "
              "before installing Moon...")
        print("\033[31mMoon unconfigured...\033[m")
        sys.exit(1)
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
        print("Error while copying configuration files... Maybe they are already there...")
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
