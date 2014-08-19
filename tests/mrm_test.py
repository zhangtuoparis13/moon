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


def start_server():
    pid = os.fork()
    if pid == 0:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moon.gi.settings")
        from django.core.management import execute_from_command_line
        d_args = ["{}.py".format(__name__), "runserver", "127.0.0.1:8080"]
        execute_from_command_line(d_args)

start_server()
time.sleep(5)

MOON_SERVER_IP = {
    "HOST": "127.0.0.1",
    "PORT": "8080",
    "BASEURL": "mrm"
}


class TestMRMFunctions(unittest.TestCase):

    def setUp(self):
        self.pip = get_pip(standalone=True)

    def tearDown(self):
        pass

    def test_connection_security(self):
        password = "bad password"
        url = "http://{HOST}:{PORT}/{BASEURL}/tenants".format(**MOON_SERVER_IP)
        key = uuid.uuid4()
        crypt_key = hashlib.sha256()
        crypt_key.update(str(key))
        crypt_key.update(password)
        post_data = [
            ('Object', ""),
            ('ObjectType', ""),
            ('Subject', ""),
            ('Action', ""),
            ('Subject_Tenant', ""),
            ('Object_Tenant', ""),
            ('RAW_PATH_INFO', ""),
            ('key', key)]
        result = urllib2.urlopen(url, urllib.urlencode(post_data))
        content = json.loads(result.read())
        print(content["key"])
        print(str(crypt_key))