Moon
====

This is an authorization module for OpenStack

How to install it
----------------
Download the code and install the Keystone and Nova hooks on your OpenStack server see [openstack_driver].

- Install Vagrant [http://www.vagrantup.com/] in your system and start it:

    cd tests/vagrant/
    vagrant up

- Go in your new server and configure django:

    vagrant ssh
    python -m moon.moon_server --run syncdb

- Edit configuration files in /etc/moon and specially tenants.json to fit your OpenStack server
- Synchronize the moon server and the OpenStack server:

    python -m moon.moon_server --sync

- After that, you can start the moon server:

    python -m moon.moon_server --run runserver 0.0.0.0:8080

- You can also drop the database used by moon with:

    python -m moon.moon_server --dbdrop
