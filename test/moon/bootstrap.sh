#!/bin/sh

# ``bootstrap.sh`` is a shell script to automate the installation of a DevStack platform
# connected to a moon platform.
# usage:
#     bootstrap.sh <http_proxy_url>

# author: Thomas Duval
# mail: thomas.duval@orange.com
# version: 0.1 - 08282015

IP=192.168.33.20
PROXY=$1

if [ -f Vagrantfile ]; then
    VAGRANT=Vagrantfile
else
    VAGRANT=/vagrant/Vagrantfile
fi

IP=$(grep "config.vm.network :private_network" $VAGRANT | cut -d "\"" -f 2)

echo -e "IP is set to \033[7m$IP\033[m, ok ? (crtl-c to cancel)"

read answer

export http_proxy=$PROXY
export https_proxy=$PROXY
export no_proxy="127.0.0.1,$IP"

sudo -E apt-get update
sudo -E apt-get -y install git
git clone https://git.openstack.org/openstack-dev/devstack
cd devstack/
cp /vagrant/local.conf .
./stack.sh 

# Backup original keystone directory
mv /opt/stack/keystone /opt/stack/keystone-orig
ln -s /opt/stack/keystone-moon /opt/stack/keystone 

# Modify /etc/keystone/keystone-paste.ini
mv /etc/keystone/keystone-paste.ini /etc/keystone/keystone-paste.ini.bak
cp /etc/keystone/keystone-paste.ini.bak /tmp/_k0
sed '/pipeline = / s/json_body /json_body moon /' /tmp/_k0 > /tmp/_k1
sed '2 s/$/\n[filter:moon]\npaste.filter_factory = keystone.contrib.moon.routers:Admin.factory\n/' /tmp/_k1 > /tmp/_k2
cp /tmp/_k2 /etc/keystone/keystone-paste.ini

rm -f /tmp/_k*

# Modify /etc/keystone/keystone.conf
cat <<EOF >> /etc/keystone/keystone.conf

[moon]

# Authorisation backend driver. (string value)
authz_driver = keystone.contrib.moon.backends.flat.SuperExtensionConnector

# Moon Log driver. (string value)
log_driver = keystone.contrib.moon.backends.flat.LogConnector

# IntraExtension backend driver. (string value)
intraextension_driver = keystone.contrib.moon.backends.sql.IntraExtensionConnector

# Tenant backend driver. (string value)
tenant_driver = keystone.contrib.moon.backends.sql.TenantConnector

# Local directory where all policies are stored. (string value)
policy_directory = /etc/keystone/policies

# Local directory where SuperExtension configuration is stored. (string value)
root_policy_directory = /etc/keystone/policies/policy_root

EOF

# Link Moon configuration in etc to the directory in /opt/stack/keystone-moon
ln -s /opt/stack/keystone-moon/examples/moon/policies /etc/keystone/policies

# db_sync
cd /opt/stack/keystone-moon/
./bin/keystone-manage db_sync --extension moon

cd -

# TODO: install keystonemiddleware
# TODO: configure keystonemiddleware / nova / swift
# TODO: install moonclient
# TODO: configure moonclient
# TODO: install moonwebview
# TODO: configure moonwebview

# Restart Apache
sudo service apache2 restart

