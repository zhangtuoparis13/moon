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
import pkg_resources
import os.path
import uuid
from moon_server.core.pdp.intra_extension import IntraExtension
from moon_server.core.pdp.inter_extension import InterExtension
from moon_server.tests.unit_test.samples.mls001.inter_extension import results


class TestCorePDPInterExtension(unittest.TestCase):

    def setUp(self):
        _sample = 'mls001'
        _sample_path = os.path.join('samples', _sample)
        intra_extension_setting_abs_dir = pkg_resources.resource_filename('moon', _sample_path)
        self.requesting_intra_extension = IntraExtension()
        self.requested_intra_extension = IntraExtension()
        self.requesting_intra_extension.load_from_json(intra_extension_setting_abs_dir)
        self.requested_intra_extension.load_from_json(intra_extension_setting_abs_dir)
        self.inter_extension = InterExtension(self.requesting_intra_extension, self.requested_intra_extension)
        self._results = results

    def tearDown(self):
        pass

    def test_create_destroy_collaboration(self):
        for _genre in ["trust"]:
            _sub_list = self._results[_genre]["subject_list"]
            _obj_list = self._results[_genre]["object_list"]
            _act = self._results[_genre]["action"]
            _vent_uuid = self.inter_extension.create_collaboration(_genre, _sub_list, _obj_list, _act)
            self.assertIsInstance(_vent_uuid, str)
            self.assertEqual(len(_vent_uuid), 36)  # check uuid length
            for _request in self._results[_genre]["requests"]:
                self.assertEqual(self.inter_extension.authz(_request["subject"],
                                                            _request["object"],
                                                            _request["action"]),
                                 _request["result"])
            self.assertEqual(self.inter_extension.destroy_collaboration(_genre, _vent_uuid),
                             "[InterExtension] Destroy Collaboration: OK")

        for _genre in ["coordinate"]:
            _sub_list = self._results[_genre]["subject_list"]
            _obj_list = self._results[_genre]["object_list"]
            _act = self._results[_genre]["action"]
            _vent_uuid = self.inter_extension.create_collaboration(_genre, _sub_list, _obj_list, _act)
            self.assertIsInstance(_vent_uuid, str)
            self.assertEqual(len(_vent_uuid), 36)  # check uuid length
            for _request in self._results[_genre]["requests"]:
                self.assertEqual(self.inter_extension.admin(_request["subject"],
                                                            _request["object"],
                                                            _request["action"]),
                                 _request["result"])
            self.assertEqual(self.inter_extension.destroy_collaboration(_genre, _vent_uuid),
                             "[InterExtension] Destroy Collaboration: OK")

    def test_delegate_collaboration(self):
        _sub = results["delegate_collaboration_admin"]["before"]['subject']
        _obj = results["delegate_collaboration_admin"]["before"]['object']
        _act = results["delegate_collaboration_admin"]["before"]['action']
        _result = results["delegate_collaboration_admin"]["before"]['_result']
        _description = results["delegate_collaboration_admin"]["before"]['_description']
        self.assertEqual(self.inter_extension.admin(_sub, _obj, _act), _result)
        print("[InterExtension] Delegate Collaboration Privilege Before: ", _description)

        for i in range(len(results["delegate_collaboration_privilege"])):
            _delegator_id = results["delegate_collaboration_privilege"][i]['delegator_id']
            _privilege = results["delegate_collaboration_privilege"][i]['privilege']
            _result = results["delegate_collaboration_privilege"][i]['_result']
            self.assertEqual(self.inter_extension.delegate(_delegator_id, _privilege), _result)
            print("[InterExtension] Delegate Collaboration Privilege ---------------- OK")

        _sub = results["delegate_collaboration_admin"]["after"]['subject']
        _obj = results["delegate_collaboration_admin"]["after"]['object']
        _act = results["delegate_collaboration_admin"]["after"]['action']
        _result = results["delegate_collaboration_admin"]["after"]['_result']
        _description = results["delegate_collaboration_admin"]["after"]['_description']
        self.assertEqual(self.inter_extension.admin(_sub, _obj, _act), _result)
        print("[InterExtension] Delegate Collaboration Privilege after: ", _description)

if __name__ == "__main__":
    unittest.main()

