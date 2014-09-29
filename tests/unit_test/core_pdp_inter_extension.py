"""
unit test for moon/core/pdp
"""

import unittest
import pkg_resources
import os.path
import uuid
from moon.core.pdp.intra_extension import IntraExtension
from moon.core.pdp.inter_extension import InterExtension
from moon.tests.unit_test.samples.mls001.inter_extension import results


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

if __name__ == "__main__":
    unittest.main()

