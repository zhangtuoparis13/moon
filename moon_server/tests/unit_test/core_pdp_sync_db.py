"""
unit test for moon/core/pdp
"""

import unittest
import pkg_resources
from moon_server.core.pdp.extension import Extension
from moon_server.core.pdp.sync_db import IntraExtensionSyncer, IntraExtensionsSyncer
from moon_server.core.pdp.intra_extension import IntraExtension
from moon_server.core.pdp.core import IntraExtensions
from moon_server.core.pdp.inter_extension import VirtualEntity, InterExtension


class TestCorePDPSyncdb(unittest.TestCase):

    def setUp(self):
        self.intra_extension_syncer = IntraExtensionSyncer()
        self.intra_extensions_syncer = IntraExtensionsSyncer()

    def tearDown(self):
        pass

    def test_intra_extension_drop(self):
        self.intra_extension_syncer.drop()
        print("[test_intra_extension_drop]----------------: ")

    def test_intra_extension_backup_to_db_and_get_from_db(self):
        _intra_extension = IntraExtension()
        _intra_extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001')
        _intra_extension.load_from_json(_intra_extension_setting_abs_dir)
        _data = _intra_extension.get_data()
        self.intra_extension_syncer.backup_intra_extension_to_db(_data)

        _intra_extension = IntraExtension()
        _intra_extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls002')
        _intra_extension.load_from_json(_intra_extension_setting_abs_dir)
        _data = _intra_extension.get_data()
        self.intra_extension_syncer.backup_intra_extension_to_db(_data)

        _uuid = _intra_extension.get_uuid()
        print("[test_intra_extension_backup_to_db_and_get_from_db] for", _uuid, "----------------: ",
              self.intra_extension_syncer.get_intra_extension_from_db(_uuid).keys())

    # def test_intra_extensions_drop(self):
    #     self.intra_extension_syncer.drop()
    #     print("[test_intra_extensions_drop]----------------: ")

    def test_intra_extensions_get_from_db(self):
        print("[test_intra_extensions_get_from_db]----------------: ",
              self.intra_extensions_syncer.get_intra_extensions_from_db())


if __name__ == "__main__":
    unittest.main()

