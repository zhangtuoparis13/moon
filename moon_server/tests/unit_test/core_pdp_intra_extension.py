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

"""
unit test for moon/core/pdp
"""

import unittest
import os.path
import pkg_resources
import copy
from moon_server.core.pdp.intra_extension import IntraExtension
from moon_server.tests.unit_test.samples.mls001.intra_extension import results, requests


class TestCorePDPIntraExtension(unittest.TestCase):

    def setUp(self):
        _sample = 'mls001'
        _sample_path = os.path.join('samples', _sample)
        intra_extension_setting_abs_dir = pkg_resources.resource_filename('moon', _sample_path)
        self.intra_extension = IntraExtension()
        self.intra_extension.load_from_json(intra_extension_setting_abs_dir)
        self._requests = requests
        self._results = results

    def tearDown(self):
        pass

    def test_get_uuid(self):
        #self.assertIsInstance(self.intra_extension.get_uuid(), UUID)
        print("[Get Uuid]---------------- OK ")

    def test_get_tenant_uuid(self):
        # self.assertIsInstance(self.intra_extension.get_tenant_uuid(), UUID)
        print("[Get Tenant Uuid]---------------- OK ")

    def test_authz(self):
        _genre = 'authz'
        for i in range(len(requests[_genre])):
            _sub = requests[_genre][i]['subject']
            _obj = requests[_genre][i]['object']
            _act = requests[_genre][i]['action']
            _result = requests[_genre][i]['_result']
            _description = requests[_genre][i]['_description']
            self.assertEqual(self.intra_extension.authz(_sub, _obj, _act), _result)
            print("[Authz] ", _description, " ---------------- OK")

    def test_admin(self):
        _genre = 'admin'
        for i in range(len(requests[_genre])):
            _sub = requests[_genre][i]['subject']
            _obj = requests[_genre][i]['object']
            _act = requests[_genre][i]['action']
            _result = requests[_genre][i]['_result']
            _description = requests[_genre][i]['_description']
            self.assertEqual(self.intra_extension.admin(_sub, _obj, _act), _result)
            print("[Admin] ", _description, " ---------------- OK")

    def test_create_destory_requesting_collaboration(self):
        for _type in ["trust", "coordinate"]:
            _vent_uuid = self._results[_type]["collaboration"]["requesting"]["vent_uuid"]
            _genre = self._results[_type]["collaboration"]["requesting"]["genre"]
            _subs = self._results[_type]["collaboration"]["requesting"]["subject_list"]
            _data = copy.deepcopy(self.intra_extension.get_data())
            _dict = self.intra_extension.create_requesting_collaboration(_genre, _subs, _vent_uuid, "read")
            self.assertIsInstance(_dict, dict)
            self.assertEqual(self.intra_extension.destroy_requesting_collaboration(_genre, _subs, _vent_uuid,
                                                                                   _dict["subject_category_value_dict"],
                                                                                   _dict["object_category_value_dict"]),
                             "[Destroy Requesting Collaboration] OK")
            self.assertEqual(self.intra_extension.get_data(), _data)

    def test_create_destory_requested_collaboration(self):
        for _type in ["trust", "coordinate"]:
            _vent_uuid = self._results[_type]["collaboration"]["requested"]["vent_uuid"]
            _genre = self._results[_type]["collaboration"]["requested"]["genre"]
            _objs = self._results[_type]["collaboration"]["requested"]["object_list"]
            _data = copy.deepcopy(self.intra_extension.get_data())
            _dict = self.intra_extension.create_requested_collaboration(_genre, _vent_uuid, _objs, "read")
            self.assertIsInstance(_dict, dict)
            self.assertEqual(self.intra_extension.destroy_requested_collaboration(_genre, _vent_uuid, _objs,
                                                                                  _dict["subject_category_value_dict"],
                                                                                  _dict["object_category_value_dict"]),
                             "[Destroy Requested Collaboration] OK")
            self.assertEqual(self.intra_extension.get_data(), _data)


"""
    def test_get_data(self):
        print("[test_get_data]----------------: ", self.intra_extension.get_data().keys())
        self.assertIsInstance(self.intra_extension.get_data(), dict)

    def test_set_data(self):
        _intra_extension = IntraExtension()
        intra_extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001')
        _intra_extension.load_from_json(intra_extension_setting_abs_dir)
        _data = _intra_extension.get_data()
        self.intra_extension.set_data(_data)
        print("[test_set_data]----------------: ", self.intra_extension.get_data().keys())
        self.assertIsInstance(self.intra_extension.get_data(), dict)

    def test_set_to_db_and_get_from_db(self):
        print("[test_set_to_db_and_get_from_db]----------------: ", self.intra_extension.get_data().keys())
        self.intra_extension.backup_intra_extension_to_db()
        self.intra_extension.get_intra_extension_from_db(self.intra_extension.get_uuid())
        print("[test_set_to_db_and_get_from_db]----------------: ", self.intra_extension.get_data().keys())

"""

if __name__ == "__main__":
    unittest.main()
