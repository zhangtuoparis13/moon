=======================================
Moon's Development environment overview
=======================================

Context
=======

This paper is intended to introduced new contributors of the Moon project to the developpement environement already set up. We will introduced used tools as well as the files organisation.

Moon project attempts to provide a free software security module for the OpenStack suite. As it is curently in developpement, new contributors are welcome.

We will introduce the used tools and the current organisation of the project.

Used developpement tools
========================

In this section, we will describe the different tools used on each developpment workstation.

Vagrant & Virtualbox
--------------------

Vagrant:
^^^^^^^^

Vagrant is a provisionning tool for virtual machines. It defines their specificiations, builds the VM and execute user-defined provisionning scripts.  

This program takes as input a configuration file named ``Vagrantfile``, which defines all the specs of the VM to generate, and the provisionning script to execute in that VM.

With all these elements, Vagrant will:

#. import a barebone VM,

#. Configure a new VM according to the barebone and the Vagrantfile,

#. instanciate it,

#. execute the specified provisionning script inside the new VM.

Once all these steps are executed, the VM can be accessed through SSH, WinRM or the virtualization software’s GUI (disabled by default).

Oracle Virtualbox:
^^^^^^^^^^^^^^^^^^

Oracle Virtualbox is a virtualization solution developped by Oracle.  Even though Virtualbox is released on Open Source licence, some extensions like the *Extension pack* are closed-source.

Virtualbox provides two user interfaces:

-  a GUI written in Qt,

-  a CLI (VBoxManage).

Virtualbox is able to emulate storage disks and networks, to adjust the numbered of available CPU and the amount of available RAM to the guest OS.

As the CPU is not emulated, the guest architecture depends on the host one.

In the case of the Moon project, Virtualbox is never directly used. Actualy, Virtualbox is used as a backend of Vagrant (*Vagrant’s provider*).

Git version control system
--------------------------

In moon project, the used VCS is GIT.

Git attempts to be a a KISS (keep it simple and stupid) VCS focusing on reliability.

This solution was chosen because of it popularity among the developer community and because it corresponds to the OPNFV’s development stack.

Python 2.7
----------

Python is a famous scripting language, started in 1990, which can be used in a wide range of project type.

Nowdays, two branches of the projects are active:

-  *Python3.5:* The new branch of the software, implmenting new functionalities but is not fully compatible with Python2 scripts.

-  *Python2.7:* The old branch of python, aiming at reliability. Many Python packageis are supporting only this verison.

As Python 2.7 is used by most of the Openstack project, Moon is written to work with Python2.7 interpreter.

OPNFV JIRA
----------

Jira is a SaaS software allowing the management of development and bugtracking task in a project. This solution is edited by Atlassian.

OPNFV use this solution to manage their project. A user can access the software through the LinuxID SSO.

This solution was chosen for the moon project as it widely used by the other OpenStack projects.

Code location
=============

In this part of the document, we will describe the different codes Repositories used in the Moon project.

OPNFV Git repository
--------------------

The OPENFV repository is the official one for the moon project: each release of the project must be pulled from this repository.

Two important facts must be kept in mind will using this repository:

-  the authentification is based uppon the LinuxID’s SSO,

-  Each commit must be validated through a gerrit process before being
   integrated into the repository.

Consequently, this repository would better to be used for publishing code to the OpenStack communitity rather than developping intermediate version.

URL:
^^^^

https://git.opnfv.org/moon

Moon Github repository
----------------------

Github is the main development repository because of its popularity and because the rules for contributing are less strict. It is use as a Developpement repository whereas OPNFV repository is a publishing area.

Using Github repository implies creating a Github account for authentification, and to be added as a contributor (to get write access).

URL:
^^^^

`ssh://git@github.com:rebirthmonkey/moon.git <ssh://git@github.com:rebirthmonkey/moon.git>`__

Github VMSpace
--------------

VMSpace is not a repository for Moon code but a repository containing *Vagrantfiles* to contruct developpment, integration and qualification environnements.

This repository must be cloned at the beginning of the developpement.

The ``readme.md`` file explains how to use each folder of the VMspace respository.

URL:
^^^^

`ssh://git@github.com:rebirthmonkey/vmspace.git <ssh://git@github.com:rebirthmonkey/vmspace.git>`__

Moon-Devstack-Dev description
=============================

Moon-devstack-dev is the standard developpement environement for the Moon prject. In this part, we will explain the specs of the environement.

Barebone
--------

The VM is based uppon ``ubuntu/trusty64`` barebone. Indeed, the OpenStack plateform is known for working well on Ubuntu OS.  Consequently, we use the official vagrant image for the last Ubuntu LTS relase on 64 bits architecture.

VM Specifications
-----------------

The VM uses three custom setting:

-  the option ``IOAPIC`` is set to on, to allow the guest OS to get more than one CPU,

-  there are three CPU, to allow the developpement environement to run more than one VM,

-  there are 6072MB in RAM for the guest OS, to be sure the OpenStack suite will run fluently in the guest system.

Shared folders
--------------

Four folders are shared beetween the host OS and the guest OS:

-  ``../../opnfv-moon/keystone-moon/`` to ``/opt/stack/keystone-moon``: This folder contains the source code of the keystone-moon component.

-  ``../../opnfv-moon/moonclient/`` to ``/opt/stack/moonclient``: This folder provides to the guest OS the moonclient source code.

-  ``../../opnfv-moon/keystonemiddleware-moon/`` to ``/opt/stack/keystonemiddleware-moon``: this shared folder transmits the keystonemiddleware-moon source code to the guest OS.

-  ``../../github-moon/moonwebview/`` to ``/opt/stack/moonwebview``: this folder shares the moon web interface’s source code between the guest OS and the host OS.

.. image :: schema.jpg 


Sharing the source code between the guest OS and the host OS enables the developpers to edit its code from its IDE on the host system, and evaluate it in the guest system.

Port forwarding
---------------

There are three ports forwarding to the guest OS (without mentionning the SSH redirection): 

#. ``80`` from ``8073``: Access to the Horizon UI,

#. ``5000`` from ``8074``: Access to the Keystone-moon admin endpoint,

#. ``35357`` from ``8075``: Access to the Keystone-moon service endpoint.

Provisionning script
--------------------

After the creation of the VM, a provisionning script is run. It will commit the following tasks:

#. installs the prerequisite to the devstack environement,

#. launches the devstack’s installation script (it will set up an openstack instance and launch it),

#. incorporate Moon’s components into the devstack installation.

Once the provisionning script has completed, you should have a working development environement for moon.
