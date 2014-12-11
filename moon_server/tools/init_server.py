#!/usr/bin/env python

# Copyright 2014 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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


class CreateException(BaseException):

    def __new__(self, m):
        self.message = m

    def __str__(self):
        return "\033[31m" + self.message + "\033[m"


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
        return {"error": str(content)}


def init_tenants():
    tenant_admin, tenant_dev, tenant_test = None, None, None
    tenants = get_url("/pip/projects/")["projects"]
    for _tenant in tenants:
        _t = get_url("/pip/projects/{}".format(_tenant))["projects"]
        if _t["name"] == "admin":
            tenant_admin = _tenant
        elif _t["name"] == "dev":
            tenant_dev = _tenant
        elif _t["name"] == "test":
            tenant_test = _tenant
    if not tenant_dev:
        print("\tCreating tenant dev...")
        tenant_dev = get_url(
            "/pip/projects/",
            post_data={
                "name": "dev",
                "description": "Tenant for developers",
                "enabled": True,
                "domain": "default"
            }
        )["projects"]
        if "uuid" not in tenant_dev and len(tenant_dev["uuid"]) == 0:
            raise CreateException("Tenant dev not created ({})".format(tenant_dev))
        tenant_dev["init"] = False
    if not tenant_test:
        print("\tCreating tenant dev...")
        tenant_test = get_url(
            "/pip/projects/",
            post_data={
                "name": "test",
                "description": "Tenant for testers",
                "enabled": True,
                "domain": "default"
            }
        )["projects"]
        if "uuid" not in tenant_test and len(tenant_test["uuid"]) == 0:
            raise CreateException("Tenant test not created ({})".format(tenant_test))
        tenant_test["init"] = False
    return tenant_admin, tenant_dev, tenant_test


def init_extensions(tenant_admin, tenant_dev, tenant_test):
    print("\033[32mExtension creation\033[m")
    policies = get_url("/json/intra-extensions/policies")
    ext1 = get_url(
        "/json/intra-extensions/",
        post_data={"policymodel": "rbac_conf", "name": "Intra_Extension Policy RBAC"}
    )["intra-extensions"]
    ext2 = get_url(
        "/json/intra-extensions/",
        post_data={"policymodel": "mls_conf", "name": "Intra_Extension Policy MSL"}
    )["intra-extensions"]
    if ext1["uuid"]:
        print("\tCreating {}: \033[33mOK\033[m".format("Intra_Extension Policy RBAC"))
    else:
        raise CreateException("\tCreating {}: \033[41mKO\033[m ({})".format("Intra_Extension Policy RBAC", ext1))
    if ext2["uuid"]:
        print("\tCreating {}: \033[33mOK\033[m".format("Intra_Extension Policy MSL"))
    else:
        raise CreateException("\tCreating {}: \033[41mKO\033[m ({})".format("Intra_Extension Policy MSL", ext2))

    print("\033[32mExtension mappings\033[m")
    mapping = get_url(
        "/json/super-extensions/",
        post_data={
            "tenant_uuid": tenant_dev["uuid"],
            "intra_extension_uuid": ext1
        }
    )
    print(mapping)
    mapping = get_url(
        "/json/super-extensions/",
        post_data={
            "tenant_uuid": tenant_test["uuid"],
            "intra_extension_uuid": ext2
        }
    )
    print(mapping)
    return ext1, ext2


def init_vms(tenant_admin, tenant_dev, tenant_test, ext1, ext2, new_vm_template):
    #Initialization of tenants if needed
    if not tenant_dev["init"]:
        print("\tCreation of VM in tenant dev")
        vm = dict(new_vm_template)
        vm["name"] = "VM-dev-1"
        _data = get_url("/json/intra-extension/"+ext1["uuid"]+"/object/", post_data={"object": vm})
        if _data["uuid"]:
            print("\tCreating {}: \033[33mOK\033[m".format(vm["name"]))
        else:
            raise CreateException("\tCreating {}: \033[41mKO\033[m ({})".format(vm["name"], _data))
        vm["name"] = "VM-dev-2"
        _data = get_url("/json/intra-extension/"+ext1["uuid"]+"/object/", post_data={"object": vm})
        if _data["uuid"]:
            print("\tCreating {}: \033[33mOK\033[m".format(vm["name"]))
        else:
            raise CreateException("\tCreating {}: \033[41mKO\033[m ({})".format(vm["name"], _data))
        vm["name"] = "VM-dev-3"
        _data = get_url("/json/intra-extension/"+ext1["uuid"]+"/object/", post_data={"object": vm})
        if _data["uuid"]:
            print("\tCreating {}: \033[33mOK\033[m".format(vm["name"]))
        else:
            raise CreateException("\tCreating {}: \033[41mKO\033[m ({})".format(vm["name"], _data))
    if not tenant_test["init"]:
        print("\tCreation of VM in tenant test")
        vm = dict(new_vm_template)
        vm["name"] = "VM-test-1"
        _data = get_url("/json/intra-extension/"+ext2["uuid"]+"/object/", post_data={"object": vm})
        if _data["uuid"]:
            print("\tCreating {}: \033[33mOK\033[m".format(vm["name"]))
        else:
            raise CreateException("\tCreating {}: \033[41mKO\033[m ({})".format(vm["name"], _data))
        vm["name"] = "VM-test-2"
        _data = get_url("/json/intra-extension/"+ext2["uuid"]+"/object/", post_data={"object": vm})
        if _data["uuid"]:
            print("\tCreating {}: \033[33mOK\033[m".format(vm["name"]))
        else:
            raise CreateException("\tCreating {}: \033[41mKO\033[m ({})".format(vm["name"], _data))
        vm["name"] = "VM-test-3"
        _data = get_url("/json/intra-extension/"+ext2["uuid"]+"/object/", post_data={"object": vm})
        if _data["uuid"]:
            print("\tCreating {}: \033[33mOK\033[m".format(vm["name"]))
        else:
            raise CreateException("\tCreating {}: \033[41mKO\033[m ({})".format(vm["name"], _data))


def check_users(tenant_admin, tenant_dev, tenant_test, ext1, ext2):
    _users_dev = get_url("/pip/projects/{}/subjects".format(tenant_dev["uuid"]))["subjects"]
    _users_test = get_url("/pip/projects/{}/subjects".format(tenant_test["uuid"]))["subjects"]
    users = {}
    if "alice" not in map(lambda x: x["name"], _users_dev):
        _u = get_url(
            "/json/intra-extension/{}/subjects".format(ext1["uuid"]),
            post_data={
                "name": "alice",
                'domain': "Default",
                'enabled': True,
                'project': "dev",
                'password': "alice",
                'description': "Alice user"
            }
        )["subjects"]
        if _u["uuid"]:
            print("\tCreating Alice: \033[33mOK\033[m")
            users["alice"] = dict(_u)
        else:
            raise CreateException("\tCreating Alice: \033[41mKO\033[m ({})".format(_u))
    if "bob" not in map(lambda x: x["name"], _users_dev):
        _u = get_url(
            "/json/intra-extension/{}/subjects".format(ext1["uuid"]),
            post_data={
                "name": "bob",
                'domain': "Default",
                'enabled': True,
                'project': "dev",
                'password': "bob",
                'description': "Bob user"
            }
        )["subjects"]
        if _u["uuid"]:
            print("\tCreating Bob: \033[33mOK\033[m")
            users["bob"] = dict(_u)
        else:
            raise CreateException("\tCreating Bob: \033[41mKO\033[m ({})".format(_u))
    if "carol" not in map(lambda x: x["name"], _users_dev):
        _u = get_url(
            "/json/intra-extension/{}/subjects".format(ext1["uuid"]),
            post_data={
                "name": "carol",
                'domain': "Default",
                'enabled': True,
                'project': "dev",
                'password': "carol",
                'description': "Carol user"
            }
        )["subjects"]
        if _u["uuid"]:
            print("\tCreating Carol: \033[33mOK\033[m")
            users["carol"] = dict(_u)
        else:
            raise CreateException("\tCreating Carol: \033[41mKO\033[m ({})".format(_u))
    if "dave" not in map(lambda x: x["name"], _users_test):
        _u = get_url(
            "/json/intra-extension/{}/subjects".format(ext2["uuid"]),
            post_data={
                "name": "dave",
                'domain': "Default",
                'enabled': True,
                'project': "test",
                'password': "dave",
                'description': "Dave user"
            }
        )["subjects"]
        if _u["uuid"]:
            print("\tCreating Dave: \033[33mOK\033[m")
            users["dave"] = dict(_u)
        else:
            raise CreateException("\tCreating Dave: \033[41mKO\033[m ({})".format(_u))
    if "eve" not in map(lambda x: x["name"], _users_test):
        _u = get_url(
            "/json/intra-extension/{}/subjects".format(ext2["uuid"]),
            post_data={
                "name": "eve",
                'domain': "Default",
                'enabled': True,
                'project': "test",
                'password': "eve",
                'description': "Eve user"
            }
        )["subjects"]
        if _u["uuid"]:
            print("\tCreating Eve: \033[33mOK\033[m")
            users["eve"] = dict(_u)
        else:
            raise CreateException("\tCreating Eve: \033[41mKO\033[m ({})".format(_u))
    return users


def add_user_assignments(tenant_admin, tenant_dev, tenant_test, ext1, ext2):
    #Get all users
    users = get_url("/pip/projects/{}/users")["users"]
    user_alice = None
    user_bob = None
    user_carol = None
    user_dave = None
    user_eve = None
    for _user in users:
        if _user["name"] == "alice":
            user_alice = _user
        elif _user["name"] == "bob":
            user_bob = _user
        elif _user["name"] == "carol":
            user_carol = _user
        elif _user["name"] == "dave":
            user_dave = _user
        elif _user["name"] == "eve":
            user_eve = _user
    #Get all roles
    roles = get_url("/pip/projects/{}/roles")["roles"]
    role_admin = None
    role_member = None
    for _role in roles:
        if _role["name"] == "admin":
            role_admin = _role
        if _role["name"] == "Member":
            role_member = _role

    assign = get_url(
        "/json/intra-extension/{}/subject_assignments".format(ext1["uuid"]),
        post_data={
            "subject_id": user_alice["uuid"],
            "category_id": "role",
            "value": role_admin["uuid"]
        }
    )["subject_assignments"]
    if assign and "uuid" in assign:
        print("\tAssignment for Alice created")
    else:
        raise CreateException("Error in Alice assignments creation ({})".format(assign))
    assign = get_url(
        "/json/intra-extension/{}/subject_assignments".format(ext1["uuid"]),
        post_data={
            "subject_id": user_bob["uuid"],
            "category_id": "role",
            "value": role_member["uuid"]
        }
    )["subject_assignments"]
    if assign and "uuid" in assign:
        print("\tAssignment for Bob created")
    else:
        raise CreateException("Error in Bob assignments creation ({})".format(assign))
    assign = get_url(
        "/json/intra-extension/{}/subject_assignments".format(ext1["uuid"]),
        post_data={
            "subject_id": user_carol["uuid"],
            "category_id": "role",
            "value": role_member["uuid"]
        }
    )["subject_assignments"]
    if assign and "uuid" in assign:
        print("\tAssignment for Carol created")
    else:
        raise CreateException("Error in Carol assignments creation ({})".format(assign))
    assign = get_url(
        "/json/intra-extension/{}/subject_assignments".format(ext2["uuid"]),
        post_data={
            "subject_id": user_dave["uuid"],
            "category_id": "role",
            "value": role_admin["uuid"]
        }
    )["subject_assignments"]
    if assign and "uuid" in assign:
        print("\tAssignment for Dave created")
    else:
        raise CreateException("Error in Dave assignments creation ({})".format(assign))
    assign = get_url(
        "/json/intra-extension/{}/subject_assignments".format(ext2["uuid"]),
        post_data={
            "subject_id": user_eve["uuid"],
            "category_id": "role",
            "value": role_member["uuid"]
        }
    )["subject_assignments"]
    if assign and "uuid" in assign:
        print("\tAssignment for Eve created")
    else:
        raise CreateException("Error in Eve assignments creation ({})".format(assign))


def add_object_assignments(tenant_admin, tenant_dev, tenant_test, ext1, ext2):
    objects_dev = get_url("/pip/projects/{}/objects".format(tenant_dev))["objects"]
    objects_test = get_url("/pip/projects/{}/objects".format(tenant_test))["objects"]

    for _obj in objects_dev:
        assign = get_url(
            "/json/intra-extension/{}/object_assignments".format(ext1["uuid"]),
            post_data={
                "object_id": _obj["uuid"],
                "category_id": "id",
                "value": _obj["uuid"]
            }
        )["object_assignments"]
        if assign and "uuid" in assign:
            print("\tAssignment for {}/{} created".format(_obj["name"], "id"))
        else:
            raise CreateException("Error in {} assignments creation ({})".format(_obj["name"], assign))
        assign = get_url(
            "/json/intra-extension/{}/object_assignments".format(ext1["uuid"]),
            post_data={
                "object_id": _obj["uuid"],
                "category_id": "action",
                "value": "read"
            }
        )["object_assignments"]
        if assign and "uuid" in assign:
            print("\tAssignment for {}/{} created".format(_obj["name"], "action.read"))
        else:
            raise CreateException("Error in {} assignments creation ({})".format(_obj["name"], assign))
        assign = get_url(
            "/json/intra-extension/{}/object_assignments".format(ext1["uuid"]),
            post_data={
                "object_id": _obj["uuid"],
                "category_id": "action",
                "value": "os-start"
            }
        )["object_assignments"]
        if assign and "uuid" in assign:
            print("\tAssignment for {}/{} created".format(_obj["name"], "action.os-start"))
        else:
            raise CreateException("Error in {} assignments creation ({})".format(_obj["name"], assign))
        assign = get_url(
            "/json/intra-extension/{}/object_assignments".format(ext1["uuid"]),
            post_data={
                "object_id": _obj["uuid"],
                "category_id": "action",
                "value": "os-stop"
            }
        )["object_assignments"]
        if assign and "uuid" in assign:
            print("\tAssignment for {}/{} created".format(_obj["name"], "action.os-stop"))
        else:
            raise CreateException("Error in {} assignments creation ({})".format(_obj["name"], assign))

    for _obj in objects_test:
        assign = get_url(
            "/json/intra-extension/{}/object_assignments".format(ext1["uuid"]),
            post_data={
                "object_id": _obj["uuid"],
                "category_id": "object_security_level",
                "value": "medium"
            }
        )["object_assignments"]
        if assign and "uuid" in assign:
            print("\tAssignment for {}/{} created".format(_obj["name"], "id"))
        else:
            raise CreateException("Error in {} assignments creation ({})".format(_obj["name"], assign))
        assign = get_url(
            "/json/intra-extension/{}/object_assignments".format(ext1["uuid"]),
            post_data={
                "object_id": _obj["uuid"],
                "category_id": "action",
                "value": "read"
            }
        )["object_assignments"]
        if assign and "uuid" in assign:
            print("\tAssignment for {}/{} created".format(_obj["name"], "action.read"))
        else:
            raise CreateException("Error in {} assignments creation ({})".format(_obj["name"], assign))
        assign = get_url(
            "/json/intra-extension/{}/object_assignments".format(ext1["uuid"]),
            post_data={
                "object_id": _obj["uuid"],
                "category_id": "action",
                "value": "os-start"
            }
        )["object_assignments"]
        if assign and "uuid" in assign:
            print("\tAssignment for {}/{} created".format(_obj["name"], "action.os-start"))
        else:
            raise CreateException("Error in {} assignments creation ({})".format(_obj["name"], assign))
        assign = get_url(
            "/json/intra-extension/{}/object_assignments".format(ext1["uuid"]),
            post_data={
                "object_id": _obj["uuid"],
                "category_id": "action",
                "value": "os-stop"
            }
        )["object_assignments"]
        if assign and "uuid" in assign:
            print("\tAssignment for {}/{} created".format(_obj["name"], "action.os-stop"))
        else:
            raise CreateException("Error in {} assignments creation ({})".format(_obj["name"], assign))


def add_rules(tenant_admin, tenant_dev, tenant_test, ext1, ext2):
    objects_dev = get_url("/pip/projects/{}/objects".format(tenant_dev))["objects"]
    objects_test = get_url("/pip/projects/{}/objects".format(tenant_test))["objects"]
    rule_rbac_template = {
        "sub_cat_value": {"permission": {"role": ""}},
        "obj_cat_value": {"permission": {"id": "", "action": ""}}
    }
    rule_mls_template = {
        "sub_cat_value": {"relation_super": {"subject_security_level": ""}},
        "obj_cat_value": {"relation_super": {"object_security_level": "", "action": ""}}
    }
    #Rules for admin (Alice)
    rule_rbac_template["sub_cat_value"]["permission"]["role"] = "admin"
    for _object in objects_dev:
        for _action in ("read", "os-start", "os-stop"):
            rule_rbac_template["obj_cat_value"]["permission"]["action"] = _action
            rule_rbac_template["obj_cat_value"]["permission"]["id"] = _object["uuid"]
            _data = get_url(
                "/json/intra-extension/{}/rules".format(ext1["uuid"]),
                post_data=rule_rbac_template
            )["rules"]
            print(_data)
    #Rules for Bob and Carol
    rule_rbac_template["sub_cat_value"]["permission"]["role"] = "Member"
    for _action in ("read", "os-start"):
        rule_rbac_template["obj_cat_value"]["permission"]["action"] = _action
        rule_rbac_template["obj_cat_value"]["permission"]["id"] = objects_dev[0]["uuid"]
        _data = get_url(
            "/json/intra-extension/{}/rules".format(ext1["uuid"]),
            post_data=rule_rbac_template
        )["rules"]
        print(_data)
    #Rules for Dave
    rule_mls_template["sub_cat_value"]["relation_super"]["subject_security_level"] = "high"
    for _object in objects_test:
        for _action in ("read", "os-start", "os-stop"):
            rule_mls_template["obj_cat_value"]["relation_super"]["action"] = _action
            rule_mls_template["obj_cat_value"]["relation_super"]["object_security_level"] = "medium"
            _data = get_url(
                "/json/intra-extension/{}/rules".format(ext2["uuid"]),
                post_data=rule_mls_template
            )["rules"]
            print(_data)
    #Rules for Eve
    rule_mls_template["sub_cat_value"]["relation_super"]["subject_security_level"] = "medium"
    for _action in ("read", "os-start"):
        rule_mls_template["obj_cat_value"]["relation_super"]["action"] = _action
        rule_mls_template["obj_cat_value"]["relation_super"]["object_security_level"] = "medium"
        _data = get_url(
            "/json/intra-extension/{}/rules".format(ext2["uuid"]),
            post_data=rule_mls_template
        )["rules"]
        print(_data)


def init():
    #Genering VM template
    new_vm_template = {
        "name": "VM-",
        "image_name": "Cirros3.2",
        "flavor_name": "m1.nano"
    }
    images = map(lambda x: x["name"], get_url("/pip/images/")["images"])
    for _img in images:
        if "irros" in _img:
            new_vm_template["name"] = _img

    tenant_admin, tenant_dev, tenant_test = init_tenants()
    ext1, ext2 = init_extensions(tenant_admin, tenant_dev, tenant_test)
    init_vms(tenant_admin, tenant_dev, tenant_test, ext1, ext2, new_vm_template)
    check_users(tenant_admin, tenant_dev, tenant_test, ext1, ext2)
    add_user_assignments(tenant_admin, tenant_dev, tenant_test, ext1, ext2)
    add_object_assignments(tenant_admin, tenant_dev, tenant_test, ext1, ext2)
    add_rules(tenant_admin, tenant_dev, tenant_test, ext1, ext2)

if __name__ == "__main__":
    init()