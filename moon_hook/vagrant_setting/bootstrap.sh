#!/bin/sh

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

PASSWD="nomoresecrete"

export DEBIAN_FRONTEND=noninteractive

#if necessary, set a proxy
#export http_proxy="http://login:pass@proxy:3128";
#export https_proxy="http://login:pass@proxy:3128";
#export no_proxy="127.0.0.1"


apt-get -y --force-yes install python-software-properties git
add-apt-repository cloud-archive:icehouse

apt-get update

apt-get install -q -y --force-yes language-pack-fr
export LANGUAGE=fr_FR
export LANG=fr_FR.UTF-8
export LC_ALL=fr_FR.UTF-8
locale-gen fr_FR.UTF-8
dpkg-reconfigure locales

apt-get -y --force-yes dist-upgrade
apt-get install python-setuptools

cd /
#Must be done outside Vagrant
#git clone https://github.com/openstack-dev/devstack.git
cd /devstack

cat <<EOF >local.conf
[[local|localrc]]
FLOATING_RANGE=192.168.1.224/27
FIXED_RANGE=192.168.34.0/24
FIXED_NETWORK_SIZE=256
FLAT_INTERFACE=eth0
ADMIN_PASSWORD=$PASSWD
MYSQL_PASSWORD=$PASSWD
RABBIT_PASSWORD=$PASSWD
SERVICE_PASSWORD=$PASSWD
EOF

echo "To install your python package, go on your vagrant server..."
echo "    cd /openstack_driver"
echo "    sudo python setup.py install"
echo ""
echo "You have to install manually Devstack:"
echo "    cd /devstack"
echo "    ./stack.sh"
echo "And then install Keystone and Nova hooks and restart Apache and Nova"
echo ""
echo "Enjoy!"
