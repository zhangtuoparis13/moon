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

import unittest
import json
from moon_server.core.pip import get_pip
import httplib
from uuid import uuid4
from moon_server import settings

MOON_SERVER_IP = {
    "HOST": "127.0.0.1",
    "PORT": "8080",
    "BASEURL": "",
    "URL": ""
}

CREDENTIALS = {
    "login": getattr(settings, "OS_USERNAME"),
    "password": getattr(settings, "OS_PASSWORD"),
    "sessionid": "kxb50d9uusiywfcs2fiidmu1j5nsyckr",
    "csrftoken": ""
}


def start_moon_server():
    import subprocess
    import shlex
    import time
    print("Starting Moon server...")
    p = subprocess.Popen(shlex.split("python -m moon_server.server --policies /etc/moon/policies/ --run runserver 0.0.0.0:8080"))
    time.sleep(5)
    return p


def stop_moon_server(process):
    print("Killing Moon server...")
    import os
    try:
        pid = str(open("/var/run/moon.pid", "r").read())
    except IOError:
        pid = str(open("/tmp/moon.pid", "r").read())
    import signal
    os.kill(int(pid), signal.SIGTERM)
    ret = process.terminate()


def get_url(url, post_data=None, delete_data=None, crsftoken=None, method="GET"):
    # MOON_SERVER_IP["URL"] = url
    # _url = "http://{HOST}:{PORT}".format(**MOON_SERVER_IP)
    conn = httplib.HTTPConnection(MOON_SERVER_IP["HOST"], MOON_SERVER_IP["PORT"])
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        # "Accept": "text/plain",
        "Accept": "text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Cookie': 'sessionid={}'.format(CREDENTIALS["sessionid"]),
    }
    if crsftoken:
        headers["Cookie"] = "csrftoken={}; sessionid={}; NG_TRANSLATE_LANG_KEY:\"en\"".format(crsftoken, CREDENTIALS["sessionid"])
        CREDENTIALS["crsftoken"] = crsftoken
    if post_data:
        method = "POST"
        if crsftoken:
            post_data = "&".join(map(lambda x: "=".join(x), post_data))
        else:
            post_data = json.dumps(post_data)
        headers["Cookie"] = "csrftoken={}; sessionid={}; NG_TRANSLATE_LANG_KEY:\"en\"".format(
            CREDENTIALS["crsftoken"],
            CREDENTIALS["sessionid"])
        # conn.request(method, url, json.dumps(post_data), headers=headers)
        conn.request(method, url, post_data, headers=headers)
    elif delete_data:
        method = "DELETE"
        conn.request(method, url, json.dumps(delete_data), headers=headers)
    else:
        conn.request(method, url, headers=headers)
    resp = conn.getresponse()
    headers = resp.getheaders()
    if crsftoken:
        sessionid_start = dict(headers)["set-cookie"].index("sessionid=")+len("sessionid=")
        sessionid_end = dict(headers)["set-cookie"].index(";", sessionid_start)
        sessionid = dict(headers)["set-cookie"][sessionid_start:sessionid_end]
        CREDENTIALS["sessionid"] = sessionid
    content = resp.read()
    conn.close()
    try:
        return json.loads(content)
    except ValueError:
        return {"content": content}


class TestAdminInterface_IntraExtension(unittest.TestCase):

    def setUp(self):
        data = get_url("/auth/login/")
        sessionid = "gt9zf5lhjv86qnd6hnrk1ts3mkyk88rq"
        csrfmiddlewaretoken = filter(lambda x: "csrfmiddlewaretoken" in x, data['content'].splitlines())[0].split('"')[-2]
        post = [
            ("username", CREDENTIALS["login"]),
            ("password", CREDENTIALS["password"]),
            ("region", "http://openstackserver:5000/v3"),
            ("auth_url", "http://openstackserver:5000/v3"),
            ("csrfmiddlewaretoken", csrfmiddlewaretoken)
        ]
        auth = get_url("/auth/login/", post_data=post, crsftoken=csrfmiddlewaretoken)
        self.pip = get_pip()
        self.policies = get_url("/json/intra-extensions/policies")
        self.assertIsInstance(self.policies, dict)
        my_policy = self.policies["policies"].keys()[1]
        #Create first extension
        self.new_ext1 = get_url(
            "/json/intra-extensions/",
            post_data={"policymodel": my_policy, "name": "Intra_Extension Policy 1"})
        self.assertIsInstance(self.new_ext1, dict)
        self.new_ext1_uuid = self.new_ext1["intra_extensions"]["_id"]
        #Create second extension
        self.new_ext2 = get_url(
            "/json/intra-extensions/",
            post_data={"policymodel": my_policy, "name": "Intra_Extension Policy 2"})
        self.assertIsInstance(self.new_ext2, dict)
        self.new_ext2_uuid = self.new_ext2["intra_extensions"]["_id"]
        #Get Keystone tenants
        self.tenants = get_url("/pip/projects/")
        self.assertIsInstance(self.tenants, dict)
        self.tenant_admin = None
        self.tenant_demo = None
        for tenant in self.tenants["projects"]:
            if tenant["name"] == "admin":
                self.tenant_admin = tenant["uuid"]
            if tenant["name"] == "demo":
                self.tenant_demo = tenant["uuid"]
        #Create mapping between extensions and tenants
        mapping = get_url(
            "/json/super-extensions/".format(
                self.tenant_admin,
                self.new_ext1_uuid),
            post_data={
                "tenant_uuid": self.tenant_admin,
                "intra_extension_uuid": self.new_ext2_uuid
            }
        )
        mapping = get_url(
            "/json/super-extensions/",
            post_data={
                "tenant_uuid": self.tenant_demo,
                "intra_extension_uuid": self.new_ext2_uuid
            }
        )

    def tearDown(self):
        get_url("/json/intra-extensions/"+self.new_ext1_uuid+"/", method="DELETE")
        get_url("/json/intra-extensions/"+self.new_ext2_uuid+"/", method="DELETE")
        get_url("/auth/logout/")

    def test_errors(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        user = {
            "name": "TestUser"+str(uuid4()),
            'domain': "default",
            'enabled': True,
            'project': "admin",
            'password': "password",
            'description': "Test user for integration tests"
        }
        tenants = get_url("/pip/projects/")
        admin_tenant = filter(lambda x: x["name"] == "admin", tenants["projects"])
        ext = data["intra_extensions"][0]
        # ext_data = get_url("/json/intra-extension/"+ext+"/")
        _data = get_url("/json/intra-extensions/"+ext+"/subjects/", post_data=user)
        self.assertIsInstance(_data, dict)
        self.assertIn("subjects", _data)
        self.assertIsInstance(_data["subjects"], list)
        self.assertEqual(len(_data["subjects"]) > 0, True)

    def test_intra_extensions(self):
        number_of_intra_ext = len(get_url("/json/intra-extensions/")["intra_extensions"])
        #add an intra-extension
        self.policies = get_url("/json/intra-extensions/policies")
        self.assertIsInstance(self.policies, dict)
        my_policy = self.policies["policies"].keys()[0]
        #Create the extension
        self.new_ext1 = get_url(
            "/json/intra-extensions/",
            post_data={"policymodel": my_policy, "name": "Intra_Extension Test"})
        self.assertIsInstance(self.new_ext1, dict)
        self.new_ext1_uuid = self.new_ext1["intra_extensions"]["_id"]
        self.assertEqual(number_of_intra_ext+1, len(get_url("/json/intra-extensions/")["intra_extensions"]))
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extensions/"+ext+"/")
            self.assertIsInstance(_data, dict)
            for k in [u'admin', u'authz', u'_id', u'name']:
                self.assertIn(k, _data["intra_extensions"].keys())
            for k in [u'perimeter', u'assignment', u'configuration', u'metadata']:
                self.assertIn(k, _data["intra_extensions"]['admin'].keys())
            for k in [u'perimeter', u'assignment', u'configuration', u'metadata']:
                self.assertIn(k, _data["intra_extensions"]['authz'].keys())
            self.assertIsInstance(_data["intra_extensions"]["_id"], unicode)
            # print(json.dumps(_data, indent=4))
        self.assertEqual(number_of_intra_ext+1, len(get_url("/json/intra-extensions/")["intra_extensions"]))
        #Get Keystone tenants
        self.tenants = get_url("/pip/projects/")
        self.assertIsInstance(self.tenants, dict)
        self.tenant_admin = None
        self.tenant_demo = None
        for tenant in self.tenants["projects"]:
            if tenant["name"] == "admin":
                self.tenant_admin = tenant["uuid"]
            if tenant["name"] == "demo":
                self.tenant_demo = tenant["uuid"]
        #Create mapping between extensions and tenants
        mapping = get_url(
            "/json/super-extensions/",
            post_data={
                "tenant_uuid": self.tenant_admin,
                "intra_extension_uuid": self.new_ext1_uuid
            }
        )
        #delete an intra-extension
        get_url("/json/intra-extensions/"+self.new_ext1_uuid+"/", method="DELETE")
        self.assertEqual(number_of_intra_ext, len(get_url("/json/intra-extensions/")["intra_extensions"]))

    def test_subjects(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extensions/"+ext+"/subjects/")
            self.assertIsInstance(_data, dict)
            self.assertIn("subjects", _data)
            self.assertIsInstance(_data["subjects"], list)
            self.assertEqual(len(_data["subjects"]) > 0, True)

    def test_objects(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extensions/"+ext+"/objects/")
            self.assertIsInstance(_data, dict)
            self.assertIn("objects", _data)
            self.assertIsInstance(_data["objects"], list)
            self.assertEqual(len(_data["objects"]) > 0, True)

    def test_subject(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        user = {
            "name": "TestUser"+str(uuid4()),
            'domain': "default",
            'enabled': True,
            'project': "admin",
            'password': "password",
            'description': "Test user for integration tests"
        }
        tenants = get_url("/pip/projects/")
        admin_tenant = filter(lambda x: x["name"] == "admin", tenants["projects"])
        for ext in data["intra_extensions"]:
            # ext_data = get_url("/json/intra-extension/"+ext+"/")
            _data = get_url("/json/intra-extensions/"+ext+"/subjects/", post_data=user)
            self.assertIsInstance(_data, dict)
            self.assertIn("subjects", _data)
            self.assertIsInstance(_data["subjects"], list)
            self.assertEqual(len(_data["subjects"]) > 0, True)
            user_uuid = None
            k_users = get_url("/pip/projects/{}/users/".format(admin_tenant[0]["uuid"]))
            searched_user = False
            for k_user in k_users["users"]:
                if k_user["name"] == user["name"]:
                    user_uuid = k_user["uuid"]
                    searched_user = True
                    break
            self.assertIs(searched_user, True)
            searched_user = False
            for m_user in _data["subjects"]:
                if m_user == user_uuid:
                    searched_user = True
                    break
            self.assertIs(searched_user, True)
            # self.assertIn(user["uuid"], _data["subjects"])
            _data = get_url("/json/intra-extensions/"+ext+"/subjects/"+user_uuid+"/", method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("subjects", _data)
            self.assertIsInstance(_data["subjects"], list)
            self.assertEqual(len(_data["subjects"]) > 0, True)
            self.assertNotIn(user_uuid, _data["subjects"])

    def test_object(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        new_vm = {
            "name": "MoonTestGUI-"+str(uuid4()),
            "image_name": "Cirros3.2",
            "flavor_name": "m1.nano"
        }
        images = map(lambda x: x["name"], get_pip().get_images())
        for _img in images:
            if "irros" in _img:
                new_vm["image_name"] = _img
        #Before doing anything we have add an extension and map it to a tenant
        policies = get_url("/json/intra-extensions/policies")
        self.assertIsInstance(policies, dict)
        my_policy = policies["policies"].keys()[0]
        new_ext = get_url("/json/intra-extensions/", post_data={"policymodel": my_policy, "name": "TestGUI_IntraExtension"})
        self.assertIsInstance(new_ext, dict)
        new_ext_uuid = new_ext["intra_extensions"]["_id"]
        tenants = get_url("/pip/projects/")
        self.assertIsInstance(tenants, dict)
        tenant_admin = None
        for tenant in tenants["projects"]:
            if tenant["name"] == "admin":
                tenant_admin = tenant["uuid"]
                break
        mapping = get_url(
            "/json/super-extensions/",
            post_data={
                "tenant_uuid": tenant_admin,
                "intra_extension_uuid": new_ext_uuid
            }
        )
        #Add a new server
        _data = get_url("/json/intra-extensions/"+new_ext_uuid+"/objects/", post_data=new_vm)
        self.assertIsInstance(_data, dict)
        self.assertIn("objects", _data)
        self.assertIsInstance(_data["objects"], list)
        self.assertEqual(len(_data["objects"]) > 0, True)
        objects = get_url("/pip/projects/{}/objects/".format(tenant_admin))
        self.assertIsInstance(objects, dict)
        for obj in objects["objects"]:
            if obj["name"] == new_vm["name"]:
                new_vm["uuid"] = obj["uuid"]
        self.assertIn("uuid", new_vm)
        self.assertIn(new_vm["uuid"], _data["objects"])
        #Delete the previous server
        _data = get_url("/json/intra-extensions/"+new_ext_uuid+"/objects/"+new_vm["uuid"]+"/", method="DELETE")
        objects = get_url("/pip/projects/{}/objects/".format(tenant_admin))
        self.assertIsInstance(objects, dict)
        self.assertNotIn(new_vm["uuid"], map(lambda x: x["uuid"], objects["objects"]))
        self.assertNotIn(new_vm["uuid"], _data["objects"])

    def test_subject_categories(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extensions/"+ext+"/subject_categories/")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_categories", _data)
            self.assertIsInstance(_data["subject_categories"], list)
            self.assertEqual(len(_data["subject_categories"]) > 0, True)

    def test_object_categories(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extensions/"+ext+"/object_categories/")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_categories", _data)
            self.assertIsInstance(_data["object_categories"], list)
            self.assertEqual(len(_data["object_categories"]) > 0, True)

    def test_subject_category(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extensions/"+ext+"/subject_categories/", post_data={"category_id": "my_category"})
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_categories", _data)
            self.assertIsInstance(_data["subject_categories"], list)
            self.assertEqual(len(_data["subject_categories"]) > 0, True)
            self.assertIn("my_category", _data["subject_categories"])
            _data = get_url("/json/intra-extensions/"+ext+"/subject_categories/my_category/", method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_categories", _data)
            self.assertIsInstance(_data["subject_categories"], list)
            self.assertEqual(len(_data["subject_categories"]) > 0, True)
            self.assertNotIn("my_category", _data["subject_categories"])

    def test_object_category(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extensions/"+ext+"/object_categories/", post_data={"category_id": "my_category"})
            self.assertIsInstance(_data, dict)
            self.assertIn("object_categories", _data)
            self.assertIsInstance(_data["object_categories"], list)
            self.assertEqual(len(_data["object_categories"]) > 0, True)
            self.assertIn("my_category", _data["object_categories"])
            _data = get_url("/json/intra-extensions/"+ext+"/object_categories/my_category/", method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_categories", _data)
            self.assertIsInstance(_data["object_categories"], list)
            self.assertEqual(len(_data["object_categories"]) > 0, True)
            self.assertNotIn("my_category", _data["object_categories"])

    def test_subject_category_values(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            categories = get_url("/json/intra-extensions/"+ext+"/subject_categories/")
            _data = get_url("/json/intra-extensions/"+ext+"/subject_category_values/")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_category_values", _data)
            self.assertIsInstance(_data["subject_category_values"], dict)
            for key in _data["subject_category_values"]:
                self.assertIsInstance(_data["subject_category_values"][key], list)
                self.assertIn(key, categories["subject_categories"])

    # TODO: adding a new category must imply modifying meta_rules (which don't work actually)
    # def test_subject_category_value(self):
    #     data = get_url("/json/intra-extensions/")
    #     self.assertIsInstance(data, dict)
    #     for ext in data["intra_extensions"]:
    #         _data = get_url("/json/intra-extensions/"+ext+"/subject_categories/", post_data={"category_id": "my_category"})
    #         self.assertIsInstance(_data, dict)
    #         self.assertIn("subject_categories", _data)
    #         self.assertIsInstance(_data["subject_categories"], list)
    #         self.assertEqual(len(_data["subject_categories"]) > 0, True)
    #         self.assertIn("my_category", _data["subject_categories"])
    #         _data = get_url("/json/intra-extensions/"+ext+"/subject_category_values/")
    #         self.assertIsInstance(_data, dict)
    #         self.assertIn("subject_category_values", _data)
    #         self.assertIsInstance(_data["subject_category_values"], dict)
    #         #Adding a value in a pre-existent category
    #         for val in [u'high', u'medium', u'low']:
    #             self.assertIn(val, _data["subject_category_values"]["subject_security_level"])
    #         _data = get_url("/json/intra-extensions/"+ext+"/subject_category_values/",
    #                         post_data={"category_id": "subject_security_level", "value": "ultra-low1"})
    #         self.assertIsInstance(_data, dict)
    #         self.assertIn("subject_category_values", _data)
    #         self.assertIsInstance(_data["subject_category_values"], dict)
    #         #Deleting a value in a pre-existent category
    #         for val in [u'high', u'medium', u'low', u"ultra-low1"]:
    #             self.assertIn(val, _data["subject_category_values"]["subject_security_level"])
    #         _data = get_url("/json/intra-extensions/"+ext+"/subject_category_values/subject_security_level/ultra-low1",
    #                         method="DELETE")
    #         self.assertIsInstance(_data, dict)
    #         self.assertIn("subject_category_values", _data)
    #         self.assertIsInstance(_data["subject_category_values"], dict)
    #         for val in [u'high', u'medium', u'low']:
    #             self.assertIn(val, _data["subject_category_values"]["subject_security_level"])
    #         self.assertNotIn(u"ultra-low1", _data["subject_category_values"]["subject_security_level"])
    #         #Adding a value in a new category
    #         _data = get_url("/json/intra-extensions/"+ext+"/subject_category_values/",
    #                         post_data={"category_id": "my_category", "value": "my_category_value1"})
    #         _data = get_url("/json/intra-extensions/"+ext+"/subject_category_values/",
    #                         post_data={"category_id": "my_category", "value": "my_category_value2"})
    #         self.assertIsInstance(_data, dict)
    #         self.assertIn("subject_category_values", _data)
    #         self.assertIsInstance(_data["subject_category_values"], dict)
    #         for val in [u'my_category_value1', u'my_category_value2']:
    #             self.assertIn(val, _data["subject_category_values"]["my_category"])
    #         #Deleting a value in a new category
    #         for val in [u'my_category_value1', u'my_category_value2']:
    #             self.assertIn(val, _data["subject_category_values"]["my_category"])
    #         _data = get_url("/json/intra-extensions/"+ext+"/subject_category_values/my_category/my_category_value1",
    #                         method="DELETE")
    #         _data = get_url("/json/intra-extensions/"+ext+"/subject_category_values/my_category/my_category_value2",
    #                         method="DELETE")
    #         self.assertIsInstance(_data, dict)
    #         self.assertIn("subject_category_values", _data)
    #         self.assertIsInstance(_data["subject_category_values"], dict)
    #         for val in [u'my_category_value1', u'my_category_value2']:
    #             self.assertNotIn(val, _data["subject_category_values"]["my_category"])
    #         #Deleting the new category
    #         _data = get_url("/json/intra-extensions/"+ext+"/subject_categories/my_category",
    #                         method="DELETE")
    #         self.assertIsInstance(_data, dict)
    #         self.assertIn("subject_categories", _data)
    #         self.assertIsInstance(_data["subject_categories"], list)
    #         self.assertEqual(len(_data["subject_categories"]) > 0, True)
    #         self.assertNotIn("my_category", _data["subject_categories"])

    def test_object_category_values(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            categories = get_url("/json/intra-extensions/"+ext+"/object_categories/")
            _data = get_url("/json/intra-extensions/"+ext+"/object_category_values/")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_category_values", _data)
            self.assertIsInstance(_data["object_category_values"], dict)
            for key in _data["object_category_values"]:
                self.assertIsInstance(_data["object_category_values"][key], list)
                self.assertIn(key, categories["object_categories"])

    # TODO: adding a new category must imply modifying meta_rules (which don't work actually)
    # def test_object_category_value(self):
    #     data = get_url("/json/intra-extensions/")
    #     self.assertIsInstance(data, dict)
    #     for ext in data["intra_extensions"]:
    #         _data = get_url("/json/intra-extensions/"+ext+"/object_categories/", post_data={"category_id": "my_category"})
    #         self.assertIsInstance(_data, dict)
    #         self.assertIn("object_categories", _data)
    #         self.assertIsInstance(_data["object_categories"], list)
    #         self.assertEqual(len(_data["object_categories"]) > 0, True)
    #         self.assertIn("my_category", _data["object_categories"])
    #         _data = get_url("/json/intra-extensions/"+ext+"/object_category_values/")
    #         self.assertIsInstance(_data, dict)
    #         self.assertIn("object_category_values", _data)
    #         self.assertIsInstance(_data["object_category_values"], dict)
    #         #Adding a value in a pre-existent category
    #         for val in [u'high', u'medium', u'low']:
    #             self.assertIn(val, _data["object_category_values"]["object_security_level"])
    #         _data = get_url("/json/intra-extensions/"+ext+"/object_category_values/",
    #                         post_data={"category_id": "object_security_level", "value": "ultra-low"})
    #         self.assertIsInstance(_data, dict)
    #         self.assertIn("object_category_values", _data)
    #         self.assertIsInstance(_data["object_category_values"], dict)
    #         #Deleting a value in a pre-existent category
    #         for val in [u'high', u'medium', u'low', u"ultra-low"]:
    #             self.assertIn(val, _data["object_category_values"]["object_security_level"])
    #         _data = get_url("/json/intra-extensions/"+ext+"/object_category_values/object_security_level/ultra-low",
    #                         method="DELETE")
    #         self.assertIsInstance(_data, dict)
    #         self.assertIn("object_category_values", _data)
    #         self.assertIsInstance(_data["object_category_values"], dict)
    #         for val in [u'high', u'medium', u'low']:
    #             self.assertIn(val, _data["object_category_values"]["object_security_level"])
    #         self.assertNotIn(u"ultra-low", _data["object_category_values"]["object_security_level"])
    #         #Adding a value in a new category
    #         _data = get_url("/json/intra-extensions/"+ext+"/object_category_values/",
    #                         post_data={"category_id": "my_category", "value": "my_category_value1"})
    #         _data = get_url("/json/intra-extensions/"+ext+"/object_category_values/",
    #                         post_data={"category_id": "my_category", "value": "my_category_value2"})
    #         self.assertIsInstance(_data, dict)
    #         self.assertIn("object_category_values", _data)
    #         self.assertIsInstance(_data["object_category_values"], dict)
    #         for val in [u'my_category_value1', u'my_category_value2']:
    #             self.assertIn(val, _data["object_category_values"]["my_category"])
    #         #Deleting a value in a new category
    #         for val in [u'my_category_value1', u'my_category_value2']:
    #             self.assertIn(val, _data["object_category_values"]["my_category"])
    #         _data = get_url("/json/intra-extensions/"+ext+"/object_category_values/my_category/my_category_value1",
    #                         method="DELETE")
    #         _data = get_url("/json/intra-extensions/"+ext+"/object_category_values/my_category/my_category_value2",
    #                         method="DELETE")
    #         self.assertIsInstance(_data, dict)
    #         self.assertIn("object_category_values", _data)
    #         self.assertIsInstance(_data["object_category_values"], dict)
    #         for val in [u'my_category_value1', u'my_category_value2']:
    #             self.assertNotIn(val, _data["object_category_values"]["my_category"])
    #         #Deleting the new category
    #         _data = get_url("/json/intra-extensions/"+ext+"/object_categories/my_category",
    #                         method="DELETE")
    #         self.assertIsInstance(_data, dict)
    #         self.assertIn("object_categories", _data)
    #         self.assertIsInstance(_data["object_categories"], list)
    #         self.assertEqual(len(_data["object_categories"]) > 0, True)
    #         self.assertNotIn("my_category", _data["object_categories"])

    def test_subject_assignments(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            categories = get_url("/json/intra-extensions/"+ext+"/subject_categories/")
            _data = get_url("/json/intra-extensions/"+ext+"/subject_assignments/")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_assignments", _data)
            self.assertIsInstance(_data["subject_assignments"], dict)
            for key in _data["subject_assignments"]:
                self.assertIsInstance(_data["subject_assignments"][key], dict)
                self.assertIn(key, categories["subject_categories"])

    def test_subject_assignment(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        tested = False
        for ext in data["intra_extensions"]:
            user = get_url("/json/intra-extensions/"+ext+"/subjects/")["subjects"][0]
            #Add a new subject category value for the test
            if "MLS" not in get_url("/json/intra-extensions/"+ext)["intra_extensions"]["authz"]["metadata"]["model"]:
                continue
            _data = get_url("/json/intra-extensions/"+ext+"/subject_category_values/",
                            post_data={"category_id": "subject_security_level", "value": "ultra-low2"})
            self.assertIsInstance(_data, dict)
            if "subject_security_level" in _data["subject_category_values"].keys():
                tested = True
            else:
                continue
            self.assertIn("subject_category_values", _data)
            self.assertIsInstance(_data["subject_category_values"], dict)
            for val in [u'high', u'medium', u'low', u"ultra-low2"]:
                self.assertIn(val, _data["subject_category_values"]["subject_security_level"])
            _data = get_url("/json/intra-extensions/"+ext+"/subject_assignments/")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_assignments", _data)
            self.assertIsInstance(_data["subject_assignments"], dict)
            # for cat in get_url("/json/intra-extensions/"+ext+"/subject_categories/")["subject_categories"]:
            #     for val in get_url("/json/intra-extensions/"+ext+"/subjects/")["subjects"]:
            #         self.assertIn(val, _data['subject_assignments'][cat].keys())
            #Add now a new assignment
            _data = get_url("/json/intra-extensions/"+ext+"/subject_assignments/",
                            post_data={
                                "category_id": "subject_security_level",
                                "value": "ultra-low2",
                                "subject_id": user
                            })
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_assignments", _data)
            self.assertIsInstance(_data["subject_assignments"], dict)
            self.assertIn("subject_security_level", _data["subject_assignments"])
            self.assertIsInstance(_data["subject_assignments"]["subject_security_level"], dict)
            self.assertIn(user, _data["subject_assignments"]["subject_security_level"])
            self.assertIsInstance(_data["subject_assignments"]["subject_security_level"][user], list)
            self.assertIn("ultra-low2", _data["subject_assignments"]["subject_security_level"][user])
            #Delete the last assignment
            _data = get_url(
                "/json/intra-extensions/"+ext+"/subject_assignments/"+user+"/subject_security_level/ultra-low2",
                method="DELETE"
            )
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_assignments", _data)
            self.assertIsInstance(_data["subject_assignments"], dict)
            self.assertIn("subject_security_level", _data["subject_assignments"])
            self.assertIsInstance(_data["subject_assignments"]["subject_security_level"], dict)
            self.assertIn(user, _data["subject_assignments"]["subject_security_level"])
            self.assertIsInstance(_data["subject_assignments"]["subject_security_level"][user], list)
            self.assertNotIn("ultra-low2", _data["subject_assignments"]["subject_security_level"][user])
            #Adding a new category
            _data = get_url("/json/intra-extensions/"+ext+"/subject_categories/", post_data={"category_id": "my_category"})
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_categories", _data)
            self.assertIsInstance(_data["subject_categories"], list)
            self.assertEqual(len(_data["subject_categories"]) > 0, True)
            self.assertIn("my_category", _data["subject_categories"])
            #Adding a value in a new category
            _data = get_url("/json/intra-extensions/"+ext+"/subject_category_values/",
                            post_data={"category_id": "my_category", "value": "my_category_value1"})
            _data = get_url("/json/intra-extensions/"+ext+"/subject_category_values/",
                            post_data={"category_id": "my_category", "value": "my_category_value2"})
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_category_values", _data)
            self.assertIsInstance(_data["subject_category_values"], dict)
            for val in [u'my_category_value1', u'my_category_value2']:
                self.assertIn(val, _data["subject_category_values"]["my_category"])
            #Adding a new assignment
            assign = {
                "subject_id": user,
                "category_id": "my_category",
                "value": "my_category_value2"
            }
            _data = get_url("/json/intra-extensions/"+ext+"/subject_assignments/",
                            post_data=assign)
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_assignments", _data)
            self.assertIsInstance(_data["subject_assignments"], dict)
            self.assertIn("my_category", _data["subject_assignments"])
            self.assertIsInstance(_data["subject_assignments"]["my_category"], dict)
            self.assertIn(user, _data["subject_assignments"]["my_category"])
            self.assertIsInstance(_data["subject_assignments"]["my_category"][user], list)
            self.assertIn("my_category_value2", _data["subject_assignments"]["my_category"][user])
            #Deleting a value in a new category
            _data = get_url("/json/intra-extensions/"+ext+"/subject_category_values/")
            for val in [u'my_category_value1', u'my_category_value2']:
                self.assertIn(val, _data["subject_category_values"]["my_category"])
            _data = get_url("/json/intra-extensions/"+ext+"/subject_category_values/my_category/my_category_value1",
                            method="DELETE")
            _data = get_url("/json/intra-extensions/"+ext+"/subject_category_values/my_category/my_category_value2",
                            method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_category_values", _data)
            self.assertIsInstance(_data["subject_category_values"], dict)
            for val in [u'my_category_value1', u'my_category_value2']:
                self.assertNotIn(val, _data["subject_category_values"]["my_category"])
            #Deleting the new category
            _data = get_url("/json/intra-extensions/"+ext+"/subject_categories/my_category",
                            method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_categories", _data)
            self.assertIsInstance(_data["subject_categories"], list)
            self.assertEqual(len(_data["subject_categories"]) > 0, True)
            self.assertNotIn("my_category", _data["subject_categories"])
        self.assertIs(tested, True)

    def test_object_assignments(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            categories = get_url("/json/intra-extensions/"+ext+"/object_categories/")
            _data = get_url("/json/intra-extensions/"+ext+"/object_assignments/")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_assignments", _data)
            self.assertIsInstance(_data["object_assignments"], dict)
            for key in _data["object_assignments"]:
                self.assertIsInstance(_data["object_assignments"][key], dict)
                self.assertIn(key, categories["object_categories"])

    def test_object_assignment(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        tested = False
        for ext in data["intra_extensions"]:
            obj = get_url("/json/intra-extensions/"+ext+"/objects/")["objects"][0]
            #Add a new object category value for the test
            if "MLS" not in get_url("/json/intra-extensions/"+ext)["intra_extensions"]["authz"]["metadata"]["model"]:
                continue
            _data = get_url("/json/intra-extensions/"+ext+"/object_category_values/",
                            post_data={"category_id": "object_security_level", "value": "ultra-low2"})
            if "object_security_level" in _data["object_category_values"].keys():
                tested = True
            else:
                continue
            self.assertIsInstance(_data, dict)
            self.assertIn("object_category_values", _data)
            self.assertIsInstance(_data["object_category_values"], dict)
            for val in [u'high', u'medium', u'low', u"ultra-low2"]:
                self.assertIn(val, _data["object_category_values"]["object_security_level"])
            _data = get_url("/json/intra-extensions/"+ext+"/object_assignments/")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_assignments", _data)
            self.assertIsInstance(_data["object_assignments"], dict)
            # for cat in get_url("/json/intra-extensions/"+ext+"/object_categories/")["object_categories"]:
            #     for val in get_url("/json/intra-extensions/"+ext+"/objects/")["objects"]:
            #         self.assertIn(val, _data['object_assignments'][cat].keys())
            #Add now a new assignment
            _data = get_url("/json/intra-extensions/"+ext+"/object_assignments/",
                            post_data={
                                "category_id": "object_security_level",
                                "value": "ultra-low2",
                                "object_id": obj
                            })
            self.assertIsInstance(_data, dict)
            self.assertIn("object_assignments", _data)
            self.assertIsInstance(_data["object_assignments"], dict)
            self.assertIn("object_security_level", _data["object_assignments"])
            self.assertIsInstance(_data["object_assignments"]["object_security_level"], dict)
            self.assertIn(obj, _data["object_assignments"]["object_security_level"])
            self.assertIsInstance(_data["object_assignments"]["object_security_level"][obj], list)
            self.assertIn("ultra-low2", _data["object_assignments"]["object_security_level"][obj])
            #Delete the last assignment
            _data = get_url(
                "/json/intra-extensions/"+ext+"/object_assignments/"+obj+"/object_security_level/ultra-low2",
                method="DELETE"
            )
            self.assertIsInstance(_data, dict)
            self.assertIn("object_assignments", _data)
            self.assertIsInstance(_data["object_assignments"], dict)
            self.assertIn("object_security_level", _data["object_assignments"])
            self.assertIsInstance(_data["object_assignments"]["object_security_level"], dict)
            self.assertIn(obj, _data["object_assignments"]["object_security_level"])
            self.assertIsInstance(_data["object_assignments"]["object_security_level"][obj], list)
            self.assertNotIn("ultra-low2", _data["object_assignments"]["object_security_level"][obj])
            #Adding a new category
            _data = get_url("/json/intra-extensions/"+ext+"/object_categories/", post_data={"category_id": "my_category"})
            self.assertIsInstance(_data, dict)
            self.assertIn("object_categories", _data)
            self.assertIsInstance(_data["object_categories"], list)
            self.assertEqual(len(_data["object_categories"]) > 0, True)
            self.assertIn("my_category", _data["object_categories"])
            #Adding a value in a new category
            _data = get_url("/json/intra-extensions/"+ext+"/object_category_values/",
                            post_data={"category_id": "my_category", "value": "my_category_value1"})
            _data = get_url("/json/intra-extensions/"+ext+"/object_category_values/",
                            post_data={"category_id": "my_category", "value": "my_category_value2"})
            self.assertIsInstance(_data, dict)
            self.assertIn("object_category_values", _data)
            self.assertIsInstance(_data["object_category_values"], dict)
            for val in [u'my_category_value1', u'my_category_value2']:
                self.assertIn(val, _data["object_category_values"]["my_category"])
            #Adding a new assignment
            assign = {
                "object_id": obj,
                "category_id": "my_category",
                "value": "my_category_value2"
            }
            _data = get_url("/json/intra-extensions/"+ext+"/object_assignments/",
                            post_data=assign)
            self.assertIsInstance(_data, dict)
            self.assertIn("object_assignments", _data)
            self.assertIsInstance(_data["object_assignments"], dict)
            self.assertIn("my_category", _data["object_assignments"])
            self.assertIsInstance(_data["object_assignments"]["my_category"], dict)
            self.assertIn(obj, _data["object_assignments"]["my_category"])
            self.assertIsInstance(_data["object_assignments"]["my_category"][obj], list)
            self.assertIn("my_category_value2", _data["object_assignments"]["my_category"][obj])
            #Deleting a value in a new category
            _data = get_url("/json/intra-extensions/"+ext+"/object_category_values/")
            for val in [u'my_category_value1', u'my_category_value2']:
                self.assertIn(val, _data["object_category_values"]["my_category"])
            _data = get_url("/json/intra-extensions/"+ext+"/object_category_values/my_category/my_category_value1",
                            method="DELETE")
            _data = get_url("/json/intra-extensions/"+ext+"/object_category_values/my_category/my_category_value2",
                            method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_category_values", _data)
            self.assertIsInstance(_data["object_category_values"], dict)
            for val in [u'my_category_value1', u'my_category_value2']:
                self.assertNotIn(val, _data["object_category_values"]["my_category"])
            #Deleting the new category
            _data = get_url("/json/intra-extensions/"+ext+"/object_categories/my_category",
                            method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_categories", _data)
            self.assertIsInstance(_data["object_categories"], list)
            self.assertEqual(len(_data["object_categories"]) > 0, True)
            self.assertNotIn("my_category", _data["object_categories"])
        self.assertIs(tested, True)

    def test_rules(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extensions/"+ext+"/rules/")
            self.assertIsInstance(_data, dict)
            self.assertIn("rules", _data)
            self.assertIsInstance(_data["rules"], dict)

    def test_meta_rules(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extensions/"+ext+"/meta_rules/")
            self.assertIsInstance(_data, dict)
            self.assertIn("meta_rules", _data)
            self.assertIsInstance(_data["meta_rules"], dict)

    def test_rule(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            if "MLS" not in get_url("/json/intra-extensions/"+ext)["intra_extensions"]["authz"]["metadata"]["model"]:
                continue
            _data = get_url("/json/intra-extensions/"+ext+"/rules/")
            self.assertIsInstance(_data, dict)
            self.assertIn("rules", _data)
            self.assertIsInstance(_data["rules"], dict)
            post_data = {
                "sub_cat_value":
                    {"relation_super": {"subject_security_level": "low"}},
                "obj_cat_value":
                    {"relation_super": {"object_security_level": "low", "action": "write"}}
            }
            _data = get_url(
                "/json/intra-extensions/"+ext+"/rules/",
                post_data=post_data
            )
            self.assertIsInstance(_data, dict)
            self.assertIn("rules", _data)
            self.assertIsInstance(_data["rules"], dict)
            self.assertIn(post_data, _data["rules"]["relation_super"])
            _data = get_url(
                "/json/intra-extensions/"+ext+"/rules/",
                delete_data={
                    "sub_cat_value":
                        {"relation_super": {"subject_security_level": "low"}},
                    "obj_cat_value":
                        {"relation_super": {"object_security_level": "low", "action": "write"}}
                }
            )
            self.assertIsInstance(_data, dict)
            self.assertIn("rules", _data)
            self.assertIsInstance(_data["rules"], dict)
            self.assertIsInstance(_data["rules"]["relation_super"], list)
            self.assertNotIn(post_data, _data["rules"]["relation_super"])


# TODO: Collaboration is not ready yet
# class TestAdminInterface_InterExtension(unittest.TestCase):
#
#     def setUp(self):
#         data = get_url("/auth/login/")
#         sessionid = "gt9zf5lhjv86qnd6hnrk1ts3mkyk88rq"
#         csrfmiddlewaretoken = filter(lambda x: "csrfmiddlewaretoken" in x, data['content'].splitlines())[0].split('"')[-2]
#         post = [
#             ("username", CREDENTIALS["login"]),
#             ("password", CREDENTIALS["password"]),
#             ("region", "http://openstackserver:5000/v3"),
#             ("auth_url", "http://openstackserver:5000/v3"),
#             ("csrfmiddlewaretoken", csrfmiddlewaretoken)
#         ]
#         auth = get_url("/auth/login/", post_data=post, crsftoken=csrfmiddlewaretoken)
#         self.pip = get_pip()
#         self.policies = get_url("/json/intra-extensions/policies")
#         self.assertIsInstance(self.policies, dict)
#         my_policy = self.policies["policies"].keys()[0]
#         #Create first extension
#         self.new_ext1 = get_url(
#             "/json/intra-extensions/",
#             post_data={"policymodel": my_policy, "name": "Intra_Extension Policy 1"})
#         self.assertIsInstance(self.new_ext1, dict)
#         self.new_ext1_uuid = self.new_ext1["intra_extensions"]["_id"]
#         #Create second extension
#         self.new_ext2 = get_url(
#             "/json/intra-extensions/",
#             post_data={"policymodel": my_policy, "name": "Intra_Extension Policy 2"})
#         self.assertIsInstance(self.new_ext2, dict)
#         self.new_ext2_uuid = self.new_ext2["intra_extensions"]["_id"]
#         #Get Keystone tenants
#         self.tenants = get_url("/pip/projects/")
#         self.assertIsInstance(self.tenants, dict)
#         self.tenant_admin = None
#         self.tenant_demo = None
#         for tenant in self.tenants["projects"]:
#             if tenant["name"] == "admin":
#                 self.tenant_admin = tenant["uuid"]
#             if tenant["name"] == "demo":
#                 self.tenant_demo = tenant["uuid"]
#         #Create mapping between extensions and tenants
#         mapping = get_url(
#             "/json/super-extensions/",
#             post_data={
#                 "tenant_uuid": self.tenant_admin,
#                 "intra_extension_uuid": self.new_ext1_uuid
#             }
#         )
#         mapping = get_url(
#             "/json/super-extensions/",
#             post_data={
#                 "tenant_uuid": self.tenant_demo,
#                 "intra_extension_uuid": self.new_ext2_uuid
#             }
#         )
#
#     def tearDown(self):
#         #Delete intra_extensions
#         get_url("/json/intra-extensions/"+self.new_ext1_uuid+"/", method="DELETE")
#         get_url("/json/intra-extensions/"+self.new_ext2_uuid+"/", method="DELETE")
#         get_url("/auth/logout/")
#
#     def test_inter_extensions(self):
#         data = get_url("/json/inter-extensions/")
#         extensions = get_url("/json/intra-extensions/")
#         self.assertIs(len(extensions["intra_extensions"]) >= 2, True)
#         self.assertIsInstance(data, dict)
#         self.assertIs(len(data["inter_extensions"]) == 0, True)
#         #TODO subjects_1 = get_url("/json/intra-extensions/{}/subjects".format(extensions["intra_extensions"][0]))["subjects"]
#         #TODO objects_2 = get_url("/json/intra-extensions/{}/objects".format(extensions["intra_extensions"][1]))["objects"]
#         data = get_url(
#             "/json/inter-extensions/",
#             post_data={
#                 "requesting_intra_extension_uuid": extensions["intra_extensions"][0],
#                 "requested_intra_extension_uuid": extensions["intra_extensions"][1],
#                 "genre": "trust",
#                 "sub_list": ['user1', 'user2'],
#                 "obj_list": ['vm1', 'vm2'],
#                 "act": "write"
#             })
#         self.assertIsInstance(data, dict)
#         self.assertIn('inter_extensions', data)
#         inter_ext_uuid = get_url("/json/inter-extensions/")[u'inter_extensions'][0]["uuid"]
#         inter_ext_vents = get_url("/json/inter-extensions/")[u'inter_extensions'][0]["vents"]["trust"][0]["uuid"]
#         self.assertIs(len(data["inter_extensions"]) > 0, True)
#         #TODO test the content of data
#         #Delete an inter-extension
#         data = get_url(
#             "/json/inter-extensions/"+inter_ext_uuid+"/",
#             delete_data={
#                 "vents": inter_ext_vents,
#                 "genre": "trust",
#             })
#         self.assertIsInstance(data, dict)
#         inter_ext_vents = get_url("/json/inter-extensions/")[u'inter_extensions']
#         self.assertIs(len(inter_ext_vents) == 0, True)
#         #TODO delete the correct vent uuid
#         # for ext in data["inter_extensions"]:
#         #     _data = get_url("/json/inter-extension/"+ext+"/")
#         #     self.assertIsInstance(_data, list)
#         #     # for k in [u'admin', u'authz', u'_id']:
#         #     #     self.assertIn(k, _data.keys())
#         #     # for k in [u'perimeter', u'assignment', u'configuration', u'metadata']:
#         #     #     self.assertIn(k, _data['admin'].keys())
#         #     # for k in [u'perimeter', u'assignment', u'configuration', u'metadata']:
#         #     #     self.assertIn(k, _data['authz'].keys())
#         #     # self.assertIsInstance(_data["_id"], unicode)
#         #     print(json.dumps(_data, indent=4))


class TestPIPInterface(unittest.TestCase):

    def setUp(self):
        data = get_url("/auth/login/")
        sessionid = "gt9zf5lhjv86qnd6hnrk1ts3mkyk88rq"
        csrfmiddlewaretoken = filter(lambda x: "csrfmiddlewaretoken" in x, data['content'].splitlines())[0].split('"')[-2]
        post = [
            ("username", CREDENTIALS["login"]),
            ("password", CREDENTIALS["password"]),
            ("region", "http://openstackserver:5000/v3"),
            ("auth_url", "http://openstackserver:5000/v3"),
            ("csrfmiddlewaretoken", csrfmiddlewaretoken)
        ]
        auth = get_url("/auth/login/", post_data=post, crsftoken=csrfmiddlewaretoken)

    def tearDown(self):
        get_url("/auth/logout/")

    def test_tenants(self):
        data = get_url("/pip/projects/")
        self.assertIsInstance(data, dict)
        self.assertIn("projects", data)
        self.assertIs(len(data["projects"]) > 0, True)
        for tenant in data["projects"]:
            self.assertIsInstance(tenant, dict)
            for key in [u'domain', u'managed', u'uuid', u'description', u'enabled', u'name']:
                self.assertIn(key, tenant)
            _data = get_url("/pip/projects/{}".format(tenant["uuid"]))
            self.assertIsInstance(_data, dict)
            self.assertIn("projects", _data)
            self.assertIs(len(_data["projects"]) == 1, True)
            for key in [u'domain', u'managed', u'uuid', u'description', u'enabled', u'name']:
                self.assertIn(key, _data["projects"][0])
            self.assertEqual(tenant["uuid"], _data["projects"][0]["uuid"])
        #Try creating one tenant
        tenant = {
            "name": "TestTenantForMoon",
            "description": "...",
            "enabled": True,
            "domain": "Default"
        }
        data = get_url("/pip/projects/", post_data=tenant)
        self.assertIsInstance(data, dict)
        self.assertIn("projects", data)
        self.assertIs(len(data["projects"]) > 0, True)
        tenant_names = map(lambda x: x["name"], data["projects"])
        self.assertIn(tenant["name"], tenant_names)
        for _tenant in data["projects"]:
            if _tenant["name"] == tenant["name"]:
                tenant["uuid"] = _tenant["uuid"]
        #Try destroying one tenant
        data = get_url("/pip/projects/"+tenant["uuid"]+"/", method="DELETE")
        tenant_names = map(lambda x: x["name"], data["projects"])
        self.assertNotIn(tenant["name"], tenant_names)

    def test_users(self):
        data = get_url("/pip/projects/")
        self.assertIsInstance(data, dict)
        self.assertIn("projects", data)
        self.assertIs(len(data["projects"]) > 0, True)
        for tenant in data["projects"]:
            data = get_url("/pip/projects/{}/users/".format(tenant["uuid"]))
            self.assertIsInstance(data, dict)
            self.assertIn("users", data)
            self.assertIs(len(data["users"]) > 0, True)
            for user in data["users"]:
                self.assertIsInstance(user, dict)
                for key in [u'domain', u'name', u'enabled', u'project', u'uuid']:
                    self.assertIn(key, user)

    def test_objects(self):
        data = get_url("/pip/projects/")
        self.assertIsInstance(data, dict)
        self.assertIn("projects", data)
        self.assertIs(len(data["projects"]) > 0, True)
        for tenant in data["projects"]:
            if tenant["name"] not in ("admin", "demo"):
                continue
            data = get_url("/pip/projects/{}/objects/".format(tenant["uuid"]))
            self.assertIsInstance(data, dict)
            self.assertIn("objects", data)
            for server in data["objects"]:
                self.assertIsInstance(server, dict)
                for key in [u'name', u'enabled', u'tenant', u'uuid']:
                    self.assertIn(key, server)

    def test_roles(self):
        data = get_url("/pip/projects/")
        self.assertIsInstance(data, dict)
        self.assertIn("projects", data)
        self.assertIs(len(data["projects"]) > 0, True)
        for tenant in data["projects"]:
            users = get_url("/pip/projects/{}/users/".format(tenant["uuid"]))
            self.assertIsInstance(users, dict)
            self.assertIn("users", users)
            self.assertIs(len(users["users"]) > 0, True)
            for user in users["users"]:
                roles = get_url("/pip/projects/{}/users/{}/roles/".format(tenant["uuid"], user["uuid"]))
                self.assertIsInstance(roles, dict)
                self.assertIn("roles", roles)
                if len(roles["roles"]) > 0:
                    # self.assertIs(len(roles["roles"]) > 0, True)
                    for role in roles["roles"]:
                        for key in [u'value', u'description', u'enabled', u'category', u'uuid']:
                            self.assertIn(key, role)

    # def test_groups(self):
    #     data = get_url("/pip/projects/")
    #     self.assertIsInstance(data, dict)
    #     self.assertIn("projects", data)
    #     self.assertIs(len(data["projects"]) > 0, True)
    #     for tenant in data["projects"]:
    #         users = get_url("/pip/projects/{}/users/".format(tenant["uuid"]))
    #         self.assertIsInstance(users, dict)
    #         self.assertIn("users", users)
    #         self.assertIs(len(users["users"]) > 0, True)
    #         for user in users["users"]:
    #             groups = get_url("/pip/projects/{}/groups/{}/".format(tenant["uuid"], user["uuid"]))
    #             self.assertIsInstance(groups, dict)
    #             self.assertIn("groups", groups)
    #             self.assertIs(len(groups["groups"]) > 0, True)
    #             for key in [u'value', u'description', u'enabled', u'category', u'uuid']:
    #                 self.assertIn(key, groups)

    def test_role_assignments(self):
        data = get_url("/pip/projects/")
        self.assertIsInstance(data, dict)
        self.assertIn("projects", data)
        self.assertIs(len(data["projects"]) > 0, True)
        for tenant in data["projects"]:
            users = get_url("/pip/projects/{}/users/".format(tenant["uuid"]))
            self.assertIsInstance(users, dict)
            self.assertIn("users", users)
            self.assertIs(len(users["users"]) > 0, True)
            for user in users["users"]:
                assignments = get_url("/pip/projects/{}/assignments/roles/{}/".format(tenant["uuid"], user["uuid"]))
                self.assertIsInstance(assignments, dict)
                self.assertIn("role_assignments", assignments)
                if len(assignments["role_assignments"]) > 0:
                    for assignment in assignments["role_assignments"]:
                        for key in [u'subject', u'attributes', u'category', u'description', u'uuid']:
                            self.assertIn(key, assignment)

    # def test_group_assignments(self):
    #     data = get_url("/pip/projects/")
    #     self.assertIsInstance(data, dict)
    #     self.assertIn("projects", data)
    #     self.assertIs(len(data["projects"]) > 0, True)
    #     for tenant in data["projects"]:
    #         users = get_url("/pip/projects/{}/users/".format(tenant["uuid"]))
    #         self.assertIsInstance(users, dict)
    #         self.assertIn("users", users)
    #         self.assertIs(len(users["users"]) > 0, True)
    #         for user in users["users"]:
    #             assignments = get_url("/pip/projects/{}/assignments/groups/{}/".format(tenant["uuid"], user["uuid"]))
    #             print(assignments)
    #             self.assertIsInstance(assignments, dict)
    #             self.assertIn("group_assignments", assignments)
    #             self.assertIs(len(assignments["group_assignments"]) > 0, True)
    #             for key in [u'object', u'attributes', u'enabled', u'category', u'description', u'uuid']:
    #                 self.assertIn(key, assignments)

    def test_image_name(self):
        data = get_url("/pip/nova/images/")
        self.assertIsInstance(data, dict)
        self.assertIn("images", data)
        self.assertIs(len(data["images"]) > 0, True)
        for image in data["images"]:
            self.assertIsInstance(image, dict)
            self.assertIn("name", image)
            self.assertIn("uuid", image)

    def test_flavor(self):
        data = get_url("/pip/nova/flavors/")
        self.assertIsInstance(data, dict)
        self.assertIn("flavors", data)
        self.assertIs(len(data["flavors"]) > 0, True)
        for flavor in data["flavors"]:
            self.assertIsInstance(flavor, dict)
            self.assertIn("name", flavor)
            self.assertIn("uuid", flavor)


if __name__ == '__main__':
    # moon_proc = start_moon_server()
    # try:
    unittest.main()
        # finally:
        #     stop_moon_server(moon_proc)