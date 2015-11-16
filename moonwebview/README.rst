Moon
====

This is an authorization module for OpenStack

How to install it
-----------------
Download the code and install the Keystone and Nova hooks on your OpenStack server see [moon_hook/README.rst].
Download the code and install the Moon framework see [moon_server/README.rst].

! First version

Install Vagrant [http://www.vagrantup.com/] in your system and start it:

    cd tests/vagrant/
    #Modify the bootstrap.sh to fit your needs (openstack server and proxy)
    vagrant up

Go in your new server and configure django:

    vagrant ssh
    python -m moonwebview.server.server --run syncdb

Edit configuration files in /etc/moon and specially tenants.json to fit your OpenStack server
Synchronize the moon server and the OpenStack server:

    python -m moonwebview.server.server --sync

After that, you can start the moon server:

    python -m moonwebview.server.server --run runserver 0.0.0.0:80

You can also drop the database used by moon with:

    python -m moonwebview.server.server --dbdrop

! Second version

Copy /opt/stack/moonwebview/etc/moonwebview.conf into /etc/apache2/sites-available
Link /etc/apache2/sites-available/moonwebview.conf to /etc/apache2/sites-enabled/moonwebview.conf
    sudo cp /opt/stack/moonwebview/etc/moonwebview.conf /etc/apache2/sites-available
    sudo ln -s /opt/stack/moonwebview/etc/moonwebview.conf /etc/apache2/sites-available

Install Moonwebview
    cd /opt/stack/moonwebview/
    sudo python setup.py develop

Restart Apache
    sudo service apache2 restart

Add the link moon.server to your /etc/hosts :
    vi /etc/hosts
    #    127.0.0.1 localhost moon.server

Go to your web browser: http://moon.server/