Hook for Moon authorization framework
=====================================

Howto install it
----------------
Go to your Keystone server and put and modify in the file `/etc/keystone/keystone-api.ini` the following lines:

    [filter:moon]
    paste.filter_factory = keystone.contrib.moon:Moon.factory
    ...
    [pipeline:public_api]
    pipeline = access_log sizelimit url_normalize token_auth admin_token_auth moon xml_body json_body ec2_extension user_crud_extension public_service

    [pipeline:admin_api]
    pipeline = access_log sizelimit url_normalize token_auth admin_token_auth moon xml_body json_body ec2_extension s3_extension crud_extension admin_service

    [pipeline:api_v3]
    pipeline = access_log sizelimit url_normalize token_auth admin_token_auth moon xml_body json_body ec2_extension s3_extension service_v3
    ...

If you use a `Devstack` environment, go in the directory `/opt/stack/keystone/keystone/contrib/moon/`.
If you use an Icehouse environment, go in the directory `/usr/lib/python2.7/dist-packages/keystone/contrib/moon/`.
Copy those files in it:
- __init__.py
- moon_hook.py
- keystone_sync.py

Create a directory `/etc/moon` and copie in it the file `api.json`.

Endly modify the file `moon_hook.py` the dictionary MOON_SERVER_IP to map to your infrastructure:

    MOON_SERVER_IP = {
        "HOST": "<ip address of moon server>",
        "PORT": "8080",
        "BASEURL": "mrm"
    }

