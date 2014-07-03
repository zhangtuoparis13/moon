#!/usr/bin/env bash

MySQLPASSWD="P4ssw0rd"
ping -c 1 www-cache.aql.fr
if [ $? == 0 ] ; then
    export http_proxy="http://vis:visiteur@www-cache.aql.fr:3128";
    export https_proxy="http://vis:visiteur@www-cache.aql.fr:3128";
    echo Configuring proxy to $http_proxy;
fi

ping -c 1 proxy.rd.francetelecom.fr
if [ $? == 0 ] ; then
    export http_proxy="http://proxy.rd.francetelecom.fr:8080";
    export https_proxy="http://proxy.rd.francetelecom.fr:8080";
    echo Configuring proxy to $http_proxy;
fi

apt-get update
apt-get install -y language-pack-fr
export LANGUAGE=fr_FR
export LANG=fr_FR.UTF-8
export LC_ALL=fr_FR.UTF-8
locale-gen fr_FR.UTF-8
dpkg-reconfigure locales

echo "mysql-server-5.5 mysql-server/root_password password ${MySQLPASSWD}
mysql-server-5.5 mysql-server/root_password seen true
mysql-server-5.5 mysql-server/root_password_again password ${MySQLPASSWD}
mysql-server-5.5 mysql-server/root_password_again seen true
" | debconf-set-selections

apt-get install -y --force-yes \
    mysql-server \
    python-minimal \
    python-mysqldb \
    python-django \
    python-dev \
    python-pip \
    graphviz \
    python-sqlalchemy \
    python-pygraphviz \
    mongodb-server

pip install django_openstack_auth
pip install python-keystoneclient
pip install python-novaclient
pip install pymongo

ln -s /vagrant/ /usr/local/lib/python2.7/dist-packages/moon
ln -s /vagrant/samples/moon /etc/moon

mysql -uroot -p$MySQLPASSWD <<EOF
create database user_db;
create user moonuser identified by '$MySQLPASSWD';
grant all privileges on user_db.* to 'moonuser'@'localhost' identified by "$MySQLPASSWD" with grant option;
create database moon;
grant all privileges on moon.* to 'moonuser'@'localhost' identified by "$MySQLPASSWD" with grant option;
EOF

mkdir /var/log/moon/
chown -R vagrant /var/log/moon/

cat <<EOF > /etc/logrotate.d/moon
/var/log/moon/*.db {
       daily
       rotate 10
       copytruncate
       delaycompress
       compress
       notifempty
       missingok
}
EOF

echo -e "\n192.168.119.113 openstackserver" >> /etc/hosts

python /vagrant/moon_server.py --run "syncdb"
