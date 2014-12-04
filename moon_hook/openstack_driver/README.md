Hook for Moon authorization framework
=====================================

How to create the Python package
--------------------------------

Go in the source directory:

    python setup.py sdist


How to install it
----------------
Go to your Keystone server and put and modify in the file `/etc/keystone/keystone-paste.ini` the following lines:

    [filter:moon]
    moon_server_ip = <ip of moon server>
    moon_server_port = 8080
    moon_server_password = P4ssw0rd
    paste.filter_factory = moon.keystone_hook:filter_factory
    ...
    [pipeline:public_api]
    pipeline = access_log sizelimit url_normalize token_auth admin_token_auth moon xml_body json_body ec2_extension user_crud_extension public_service

    [pipeline:admin_api]
    pipeline = access_log sizelimit url_normalize token_auth admin_token_auth moon xml_body json_body ec2_extension s3_extension crud_extension admin_service

    [pipeline:api_v3]
    pipeline = access_log sizelimit url_normalize token_auth admin_token_auth moon xml_body json_body ec2_extension s3_extension service_v3
    ...

Go to your Nova server(s) and put and modify in the file `/etc/nova/api-paste.ini` the following lines:

    #############
    # OpenStack #
    #############
    ...
    [composite:openstack_compute_api_v2]
    use = call:nova.api.auth:pipeline_factory
    noauth = compute_req_id faultwrap sizelimit noauth moon ratelimit osapi_compute_app_v2
    keystone = compute_req_id faultwrap sizelimit authtoken keystonecontext moon ratelimit osapi_compute_app_v2
    keystone_nolimit = compute_req_id faultwrap sizelimit authtoken keystonecontext moon osapi_compute_app_v2

    [composite:openstack_compute_api_v3]
    use = call:nova.api.auth:pipeline_factory_v3
    noauth = moon request_id faultwrap sizelimit noauth_v3 osapi_compute_app_v3
    keystone = moon request_id faultwrap sizelimit authtoken keystonecontext osapi_compute_app_v3

    [filter:moon]
    moon_server_ip = <ip of moon server>
    moon_server_port = 8080
    moon_server_password = P4ssw0rd
    paste.filter_factory = moon.nova_hook:filter_factory


Copy the moon package on this server and decompress it and install it:

    scp Moon....tar.gz openstackserver:/tmp
    ssh openstackserver
    cd /tmp
    tar xvfz Moon....tar.gz
    cd Moon...
    sudo python setup.py install

You must restart some OpenStack services (Keystone and Nova-api). Depending on your configuration, you can use:

    screen -x stack
    ...

or:

    sudo service nova-api restart
    sudo service apache restart
