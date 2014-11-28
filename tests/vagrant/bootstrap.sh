#!/usr/bin/env bash

MySQLPASSWD="nomoresecrete"
OPENSTACK_SERVER="<set an IP here>"

#if necessary, set a proxy
#export http_proxy="http://login:pass@proxy:3128";
#export https_proxy="http://login:pass@proxy:3128";
#export no_proxy="127.0.0.1"

apt-get update
#if you need other language
#apt-get install -y language-pack-fr
#export LANGUAGE=fr_FR
#export LANG=fr_FR.UTF-8
#export LC_ALL=fr_FR.UTF-8
#locale-gen fr_FR.UTF-8
#dpkg-reconfigure locales

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
    nodejs \
    git \
    npm

#apt-get install swi-prolog
#cd /tmp
#wget https://code.google.com/p/pyswip/downloads/detail?name=pyswip-0.2.3.tar.gz -O pyswip-0.2.3.tar.gz
#tar xvfz pyswip-0.2.3.tar.gz
#cd pyswip-0.2.3/
#python setup.py install

pip install django_openstack_auth
pip install python-keystoneclient
pip install python-novaclient
pip install pymongo
pip install oslo.config

# installing dependencies for gui
update-alternatives --install /usr/bin/node node  /usr/bin/nodejs 20
npm config set registry="http://registry.npmjs.org/"
npm config set strict-ssl false
npm config set https-proxy ${http_proxy}
npm config set proxy ${https_proxy}
npm install bower -g
echo you must install all javascript librairies with 
echo cd /moon/gui/
echo bower install

#Hack to simplify the installation and development process
ln -s /moon/ /usr/local/lib/python2.7/dist-packages/moon
ln -s /moon/samples/moon /etc/moon

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

echo -e "\n$OPENSTACK_SERVER openstackserver" >> /etc/hosts

echo Before running the server you must execute :
echo python -m moon.moon_server --run "syncdb"

