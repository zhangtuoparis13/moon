#!/bin/sh

MySQLPASSWD="P4ssw0rd"
OPENSTACK_SERVER="192.168.119.113"

apt-get update

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
    mongodb-server \
    libxslt1-dev \
    zlib1g-dev

pip install django_openstack_auth
pip install python-keystoneclient
pip install python-novaclient
pip install pymongo
pip install oslo.config

python setup.py install

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

