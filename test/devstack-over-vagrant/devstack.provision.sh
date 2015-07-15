#!/bin/bash

# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

# Ce  script cherche à provisionner une machine Ubuntu Trusty avec une installation de Devstack.
# Les étapes réalisées par ce script sont les suivantes:
# 	* Configuration du support du proxy par la VM par APT et le script d'installation
#	* MAJ des index des dépots APT
#	* MAJ des paquets du système
#	* Installation du SCM GIT
#	* Configuration du support du proxy par ce dernier
#	* Récupération de DevStack
#	* Patch de ce dernier pour utiliser le protocole HTTPS et non GIT
#	* Configuration de DevStack
#	* Lancement de DevStack
# Ce présent script a été testé sur Ubuntu Trusty, avec une configuration dèrrière un serveur Proxy


############################ Configuration du script #############################################
## Proxy
	## Info : Diverses variables sur le proxy
http_proxy=
https_proxy=
ftp_proxy=
no_proxy=localhost,127.0.0.0/8,::1
	## Configuration du proxy dans APT
APT_CONF=/etc/apt/apt.conf.d/20-proxy.conf
	## Utilisateur allant executer Devstack
DEVSTACK_USER=vagrant
	## Branche de devstack à utiliser (master|stable/kilo|stable/juno etc.)
BRANCH=stable/kilo

## Devstack SRC
	# Url d'où GIT doit cloner le dépot devstack
URL_DEVSTACK=https://github.com/openstack-dev/devstack.git
	# Repertoire ou dépot devstack doit être cloné
REP_REPO_DEVSTACK=~vagrant/devstack/

## Configuration de Devstack
FIXED_RANGE=10.254.1.0/24
NETWORK_GATEWAY=10.254.1.1
LOGDAY=1
LOGDIR=\$DEST/logs
LOGFILE=\$LOGDIR/stack.sh.log
ADMIN_PASSWORD=mokJomRyxIjagDogCafVishec
DATABASE_PASSWORD=huJautBoyzfucomFicuvTagRo
RABBIT_PASSWORD=wohodofNavfogJiercisGujEe
SERVICE_PASSWORD=amenhoucterkajOsawquavdis
SERVICE_TOKEN=9f2d78d4-e679-b158-9ab7-4d2e01613d7b
STACK_USER=vagrant
CONF_FILE=~vagrant/devstack/local.conf
################################ Fin de la configuration ########################################

echo ====================== Début du provisonnement de devstack ========================
echo 
echo == Application de la configuration du proxy

#Si on a déclarer un proxy qqpart, alors, on supprime le fichier de configuration du proxy
if [ "$http_proxy" != "" ] ||  [ "$https_proxy" != "" ] || [ "$ftp_proxy" != "" ] ; then 
	echo 	\* Suppression de la configuration pré-existante
	rm -f APT_CONF
fi

# Application de la configuration du proxy à APT
if [ "$http_proxy" != "" ]; then
	echo 	\* Configuration APT - Proxy HTTP : $http_proxy 
	echo Acquire::http::proxy \"$http_proxy\"\; >> $APT_CONF
fi

if [ "$https_proxy" != "" ]; then
	echo 	\* Configuration APT - Proxy HTTPS : $https_proxy
	echo Acquire::https::proxy \"$https_proxy\"\; >> $APT_CONF
fi

if [ "$ftp_proxy" != "" ]; then
	echo 	\* Configuration APT - Proxy FTP : $ftp_proxy
	echo Acquire::ftp::proxy \"$ftp_proxy\"\; >> $APT_CONF
fi

echo == Mise à jour de APT
echo 	\*  Mise à jour des dépots
apt-get update -y

echo 	\* Mise à jour du système
apt-get dist-upgrade -y

echo == Installation de git
echo 	\* Installation du paquetage
apt-get install -y git

# Application de la configuration du proxy à GIT
if [ "$http_proxy" != "" ]; then
	echo 	\* Configuration GIT - Proxy HTTP : $http_proxy 
	git config --global http.proxy $http_proxy
fi

if [ "$https_proxy" != "" ]; then
	echo 	\* Configuration GIT - Proxy HTTPS : $https_proxy
	git config --global https.proxy $https_proxy
fi

if [ "$ftp_proxy" != "" ]; then
	echo 	\* Configuration GIT - Proxy FTP : $ftp_proxy
	git config --global ftp.proxy $ftp_proxy
fi

# Clonage du dépot devstack
echo == Récupération de Devstack
echo 	\* Création répertoire : $REP_REPO_DEVSTACK
rm -rf $REP_REPO_DEVSTACK
mkdir $REP_REPO_DEVSTACK
cd $REPO_REPO_DEVSTACK
echo	\* Clonage dépot : $URL_DEVSTACK
git clone -b $BRANCH $URL_DEVSTACK $REP_REPO_DEVSTACK 

# configuration devstack
echo == Configuration de l\'environement de Devstack - local.conf
echo 	\* Rentre dans $REP_REPO_DEVSTACK
cd $REP_REPO_DEVSTACK 
echo 	\* Création fichier
cp /vagrant/local.conf.default $CONF_FILE
#echo [[local\|localrc]] > $CONF_FILE
for i in FIXED_RANGE NETWORK_GATEWAY LOGDAY LOGDIR LOGFILE ADMIN_PASSWORD DATABASE_PASSWORD RABBIT_PASSWORD SERVICE_PASSWORD SERVICE_TOKEN STACK_USER; do
	echo $i=$(eval "echo \$$(echo $i)") >> $CONF_FILE
	echo 	\* Configuration de $i=$(eval "echo \$$(echo $i)") 
done

# Path pour eviter l'usge de git
echo == Patch de stackrc pour bannir l\'usage du protocol git
sed s/git:\\/\\/git.openstack.org/https:\\/\\/git.openstack.org/g stackrc > stackrc.new
mv stackrc stackrc.old
cp stackrc.new stackrc

echo == Lancement de devstack
#Rectification des droits pour laisser Devstack accessible à l'utilisateur Vagrant
echo 	\* Rectification des droits du depot cloné de devstack ...
chown -R vagrant:vagrant  $REP_REPO_DEVSTACK

#Launching devstack...
echo 	\* Lancement de devstack en tant que Vagrant

# Some explications:
# - We use sudo tu impersonate the executaion of stack.sh
# - "-n" force sudo not to be interactive
# - sudo has one major drawback: it won't transfer the current execution environment to the launched program. That's why we call bash, set up environment variable and, then, execute .stack.sh
# - export no_proxy=\$(hostname -I | sed \"s/ /,/g\")$no_proxy is a trick to define $no_proxy in the new execution context, and add all IP Adress of all interface in the $no_proxy variable, to prevent bugs with the keystone's configuration of each OpenStack module.
sudo -n -u $DEVSTACK_USER bash -c "eval \"export USER=$DEVSTACK_USER && export HOME=~$DEVSTACK_USER && export http_proxy=$http_proxy && export https_proxy=$https_proxy && export ftp_proxy=$ftp_proxy && export no_proxy=\$(hostname -I | sed \"s/ /,/g\")$no_proxy && cd $REP_REPO_DEVSTACK && ./stack.sh \""
