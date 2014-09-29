import unittest
import urllib
import json
from moon.core.pip import get_pip
import httplib


MOON_SERVER_IP = {
    "HOST": "127.0.0.1",
    "PORT": "8080",
    "BASEURL": "",
    "URL": ""
}

CREDENTIALS = {
    "login": "admin",
    "password": "P4ssw0rd",
    "Cookie": "wqvkwu2xb8ivlyhid441k0lbm7lwaedz"
}


def get_url(url, post_data=None, crsftoken=None, method="GET"):
    # MOON_SERVER_IP["URL"] = url
    # _url = "http://{HOST}:{PORT}".format(**MOON_SERVER_IP)
    if post_data:
        method = "POST"
    conn = httplib.HTTPConnection(MOON_SERVER_IP["HOST"], MOON_SERVER_IP["PORT"])
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain",
        'Cookie': 'sessionid={}'.format(CREDENTIALS["Cookie"]),
    }
    if post_data:
        conn.request(method, url, json.dumps(post_data), headers=headers)
    else:
        conn.request(method, url, headers=headers)
    resp = conn.getresponse()
    content = resp.read()
    conn.close()

    try:
        return json.loads(content)
    except ValueError:
        return str(content)


class TestAdminInterface_IntraExtension(unittest.TestCase):

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
        self.pip = get_pip()

    def tearDown(self):
        pass

    def test_intra_extensions(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extension/"+ext+"/")
            self.assertIsInstance(_data, dict)
            for k in [u'admin', u'authz', u'_id']:
                self.assertIn(k, _data["intra_extension"].keys())
            for k in [u'perimeter', u'assignment', u'configuration', u'metadata']:
                self.assertIn(k, _data["intra_extension"]['admin'].keys())
            for k in [u'perimeter', u'assignment', u'configuration', u'metadata']:
                self.assertIn(k, _data["intra_extension"]['authz'].keys())
            self.assertIsInstance(_data["intra_extension"]["_id"], unicode)
            # print(json.dumps(_data, indent=4))
        #TODO: add an intra-extension
        #TODO: delete an intra-extension

    def test_subjects(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extension/"+ext+"/subjects/")
            self.assertIsInstance(_data, dict)
            self.assertIn("subjects", _data)
            self.assertIsInstance(_data["subjects"], list)
            self.assertEqual(len(_data["subjects"]) > 0, True)

    def test_objects(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extension/"+ext+"/objects/")
            self.assertIsInstance(_data, dict)
            self.assertIn("objects", _data)
            self.assertIsInstance(_data["objects"], list)
            self.assertEqual(len(_data["objects"]) > 0, True)

    def test_subject(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extension/"+ext+"/subject/", post_data={"subject_uuid": "test_subject"})
            self.assertIsInstance(_data, dict)
            self.assertIn("subjects", _data)
            self.assertIsInstance(_data["subjects"], list)
            self.assertEqual(len(_data["subjects"]) > 0, True)
            self.assertIn("test_subject", _data["subjects"])
            _data = get_url("/json/intra-extension/"+ext+"/subject/test_subject/", method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("subjects", _data)
            self.assertIsInstance(_data["subjects"], list)
            self.assertEqual(len(_data["subjects"]) > 0, True)
            self.assertNotIn("test_subject", _data["subjects"])

    def test_object(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extension/"+ext+"/object/", post_data={"object_uuid": "test_object"})
            self.assertIsInstance(_data, dict)
            self.assertIn("objects", _data)
            self.assertIsInstance(_data["objects"], list)
            self.assertEqual(len(_data["objects"]) > 0, True)
            self.assertIn("test_object", _data["objects"])
            _data = get_url("/json/intra-extension/"+ext+"/object/test_object/", method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("objects", _data)
            self.assertIsInstance(_data["objects"], list)
            self.assertEqual(len(_data["objects"]) > 0, True)
            self.assertNotIn("test_object", _data["objects"])

    def test_subject_categories(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extension/"+ext+"/subject_categories/")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_categories", _data)
            self.assertIsInstance(_data["subject_categories"], list)
            self.assertEqual(len(_data["subject_categories"]) > 0, True)

    def test_object_categories(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extension/"+ext+"/object_categories/")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_categories", _data)
            self.assertIsInstance(_data["object_categories"], list)
            self.assertEqual(len(_data["object_categories"]) > 0, True)

    def test_subject_category(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extension/"+ext+"/subject_category/", post_data={"category_id": "my_category"})
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_categories", _data)
            self.assertIsInstance(_data["subject_categories"], list)
            self.assertEqual(len(_data["subject_categories"]) > 0, True)
            self.assertIn("my_category", _data["subject_categories"])
            _data = get_url("/json/intra-extension/"+ext+"/subject_category/my_category/", method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_categories", _data)
            self.assertIsInstance(_data["subject_categories"], list)
            self.assertEqual(len(_data["subject_categories"]) > 0, True)
            self.assertNotIn("my_category", _data["subject_categories"])

    def test_object_category(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extension/"+ext+"/object_category/", post_data={"category_id": "my_category"})
            self.assertIsInstance(_data, dict)
            self.assertIn("object_categories", _data)
            self.assertIsInstance(_data["object_categories"], list)
            self.assertEqual(len(_data["object_categories"]) > 0, True)
            self.assertIn("my_category", _data["object_categories"])
            _data = get_url("/json/intra-extension/"+ext+"/object_category/my_category/", method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_categories", _data)
            self.assertIsInstance(_data["object_categories"], list)
            self.assertEqual(len(_data["object_categories"]) > 0, True)
            self.assertNotIn("my_category", _data["object_categories"])

    def test_subject_category_values(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            categories = get_url("/json/intra-extension/"+ext+"/subject_categories/")
            _data = get_url("/json/intra-extension/"+ext+"/subject_category_values/")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_category_values", _data)
            self.assertIsInstance(_data["subject_category_values"], dict)
            for key in _data["subject_category_values"]:
                self.assertIsInstance(_data["subject_category_values"][key], list)
                self.assertIn(key, categories["subject_categories"])

    def test_subject_category_value(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extension/"+ext+"/subject_category_values/")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_category_values", _data)
            self.assertIsInstance(_data["subject_category_values"], dict)
            for val in [u'high', u'medium', u'low']:
                self.assertIn(val, _data["subject_category_values"]["subject_security_level"])
            _data = get_url("/json/intra-extension/"+ext+"/subject_category_value/",
                            post_data={"category_id": "subject_security_level", "value": "ultra-low1"})
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_category_values", _data)
            self.assertIsInstance(_data["subject_category_values"], dict)
            for val in [u'high', u'medium', u'low', u"ultra-low1"]:
                self.assertIn(val, _data["subject_category_values"]["subject_security_level"])
            _data = get_url("/json/intra-extension/"+ext+"/subject_category_value/subject_security_level/ultra-low1",
                            method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_category_values", _data)
            self.assertIsInstance(_data["subject_category_values"], dict)
            for val in [u'high', u'medium', u'low']:
                self.assertIn(val, _data["subject_category_values"]["subject_security_level"])
            self.assertNotIn(u"ultra-low1", _data["subject_category_values"]["subject_security_level"])

    def test_object_category_values(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            categories = get_url("/json/intra-extension/"+ext+"/object_categories/")
            _data = get_url("/json/intra-extension/"+ext+"/object_category_values/")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_category_values", _data)
            self.assertIsInstance(_data["object_category_values"], dict)
            for key in _data["object_category_values"]:
                self.assertIsInstance(_data["object_category_values"][key], list)
                self.assertIn(key, categories["object_categories"])

    def test_object_category_value(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extension/"+ext+"/object_category_values/")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_category_values", _data)
            self.assertIsInstance(_data["object_category_values"], dict)
            for val in [u'high', u'medium', u'low']:
                self.assertIn(val, _data["object_category_values"]["object_security_level"])
            _data = get_url("/json/intra-extension/"+ext+"/object_category_value/",
                            post_data={"category_id": "object_security_level", "value": "ultra-low"})
            self.assertIsInstance(_data, dict)
            self.assertIn("object_category_values", _data)
            self.assertIsInstance(_data["object_category_values"], dict)
            for val in [u'high', u'medium', u'low', u"ultra-low"]:
                self.assertIn(val, _data["object_category_values"]["object_security_level"])
            _data = get_url("/json/intra-extension/"+ext+"/object_category_value/object_security_level/ultra-low",
                            method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_category_values", _data)
            self.assertIsInstance(_data["object_category_values"], dict)
            for val in [u'high', u'medium', u'low']:
                self.assertIn(val, _data["object_category_values"]["object_security_level"])
            self.assertNotIn(u"ultra-low", _data["object_category_values"]["object_security_level"])

    def test_subject_assignments(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            categories = get_url("/json/intra-extension/"+ext+"/subject_categories/")
            _data = get_url("/json/intra-extension/"+ext+"/subject_assignments/")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_assignments", _data)
            self.assertIsInstance(_data["subject_assignments"], dict)
            for key in _data["subject_assignments"]:
                self.assertIsInstance(_data["subject_assignments"][key], dict)
                self.assertIn(key, categories["subject_categories"])

    def test_subject_assignment(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            user = get_url("/json/intra-extension/"+ext+"/subjects/")["subjects"][0]
            #Add a new subject category value for the test
            _data = get_url("/json/intra-extension/"+ext+"/subject_category_value/",
                            post_data={"category_id": "subject_security_level", "value": "ultra-low2"})
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_category_values", _data)
            self.assertIsInstance(_data["subject_category_values"], dict)
            for val in [u'high', u'medium', u'low', u"ultra-low2"]:
                self.assertIn(val, _data["subject_category_values"]["subject_security_level"])
            _data = get_url("/json/intra-extension/"+ext+"/subject_assignments/")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_assignments", _data)
            self.assertIsInstance(_data["subject_assignments"], dict)
            for cat in get_url("/json/intra-extension/"+ext+"/subject_categories/")["subject_categories"]:
                for val in get_url("/json/intra-extension/"+ext+"/subjects/")["subjects"]:
                    self.assertIn(val, _data['subject_assignments'][cat].keys())
            #Add now a new assignment
            _data = get_url("/json/intra-extension/"+ext+"/subject_assignment/",
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
                "/json/intra-extension/"+ext+"/subject_assignment/subject_security_level/"+user+"/ultra-low2/",
                method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("subject_assignments", _data)
            self.assertIsInstance(_data["subject_assignments"], dict)
            self.assertIn("subject_security_level", _data["subject_assignments"])
            self.assertIsInstance(_data["subject_assignments"]["subject_security_level"], dict)
            self.assertIn(user, _data["subject_assignments"]["subject_security_level"])
            self.assertIsInstance(_data["subject_assignments"]["subject_security_level"][user], list)
            self.assertNotIn("ultra-low2", _data["subject_assignments"]["subject_security_level"][user])

    def test_object_assignments(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            categories = get_url("/json/intra-extension/"+ext+"/object_categories/")
            _data = get_url("/json/intra-extension/"+ext+"/object_assignments/")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_assignments", _data)
            self.assertIsInstance(_data["object_assignments"], dict)
            for key in _data["object_assignments"]:
                self.assertIsInstance(_data["object_assignments"][key], dict)
                self.assertIn(key, categories["object_categories"])

    def test_object_assignment(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            user = get_url("/json/intra-extension/"+ext+"/objects/")["objects"][0]
            #Add a new object category value for the test
            _data = get_url("/json/intra-extension/"+ext+"/object_category_value/",
                            post_data={"category_id": "object_security_level", "value": "ultra-low2"})
            self.assertIsInstance(_data, dict)
            self.assertIn("object_category_values", _data)
            self.assertIsInstance(_data["object_category_values"], dict)
            for val in [u'high', u'medium', u'low', u"ultra-low2"]:
                self.assertIn(val, _data["object_category_values"]["object_security_level"])
            _data = get_url("/json/intra-extension/"+ext+"/object_assignments/")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_assignments", _data)
            self.assertIsInstance(_data["object_assignments"], dict)
            for cat in get_url("/json/intra-extension/"+ext+"/object_categories/")["object_categories"]:
                for val in get_url("/json/intra-extension/"+ext+"/objects/")["objects"]:
                    self.assertIn(val, _data['object_assignments'][cat].keys())
            #Add now a new assignment
            _data = get_url("/json/intra-extension/"+ext+"/object_assignment/",
                            post_data={
                                "category_id": "object_security_level",
                                "value": "ultra-low2",
                                "object_id": user
                            })
            self.assertIsInstance(_data, dict)
            self.assertIn("object_assignments", _data)
            self.assertIsInstance(_data["object_assignments"], dict)
            self.assertIn("object_security_level", _data["object_assignments"])
            self.assertIsInstance(_data["object_assignments"]["object_security_level"], dict)
            self.assertIn(user, _data["object_assignments"]["object_security_level"])
            self.assertIsInstance(_data["object_assignments"]["object_security_level"][user], list)
            self.assertIn("ultra-low2", _data["object_assignments"]["object_security_level"][user])
            #Delete the last assignment
            _data = get_url(
                "/json/intra-extension/"+ext+"/object_assignment/object_security_level/"+user+"/ultra-low2/",
                method="DELETE")
            self.assertIsInstance(_data, dict)
            self.assertIn("object_assignments", _data)
            self.assertIsInstance(_data["object_assignments"], dict)
            self.assertIn("object_security_level", _data["object_assignments"])
            self.assertIsInstance(_data["object_assignments"]["object_security_level"], dict)
            self.assertIn(user, _data["object_assignments"]["object_security_level"])
            self.assertIsInstance(_data["object_assignments"]["object_security_level"][user], list)
            self.assertNotIn("ultra-low2", _data["object_assignments"]["object_security_level"][user])

    def test_rules(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extension/"+ext+"/rules/")
            self.assertIsInstance(_data, dict)
            self.assertIn("rules", _data)
            self.assertIsInstance(_data["rules"], list)

    def test_rule(self):
        data = get_url("/json/intra-extensions/")
        self.assertIsInstance(data, dict)
        for ext in data["intra_extensions"]:
            _data = get_url("/json/intra-extension/"+ext+"/rules/")
            self.assertIsInstance(_data, dict)
            self.assertIn("rules", _data)
            self.assertIsInstance(_data["rules"], list)
            _data = get_url("/json/intra-extension/"+ext+"/rule/",
                            post_data={
                                "relation_super": {
                                    "sub_cat_value": {"subject_security_level": "high"},
                                    "obj_cat_value": {"object_security_level": "low", "action": "write"}
                                }
                            }
            )
            self.assertIsInstance(_data, dict)
            self.assertIn("rules", _data)
            self.assertIsInstance(_data["rules"], dict)
            self.assertNotIn(_data["rules"], ["high", "write", "low"])
            # _data = get_url("/json/intra-extension/"+ext+"/rule/",
            #                 post_data={
            #                     "sub_cat_value": {"subject_security_level": "high"},
            #                     "obj_cat_value": {"object_security_level": "low", "action": "write"}
            #                 }
            # )
            # self.assertIsInstance(_data, dict)
            # self.assertIn("rules", _data)
            # self.assertIsInstance(_data["rules"], list)
            # self.assertNotIn(_data["rules"], ["high", "write", "low"])


class TestAdminInterface_InterExtension(unittest.TestCase):

    def setUp(self):
        self.pip = get_pip()

    def tearDown(self):
        pass

    def test_inter_extensions(self):
        data = get_url("/json/inter-extensions/")
        extensions = get_url("/json/intra-extensions/")
        self.assertIs(len(extensions["intra_extensions"]) >= 2, True)
        self.assertIsInstance(data, dict)
        self.assertIs(len(data["inter_extensions"]) == 0, True)
        subjects_1 = get_url("/json/intra-extension/{}/subjects".format(extensions["intra_extensions"][0]))
        objects_2 = get_url("/json/intra-extension/{}/objects".format(extensions["intra_extensions"][1]))
        data = get_url(
            "/json/inter-extension/",
            post_data={
                "requesting_intra_extension_uuid": extensions["intra_extensions"][0],
                "requested_intra_extension_uuid": extensions["intra_extensions"][1],
                "genre": "trust",
                "sub_list": subjects_1,
                "obj_list": objects_2,
                "act": "write"
            })
        self.assertIsInstance(data, dict)
        self.assertIn('inter_extensions', data)
        self.assertIs(len(data["inter_extensions"]) > 0, True)
        # for ext in data["inter_extensions"]:
        #     _data = get_url("/json/inter-extension/"+ext+"/")
        #     self.assertIsInstance(_data, list)
        #     # for k in [u'admin', u'authz', u'_id']:
        #     #     self.assertIn(k, _data.keys())
        #     # for k in [u'perimeter', u'assignment', u'configuration', u'metadata']:
        #     #     self.assertIn(k, _data['admin'].keys())
        #     # for k in [u'perimeter', u'assignment', u'configuration', u'metadata']:
        #     #     self.assertIn(k, _data['authz'].keys())
        #     # self.assertIsInstance(_data["_id"], unicode)
        #     print(json.dumps(_data, indent=4))


class TestPIPInterface(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

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
            data = get_url("/pip/projects/{}/objects/".format(tenant["uuid"]))
            self.assertIsInstance(data, dict)
            self.assertIn("objects", data)
            print(data)
            for server in data["objects"]:
                self.assertIsInstance(server, dict)
                for key in [u'domain', u'name', u'enabled', u'project', u'uuid']:
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
                roles = get_url("/pip/projects/{}/roles/{}/".format(tenant["uuid"], user["uuid"]))
                self.assertIsInstance(roles, dict)
                self.assertIn("roles", roles)
                self.assertIs(len(roles["roles"]) > 0, True)
                for key in [u'value', u'description', u'enabled', u'category', u'uuid']:
                    self.assertIn(key, roles)

    def test_groups(self):
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
                groups = get_url("/pip/projects/{}/groups/{}/".format(tenant["uuid"], user["uuid"]))
                self.assertIsInstance(groups, dict)
                self.assertIn("groups", groups)
                self.assertIs(len(groups["groups"]) > 0, True)
                for key in [u'value', u'description', u'enabled', u'category', u'uuid']:
                    self.assertIn(key, groups)

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
                self.assertIs(len(assignments["role_assignments"]) > 0, True)
                for key in [u'subject', u'attributes', u'enabled', u'category', u'description', u'uuid']:
                    self.assertIn(key, assignments)

    def test_group_assignments(self):
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
                assignments = get_url("/pip/projects/{}/assignments/groups/{}/".format(tenant["uuid"], user["uuid"]))
                self.assertIsInstance(assignments, dict)
                self.assertIn("group_assignments", assignments)
                self.assertIs(len(assignments["group_assignments"]) > 0, True)
                for key in [u'object', u'attributes', u'enabled', u'category', u'description', u'uuid']:
                    self.assertIn(key, assignments)


if __name__ == '__main__':
    unittest.main()