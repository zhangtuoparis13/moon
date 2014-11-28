stack
=====

Modules to install
--------

    -   devstack:
    
    -   


once launches the vagrant VM
1: set the proxy for the ft intranet
	export http_proxy="http://proxy.rd.francetelecom.fr:8080"
	export https_proxy="http://proxy.rd.francetelecom.fr:8080"
	export no_proxy=localhost,127.0.0.1,10.0.2.15,10.193.107.236

2: change git protocole to https in stackrc
	GIT_BASE=${GIT_BASE:-git://git.openstack.org}

3: configure ip address in devstack/local.conf
	HOST_IP=10.193.107.236

