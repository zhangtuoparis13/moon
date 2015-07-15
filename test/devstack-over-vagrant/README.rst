Environnement de test Devstack
==============================

Pré-requis
----------
- Une connexion Internet fonctionnelle vers les dépôts APT Ubuntu & le cloud Hashicorp (https://atlas.hashicorp.com),
- Oracle Virtualbox (https://www.virtualbox.org/),
- Vagrant (https://www.vagrantup.com/),
- un client SSH.

Présentation:
-------------
Ce programme cherche a récupérer, installer et configurer automatiquement un environement Devstack au sein d'une machine virtuelle virtualbox.

Plus précisément, le script réalise les étapes suivantes:

- récupération d'une VM sous Ubuntu Trustry Tahr Server depuis les dépots d'hashicorp,

- configuration du support du proxy dans la VM pour APT et pour le script d'installation,

- mise à jour des index des dépots APT,

- mise à jour des paquets du système,

- installation du gestionnaire de version GIT,

- configuration du support du proxy par ce dernier,

- récupération de DevStack,

- patch de ce dernier pour utiliser le protocole HTTPS et non GIT,

- configuration de DevStack,

- lancement de DevStack.


Ce programme est composé de trois fichiers:

- le fichier ``VagrantFile`` indiquant:

	+ la VM de base est à utiliser,

	+ la configuration personnalisée à lui appliquer,

	+ le script de provisionning à amorcer;

- le script de ``devstack.provision.sh`` servant à installer les dépendances de DevStack dans la VM conçue, à l'installer, à le configurer et à l'amorcer,

-le fichier local.conf.default, qui permet de définir des options de configuration supplémentaire dans le fichier local.conf employé.

Configuration:
--------------

Avant d'amorcer la construction de la VM et son provisionning, il est nécéssaire de configurer quelques variables internes au script ``devstack.provision.sh``

Proxy
~~~~~

================== =================
Paramètres         Descriptions
================== =================
http_proxy         Définit l'URL du proxy pour les connexions HTTP
https_proxy        Définit l'URL du proxy pour les connexions HTTPS
ftp_proxy          Définit l'URL du proxy pour les connexions FTP 
no_proxy           Definit les hôtes ne nécéssitant pas de connexion par proxy
APT_CONF           Définit le chemin vers le fichier de configuration d'APT génrant les connexions par proxy.
================== =================

Source et destination de Devstack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

================== =================
Paramètres         Descriptions
================== =================
BRANCH             Branch de devstack à cloner (master|sable/kilo|stable/juno| etc.)
URL_DEVSTACK       URL du dépot GIT DevStack à utiliser
REP_REPO_DEVSTACK  Répertoire de destination où doit-être cloné DevStack
================== =================

Paramètres DevStack
~~~~~~~~~~~~~~~~~~~

================== =================
Paramètres         Descriptions
================== =================
DEVSTACK_USER      Utilisateur allant exécuter l'exécutable Devstack. Il ne doit pas s'agir d'un super-utilisateur.
FIXED_RANGE        Plage IP des réseaux virtuels des instances d'Openstack (en notation I.P.V.4/Masque)
NETWORK_GATEWAY    Adresse de passerelle vers le réseaux exterieur dans le réseau virtuel
LOGDAY             Durée, en jours, durant laquelles les journaux d'OpenStack sont gardés
LOGDIR             Répertoire des fichiers journaux d'OpenStack
LOGFILE            Chemin du fichier journal principal de d'OpenStack
ADMIN_PASSWORD     Mots de passes des comptes admin et demo de l'installation d'OpenStack.
DATABASE_PASSWORD  Mot de passe de l'utilisateur OpenStack en base de donnée
RABBIT_PASSWORD    Mot de passe de l'utilisateur OpenStack du broker RabbitMQ
SERVICE_PASSWORD   Mot de passe des services OpenStack, utilisé avec KeyStone 
SERVICE_TOKEN      Token utilisé après l'authentification des services avec KeyStone
CONF_FILE          Emplacement du fichier de configuration à configurer
STACK_USER         Utilisateur sous lequel OpenStack sera exécuté
================== =================

Amorçage
--------

Après avoir configuré le script, la configuration et l'amorçage de l'environnement de test se fait grace à la commande suivante:

``$ vagrant up``
