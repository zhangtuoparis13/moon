#!/usr/bin/env python
"""Initialization script

This script allows to populate Moon for a demonstration.
"""

import json
import httplib
from uuid import uuid4

MOON_SERVER_IP = {
    "HOST": "127.0.0.1",
    "PORT": "8080",
    "BASEURL": "",
    "URL": ""
}

CREDENTIALS = {
    "login": "admin",
    "password": "P4ssw0rd",
    "Cookie": "novy2h83p4oyz9ujckd361ua7fh9tl6d"
}


def get_url(url, post_data=None, delete_data=None, crsftoken=None, method="GET"):
    # MOON_SERVER_IP["URL"] = url
    # _url = "http://{HOST}:{PORT}".format(**MOON_SERVER_IP)
    conn = httplib.HTTPConnection(MOON_SERVER_IP["HOST"], MOON_SERVER_IP["PORT"])
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain",
        'Cookie': 'sessionid={}'.format(CREDENTIALS["Cookie"]),
    }
    if post_data:
        method = "POST"
        conn.request(method, url, json.dumps(post_data), headers=headers)
    elif delete_data:
        method = "DELETE"
        conn.request(method, url, json.dumps(delete_data), headers=headers)
    else:
        conn.request(method, url, headers=headers)
    resp = conn.getresponse()
    content = resp.read()
    conn.close()

    try:
        return json.loads(content)
    except ValueError:
        return str(content)


def init():
    new_vm = {
        "name": "MoonTestGUI-"+str(uuid4()),
        "image_name": "Cirros3.2",
        "flavor_name": "m1.nano"
    }
    images = map(lambda x: x["name"], get_url("/pip/images/")["images"])
    for _img in images:
        if "irros" in _img:
            new_vm["name"] = _img
    #Before doing anything we have add an extension and map it to a tenant
    policies = get_url("/json/intra-extensions/policies")
    my_policy = policies["policies"].keys()[0]
    print("my_policy", my_policy)
    new_ext = get_url("/json/intra-extension/", post_data={"policymodel": my_policy})
    new_ext_uuid = new_ext["intra_extensions"][-1]
    print("new_ext", new_ext)
    tenants = get_url("/pip/projects/")
    tenant_admin = None
    for tenant in tenants["projects"]:
        tenant_admin = tenant["uuid"]
        break
    mapping = get_url(
        "/json/super-extension/tenant/{}/intra_extension/{}".format(
            tenant_admin,
            new_ext_uuid),
        method="POST"
    )
    #Add a new server
    _data = get_url("/json/intra-extension/"+new_ext_uuid+"/object/", post_data={"object": new_vm})
    objects = get_url("/pip/projects/{}/objects/".format(tenant_admin))
    for obj in objects["objects"]:
        if obj["name"] == new_vm["name"]:
            new_vm["uuid"] = obj["uuid"]
    #Delete the previous server
    _data = get_url("/json/intra-extension/"+new_ext_uuid+"/object/"+new_vm["uuid"]+"/", method="DELETE")
    objects = get_url("/pip/projects/{}/objects/".format(tenant_admin))


def destroy():
    pass

if __name__ == "__main__":
    init()