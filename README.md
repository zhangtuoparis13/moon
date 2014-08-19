Moon
====

This is an authorization module for OpenStack

How to install it
----------------
Download the code and install the Keystone hook on your Keystone server see [openstack_driver].

- Install Vagrant [http://www.vagrantup.com/] in your system and start it:

    vagrant up

- Go in your new server:

    vagrant ssh

- Configure `settings.py` and `openrc` (see [samples/moon/openrc]).
- In a terminal, source the `openrc` file (`source openrc`) and sync the moon server:

    python ./moon_server.py --sync

- After that, you can start the moon server:

    python ./moon_server.py --run runserver 0.0.0.0:8080

- You can also drop the database used by moon with:

    python ./moon_server.py --dbdrop
