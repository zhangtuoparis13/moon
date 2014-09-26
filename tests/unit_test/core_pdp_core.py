"""
unit test for moon/core/pdp
"""

import unittest
import os.path
import pkg_resources
from moon.core.pdp.intra_extension import IntraExtension
from moon.core.pdp.inter_extension import VirtualEntity, InterExtension
from moon.core.pdp.core import IntraExtensions, InterExtensions
from moon.tests.unit_test.samples.mls001.core import results

class TestCorePDPCore(unittest.TestCase):

    def setUp(self):
        _sample = 'mls001'
        _sample_path = os.path.join('samples', _sample)
        intra_extension_setting_abs_dir = pkg_resources.resource_filename('moon', _sample_path)
        self.intra_extensions = IntraExtensions()
        self._intra_extension1_uuid = self.intra_extensions.install_intra_extension_from_json(intra_extension_setting_abs_dir)
        self._intra_extension2_uuid = self.intra_extensions.install_intra_extension_from_json(intra_extension_setting_abs_dir)
        self._inter_extensions = InterExtensions(self.intra_extensions.get_installed_intra_extensions())
        self._results = results

    def tearDown(self):
        pass

    def test_intra_extensions_get_installed_intra_extensions(self):
        self.assertIsInstance(self.intra_extensions.get_installed_intra_extensions(), dict)
        print("[Get Installed Intra Extensions]---------------- OK ")

    def test_intra_extensions_authz_admin(self):
        for _request in self._results["intra_extensions"]["authz"]:
            self.assertEqual(self.intra_extensions.authz(_request["subject"],
                                                         _request["object"],
                                                         _request["action"]),
                             _request["_result"])
        print("[IntraExtensions] Authz ---------------- OK ")

        for _request in self._results["intra_extensions"]["admin"]:
            self.assertEqual(self.intra_extensions.admin(_request["subject"],
                                                         _request["object"],
                                                         _request["action"]),
                             _request["_result"])
        print("[IntraExtensions] Admin: ---------------- OK ")

    def test_inter_extensions_authz_admin(self):
        for _genre in ["trust"]:
            (_inter_extension_uuid, _vent_uuid) = self._inter_extensions.create_collaboration(
                self._intra_extension1_uuid,
                self._intra_extension2_uuid,
                _genre,
                self._results["inter_extensions"][_genre]["subject_list"],
                self._results["inter_extensions"][_genre]["object_list"],
                self._results["inter_extensions"][_genre]["action"])
            self.assertEqual(len(_inter_extension_uuid), 36)
            self.assertEqual(len(_vent_uuid), 36)
            print("[InterExtensions] Create Collaboration ---------------- OK ")

            for _request in self._results["inter_extensions"][_genre]["requests"]:
                self.assertEqual(self._inter_extensions.authz(self._intra_extension1_uuid,
                                                              self._intra_extension2_uuid,
                                                              _request["subject"],
                                                              _request["object"],
                                                              _request["action"]),
                                 _request["result"])
                print("[InterExtensions] Authz: ---------------- OK ")

            self.assertEqual(self._inter_extensions.destroy_collaboration(_genre, _inter_extension_uuid, _vent_uuid),
                             "[InterExtensions] Destroy Collaboration: OK")
            print("[InterExtensions] Destroy Collaboration ---------------- OK ")

        for _genre in ["coordinate"]:
            (_inter_extension_uuid, _vent_uuid) = self._inter_extensions.create_collaboration(
                self._intra_extension1_uuid,
                self._intra_extension2_uuid,
                _genre,
                self._results["inter_extensions"][_genre]["subject_list"],
                self._results["inter_extensions"][_genre]["object_list"],
                self._results["inter_extensions"][_genre]["action"])
            self.assertEqual(len(_inter_extension_uuid), 36)
            self.assertEqual(len(_vent_uuid), 36)
            print("[InterExtensions] Create Collaboration ---------------- OK ")

            for _request in self._results["inter_extensions"][_genre]["requests"]:
                self.assertEqual(self._inter_extensions.admin(self._intra_extension1_uuid,
                                                              self._intra_extension2_uuid,
                                                              _request["subject"],
                                                              _request["object"],
                                                              _request["action"]),
                                 _request["result"])
                print("[InterExtensions] Admin: ---------------- OK ")

            self.assertEqual(self._inter_extensions.destroy_collaboration(_genre, _inter_extension_uuid, _vent_uuid),
                             "[InterExtensions] Destroy Collaboration: OK")
            print("[InterExtensions] Destroy Collaboration ---------------- OK ")

"""
    def test_intra_extensions_install_intra_extension_from_json(self):
        print("[test_intra_extensions_install_intra_extension_from_json]----------------: ",
              self.intra_extensions.get_installed_intra_extensions())
        _extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001')
        self.intra_extensions.install_intra_extension_from_json(_extension_setting_abs_dir)
        print("[test_intra_extensions_install_intra_extension_from_json]----------------: ",
              self.intra_extensions.get_installed_intra_extensions())

    def test_intra_extensions_get_from_db(self):
        print("[test_intra_extensions_get_from_db]----------------: ",
              self.intra_extensions.get_intra_extensions_from_db().keys())

    def test_intra_extensions_backup_intra_extensions_to_db(self):
        _extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001')
        self.intra_extensions.install_intra_extension_from_json(_extension_setting_abs_dir)
        print("[test_intra_extensions_backup_intra_extensions_to_db]----------------: ",
              self.intra_extensions.get_intra_extensions_from_db().keys())
        self.intra_extensions.backup_intra_extensions_to_db()
        print("[test_intra_extensions_backup_intra_extensions_to_db]----------------: ",
              self.intra_extensions.get_intra_extensions_from_db().keys())

    def test_install_intra_extensions_from_db(self):
        print("[test_install_intra_extensions_from_db]----------------: ",
              self.intra_extensions.get_installed_intra_extensions())
        self.intra_extensions.install_intra_extensions_from_db()
        print("[test_install_intra_extensions_from_db]----------------: ",
              self.intra_extensions.get_installed_intra_extensions())
"""

if __name__ == "__main__":
    unittest.main()

