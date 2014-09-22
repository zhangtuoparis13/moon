import unittest
from moon import settings
import hashlib
import os
import uuid
import urllib2
import urllib
import re
import json
import time
from moon.core.pip import get_pip


MOON_SERVER_IP = {
    "HOST": "127.0.0.1",
    "PORT": "8080",
    "BASEURL": "",
    "URL": ""
}

CREDENTIALS = {
    "login": "admin",
    "password": "P4ssw0rd"
}


def get_url(url, post_data=None):
    MOON_SERVER_IP["URL"] = url
    url = "http://{HOST}:{PORT}/{BASEURL}{URL}".format(**MOON_SERVER_IP)
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'sessionid=wqvkwu2xb8ivlyhid441k0lbm7lwaedz'))
    if not post_data:
        result = opener.open(url)
    else:
        result = opener.open(url, urllib.urlencode(post_data))
    data = result.read()
    try:
        return json.loads(data)
    except ValueError:
        return str(data)


class TestAdminInterface(unittest.TestCase):

    def setUp(self):
        # data = get_url("auth/login/")
        # csrfmiddlewaretoken = filter(lambda x: "csrfmiddlewaretoken" in x, data.splitlines())[0].split('"')[-2]
        # print("csrfmiddlewaretoken="+csrfmiddlewaretoken)
        # post = [
        #     ("csrfmiddlewaretoken", csrfmiddlewaretoken),
        #     ("id_username", CREDENTIALS["login"]),
        #     ("id_password", CREDENTIALS["password"]),
        #     ("id_region", "http://openstackserver:5000/v3"),
        # ]
        # auth = get_url("auth/login/", post)
        # print(auth)
        self.pip = get_pip()

    def tearDown(self):
        pass

    def test_get_intra_extensions(self):
        data = get_url("json/intra-extensions/")
        self.assertIsInstance(data, list)
        for ext in data:
            _data = get_url("json/intra-extension/"+ext+"/")
            self.assertIsInstance(_data, dict)
            for k in [u'admin', u'authz', u'_id']:
                self.assertIn(k, _data.keys())
            for k in [u'perimeter', u'assignment', u'configuration', u'metadata']:
                self.assertIn(k, _data['admin'].keys())
            for k in [u'perimeter', u'assignment', u'configuration', u'metadata']:
                self.assertIn(k, _data['authz'].keys())
            self.assertIsInstance(_data["_id"], unicode)
            # print(json.dumps(_data, indent=4))

    def test_get_subjects(self):
        data = get_url("json/intra-extensions/")
        self.assertIsInstance(data, list)
        for ext in data:
            _data = get_url("json/intra-extension/"+ext+"/subjects/")
            self.assertIsInstance(_data, dict)
            self.assertIn("subjects", _data)
            self.assertIsInstance(_data["subjects"], list)

    def test_get_objects(self):
        data = get_url("json/intra-extensions/")
        self.assertIsInstance(data, list)
        for ext in data:
            _data = get_url("json/intra-extension/"+ext+"/objects/")
            self.assertIsInstance(_data, dict)
            self.assertIn("objects", _data)
            self.assertIsInstance(_data["objects"], list)


class TestPIPInterface(unittest.TestCase):

    def setUp(self):
        # self.pip = get_pip()
        pass

    def tearDown(self):
        pass

    def test_tenants(self):
        data = get_url("pip/tenants/")
        self.assertIsInstance(data, list)
        self.assertIs(len(data) > 0, True)
        tenant_names = list()
        for tenant in data:
            self.assertIsInstance(tenant, dict)

if __name__ == '__main__':
    unittest.main()