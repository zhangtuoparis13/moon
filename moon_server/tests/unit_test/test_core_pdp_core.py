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
from moon_server.core.pdp.core import get_intra_extensions, get_inter_extensions, get_tenant_intra_extension_mapping
from moon_server.tests.unit_test.samples.mls001.core import results
from moon_server.core.pip import get_pip


class TestCorePDPCore(unittest.TestCase):

    def setUp(self):
        _sample = 'mls001'
        _sample_path = os.path.join('samples', _sample)
        self.pip = get_pip()
        self.intra_extension_setting_abs_dir = pkg_resources.resource_filename('moon_server', _sample_path)
        self.intra_extensions = get_intra_extensions()
        self._intra_extension1_uuid = self.intra_extensions.install_intra_extension_from_json(self.intra_extension_setting_abs_dir)
        self._intra_extension2_uuid = self.intra_extensions.install_intra_extension_from_json(self.intra_extension_setting_abs_dir)
        self._inter_extensions = get_inter_extensions()
        self.__tenant_intra_extension_mapping = get_tenant_intra_extension_mapping()
        self._results = results
        # print(self._intra_extension1_uuid, self._intra_extension2_uuid)

    def tearDown(self):
        self.intra_extensions.delete_intra_extension(self._intra_extension1_uuid)
        self.intra_extensions.delete_intra_extension(self._intra_extension2_uuid)

    def test_intra_extensions_get_installed_intra_extensions(self):
        self.assertIsInstance(self.intra_extensions.get_installed_intra_extensions(), dict)
        # print("[Get Installed Intra Extensions]---------------- OK ")

    def test_intra_extensions_authz_admin(self):
        for _request in self._results["intra_extensions"]["authz"]:
            self.assertEqual(self.intra_extensions.authz(_request["subject"],
                                                         _request["object"],
                                                         _request["action"]),
                             _request["_result"])
        # print("[IntraExtensions] Authz ---------------- OK ")

        for _request in self._results["intra_extensions"]["admin"]:
            self.assertEqual(self.intra_extensions.admin(_request["subject"],
                                                         _request["object"],
                                                         _request["action"]),
                             _request["_result"])
        # print("[IntraExtensions] Admin: ---------------- OK ")

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
            # print("[InterExtensions] Create Collaboration ---------------- OK ")

            for _request in self._results["inter_extensions"][_genre]["requests"]:
                self.assertEqual(self._inter_extensions.authz(self._intra_extension1_uuid,
                                                              self._intra_extension2_uuid,
                                                              _request["subject"],
                                                              _request["object"],
                                                              _request["action"]),
                                 _request["result"])
                # print("[InterExtensions] Authz: ---------------- OK ")

            self.assertEqual(self._inter_extensions.destroy_collaboration(_genre, _inter_extension_uuid, _vent_uuid),
                             "[InterExtensions] Destroy Collaboration: OK")
            # print("[InterExtensions] Destroy Collaboration ---------------- OK ")

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
            # print("[InterExtensions] Create Collaboration ---------------- OK ")

            for _request in self._results["inter_extensions"][_genre]["requests"]:
                self.assertEqual(self._inter_extensions.admin(self._intra_extension1_uuid,
                                                              self._intra_extension2_uuid,
                                                              _request["subject"],
                                                              _request["object"],
                                                              _request["action"]),
                                 _request["result"])
                # print("[InterExtensions] Admin: ---------------- OK ")

            self.assertEqual(self._inter_extensions.destroy_collaboration(_genre, _inter_extension_uuid, _vent_uuid),
                             "[InterExtensions] Destroy Collaboration: OK")
            # print("[InterExtensions] Destroy Collaboration ---------------- OK ")

    def test_create_destroy_mapping(self):
        self.assertEqual(self.__tenant_intra_extension_mapping.list_mappings(), self._results["list_mappings"])
        # print("[TenantIntraExtensionMapping] list_mappings ---------------- OK")
        _intra_extension_uuid = self.intra_extensions.install_intra_extension_from_json(self.intra_extension_setting_abs_dir)
        admin_tenant_uuid = self.pip.get_tenants(name="admin").next()["uuid"]
        mapping = self.__tenant_intra_extension_mapping.create_mapping(admin_tenant_uuid, _intra_extension_uuid)
        mapping = self.__tenant_intra_extension_mapping.destroy_mapping(admin_tenant_uuid, _intra_extension_uuid)

        # for i in range(len(results["create_mapping"])):
        #     # print(results["create_mapping"][i])
        #     _tenant_uuid = results["create_mapping"][i]['tenant_uuid']
        #     # _intra_extension_uuid = results["create_mapping"][i]['intra_extension_uuid']
        #     _intra_extension_uuid = self.intra_extensions.install_intra_extension_from_json(self.intra_extension_setting_abs_dir)
        #     _result = results["create_mapping"][i]['_result']
        #     self.assertEqual(self.__tenant_intra_extension_mapping.create_mapping(_tenant_uuid, _intra_extension_uuid), _result)
        #     # print("[TenantIntraExtensionMapping] Create Mapping  ---------------- OK")
        #
        # for i in range(len(results["destroy_mapping"])):
        #     _tenant_uuid = results["destroy_mapping"][i]['tenant_uuid']
        #     # _intra_extension_uuid = results["destroy_mapping"][i]['intra_extension_uuid']
        #     _intra_extension_uuid = self.intra_extensions.install_intra_extension_from_json(self.intra_extension_setting_abs_dir)
        #     _result = results["destroy_mapping"][i]['_result']
        #     self.assertEqual(self.__tenant_intra_extension_mapping.destroy_mapping(_tenant_uuid, _intra_extension_uuid), _result)
        #     # print("[TenantIntraExtensionMapping] Destroy Mapping  ---------------- OK")



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

