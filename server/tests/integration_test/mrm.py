import unittest
import json
from moon.core.pip import get_pip
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
    "Cookie": "i6l4ihmo5ti07au6jx09wsq0uievgews"
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
        return {"content": content}


def send_authz(authz):
    conn = httplib.HTTPConnection(MOON_SERVER_IP["HOST"], MOON_SERVER_IP["PORT"])
    method = "POST"
    url = "/mrm/authz"
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain",
    }
    conn.request(method, url, json.dumps(authz), headers=headers)
    resp = conn.getresponse()
    content = resp.read()
    conn.close()
    try:
        return json.loads(content)
    except ValueError:
        return {"content": content}


class TestMRMInterface(unittest.TestCase):

    def setUp(self):
        # data = get_url("auth/login/", crsftoken=True)
        # csrfmiddlewaretoken = filter(lambda x: "csrfmiddlewaretoken" in x, data.splitlines())[0].split('"')[-2]
        # post = [
        #     ("csrfmiddlewaretoken", csrfmiddlewaretoken),
        #     ("username", CREDENTIALS["login"]),
        #     ("password", CREDENTIALS["password"]),
        #     ("region", "http://openstackserver:5000/v3"),
        #     ("auth_url", "http://openstackserver:5000/v3"),
        # ]
        # auth = get_url("auth/login/", post)
        # print("\033[41m----------------------------")
        # print(auth)
        # print("----------------------------\033[m")
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
        #Get user
        self.users_1 = get_url("/json/intra-extensions/{}/subjects".format(self.new_ext1_uuid))["subjects"]
        self.servers_1 = get_url("/json/intra-extensions/{}/objects".format(self.new_ext1_uuid))["objects"]
        self.users_2 = get_url("/json/intra-extensions/{}/subjects".format(self.new_ext2_uuid))["subjects"]
        self.servers_2 = get_url("/json/intra-extensions/{}/objects".format(self.new_ext2_uuid))["objects"]
        #Add assignment for first user and first server
        assign = get_url(
            "/json/intra-extensions/{}/subject_assignments".format(self.new_ext1_uuid),
            post_data={
                "subject_id": self.users_1[0],
                "category_id": "subject_security_level",
                "value": "high"
            }
        )["subject_assignments"]
        assign = get_url(
            "/json/intra-extensions/{}/object_assignments".format(self.new_ext1_uuid),
            post_data={
                "subject_id": self.servers_1[0],
                "category_id": "object_security_level",
                "value": "medium"
            }
        )["object_assignments"]
        assign = get_url(
            "/json/intra-extensions/{}/object_assignments".format(self.new_ext1_uuid),
            post_data={
                "subject_id": self.servers_1[0],
                "category_id": "action",
                "value": "read"
            }
        )["object_assignments"]

    def tearDown(self):
        get_url("/json/intra-extensions/"+self.new_ext1_uuid+"/", method="DELETE")
        get_url("/json/intra-extensions/"+self.new_ext2_uuid+"/", method="DELETE")

    def test_read_object(self):
        authz_request = {
            'requesting_tenant': self.tenant_admin,
            'requested_tenant': self.tenant_admin,
            'subject': self.users_1[0],
            'object': self.servers_1[0],
            'action': "read",
            "key": str(uuid4())
        }
        authz = send_authz(authz_request)
        self.assertIsInstance(authz, dict)
        self.assertIn("authz", authz)
        self.assertNotIn("error", authz)
        self.assertEqual(authz["authz"], "KO")
        #Adding a new assignment for the first user
        _data = get_url(
            "/json/intra-extensions/"+self.new_ext1_uuid+"/subject_assignments/",
            post_data={
                "category_id": "subject_security_level",
                "value": "high",
                "subject_id": self.users_1[0]
            })
        self.assertIsInstance(_data, dict)
        self.assertIn("subject_assignments", _data)
        self.assertIsInstance(_data["subject_assignments"], dict)
        self.assertIn("subject_security_level", _data["subject_assignments"])
        self.assertIsInstance(_data["subject_assignments"]["subject_security_level"], dict)
        self.assertIn(self.users_1[0], _data["subject_assignments"]["subject_security_level"])
        self.assertIsInstance(_data["subject_assignments"]["subject_security_level"][self.users_1[0]], list)
        self.assertIn("high", _data["subject_assignments"]["subject_security_level"][self.users_1[0]])
        #Adding a new assignments for the first object
        _data = get_url(
            "/json/intra-extensions/"+self.new_ext1_uuid+"/object_assignments/",
            post_data={
                "category_id": "object_security_level",
                "value": "medium",
                "object_id": self.servers_1[0]
            })
        self.assertIsInstance(_data, dict)
        self.assertIn("object_assignments", _data)
        self.assertIsInstance(_data["object_assignments"], dict)
        self.assertIn("object_security_level", _data["object_assignments"])
        self.assertIsInstance(_data["object_assignments"]["object_security_level"], dict)
        self.assertIn(self.servers_1[0], _data["object_assignments"]["object_security_level"])
        self.assertIsInstance(_data["object_assignments"]["object_security_level"][self.servers_1[0]], list)
        self.assertIn("medium", _data["object_assignments"]["object_security_level"][self.servers_1[0]])
        _data = get_url(
            "/json/intra-extensions/"+self.new_ext1_uuid+"/object_assignments/",
            post_data={
                "category_id": "action",
                "value": "read",
                "object_id": self.servers_1[0]
            })
        self.assertIsInstance(_data, dict)
        self.assertIn("object_assignments", _data)
        self.assertIsInstance(_data["object_assignments"], dict)
        self.assertIn("action", _data["object_assignments"])
        self.assertIsInstance(_data["object_assignments"]["action"], dict)
        self.assertIn(self.servers_1[0], _data["object_assignments"]["action"])
        self.assertIsInstance(_data["object_assignments"]["action"][self.servers_1[0]], list)
        self.assertIn("read", _data["object_assignments"]["action"][self.servers_1[0]])
        #Re-testing the authorization
        authz = send_authz(authz_request)
        self.assertIsInstance(authz, dict)
        self.assertIn("authz", authz)
        self.assertNotIn("error", authz)
        self.assertEqual(authz["authz"], "OK")
        #Testing with write access
        authz_request = {
            'requesting_tenant': self.tenant_admin,
            'requested_tenant': self.tenant_admin,
            'subject': self.users_1[0],
            'object': self.servers_1[0],
            'action': "write",
            "key": str(uuid4())
        }
        authz = send_authz(authz_request)
        self.assertIsInstance(authz, dict)
        self.assertIn("authz", authz)
        self.assertNotIn("error", authz)
        self.assertEqual(authz["authz"], "KO")
        #Adding write access
        _data = get_url(
            "/json/intra-extensions/"+self.new_ext1_uuid+"/object_assignments/",
            post_data={
                "category_id": "action",
                "value": "write",
                "object_id": self.servers_1[0]
            })
        self.assertIsInstance(_data, dict)
        self.assertIn("object_assignments", _data)
        self.assertIsInstance(_data["object_assignments"], dict)
        self.assertIn("action", _data["object_assignments"])
        self.assertIsInstance(_data["object_assignments"]["action"], dict)
        self.assertIn(self.servers_1[0], _data["object_assignments"]["action"])
        self.assertIsInstance(_data["object_assignments"]["action"][self.servers_1[0]], list)
        self.assertIn("read", _data["object_assignments"]["action"][self.servers_1[0]])
        rule = {
            "sub_cat_value":
                {"relation_super": {"subject_security_level": "high"}},
            "obj_cat_value":
                {"relation_super": {"object_security_level": "medium", "action": "write"}}
        }
        _data = get_url("/json/intra-extensions/"+self.new_ext1_uuid+"/rules/",
                        post_data=rule)
        #Re-testing the authorization
        authz = send_authz(authz_request)
        self.assertIsInstance(authz, dict)
        self.assertIn("authz", authz)
        self.assertNotIn("error", authz)
        self.assertEqual(authz["authz"], "OK")
        #Testing with unknown action
        authz_request = {
            'requesting_tenant': self.tenant_admin,
            'requested_tenant': self.tenant_admin,
            'subject': self.users_1[0],
            'object': self.servers_1[0],
            'action': "something",
            "key": str(uuid4())
        }
        authz = send_authz(authz_request)
        self.assertIsInstance(authz, dict)
        self.assertIn("authz", authz)
        self.assertNotIn("error", authz)
        self.assertEqual(authz["authz"], "KO")
