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
        return {"content": content}


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
        user = {
            "name": "TestUser",
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
            _data = get_url("/json/intra-extension/"+ext+"/subject/", post_data=user)
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
            _data = get_url("/json/intra-extension/"+ext+"/subject/"+user_uuid+"/", method="DELETE")
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
        new_ext = get_url("/json/intra-extension/", post_data={"policymodel": my_policy})
        self.assertIsInstance(new_ext, dict)
        new_ext_uuid = new_ext["intra_extensions"][-1]
        tenants = get_url("/pip/projects/")
        self.assertIsInstance(tenants, dict)
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
        _data = get_url("/json/intra-extension/"+new_ext_uuid+"/object/"+new_vm["uuid"]+"/", method="DELETE")
        objects = get_url("/pip/projects/{}/objects/".format(tenant_admin))
        self.assertIsInstance(objects, dict)
        self.assertNotIn(new_vm["uuid"], map(lambda x: x["uuid"], objects["objects"]))
        self.assertNotIn(new_vm["uuid"], _data["objects"])

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
            # for cat in get_url("/json/intra-extension/"+ext+"/subject_categories/")["subject_categories"]:
            #     for val in get_url("/json/intra-extension/"+ext+"/subjects/")["subjects"]:
            #         self.assertIn(val, _data['subject_assignments'][cat].keys())
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
            # for cat in get_url("/json/intra-extension/"+ext+"/object_categories/")["object_categories"]:
            #     for val in get_url("/json/intra-extension/"+ext+"/objects/")["objects"]:
            #         self.assertIn(val, _data['object_assignments'][cat].keys())
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
            _data = get_url("/json/intra-extension/"+ext+"/rule/",
                            delete_data={
                                "relation_super": {
                                    "sub_cat_value": {"subject_security_level": "high"},
                                    "obj_cat_value": {"object_security_level": "low", "action": "write"}
                                }
                            }
            )
            self.assertIsInstance(_data, dict)
            self.assertIn("rules", _data)
            self.assertIsInstance(_data["rules"], dict)
            self.assertIsInstance(_data["rules"]["relation_super"], list)
            self.assertNotIn(_data["rules"]["relation_super"], ["high", "write", "low"])


# class TestAdminInterface_InterExtension(unittest.TestCase):
#
#     def setUp(self):
#         self.pip = get_pip()
#
#     def tearDown(self):
#         pass
#
#     def test_inter_extensions(self):
#         data = get_url("/json/inter-extensions/")
#         extensions = get_url("/json/intra-extensions/")
#         self.assertIs(len(extensions["intra_extensions"]) >= 2, True)
#         self.assertIsInstance(data, dict)
#         self.assertIs(len(data["inter_extensions"]) == 0, True)
#         subjects_1 = get_url("/json/intra-extension/{}/subjects".format(extensions["intra_extensions"][0]))
#         objects_2 = get_url("/json/intra-extension/{}/objects".format(extensions["intra_extensions"][1]))
#         data = get_url(
#             "/json/inter-extension/",
#             post_data={
#                 "requesting_intra_extension_uuid": extensions["intra_extensions"][0],
#                 "requested_intra_extension_uuid": extensions["intra_extensions"][1],
#                 "genre": "trust",
#                 "sub_list": subjects_1,
#                 "obj_list": objects_2,
#                 "act": "write"
#             })
#         self.assertIsInstance(data, dict)
#         self.assertIn('inter_extensions', data)
#         self.assertIs(len(data["inter_extensions"]) > 0, True)
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
#
#
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
                    for assignment in assignments:
                        for key in [u'subject', u'attributes', u'enabled', u'category', u'description', u'uuid']:
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
    unittest.main()