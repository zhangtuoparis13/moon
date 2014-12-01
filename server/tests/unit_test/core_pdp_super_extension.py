"""
unit test for moon/core/pdp/extension.py
"""

import unittest
import copy
from moon.core.pdp.super_extension.core import SuperExtension
from moon.tests.unit_test.samples.super_extension import results, requests, requests2


class TestCorePDPExtension(unittest.TestCase):

    def setUp(self):
        self.super_extension = SuperExtension()
        self._requests = requests
        self._results = results

    def tearDown(self):
        pass

    def test_admin(self):
        for i in range(len(requests)):
            _sub = requests[i]['subject']
            _obj = requests[i]['object']
            _act = requests[i]['action']
            _result = requests[i]['_result']
            _description = requests[i]['_description']
            self.assertEqual(self.super_extension.admin(_sub, _obj, _act), _result)
            print("[SuperExtension] Mapping Admin: ", _description, " ---------------- OK")

        for i in range(len(requests2)):
            _sub = requests2[i]['subject']
            _obj = requests2[i]['object']
            _act = requests2[i]['action']
            _result = requests2[i]['_result']
            _description = requests2[i]['_description']
            self.assertEqual(self.super_extension.admin(_sub, _obj, _act), _result)
            print("[SuperExtension] Collaboration Admin: ", _description, " ---------------- OK")

    def test_delegate_mapping(self):
        _sub = results["delegate_mapping_admin"]["before"]['subject']
        _obj = results["delegate_mapping_admin"]["before"]['object']
        _act = results["delegate_mapping_admin"]["before"]['action']
        _result = results["delegate_mapping_admin"]["before"]['_result']
        _description = results["delegate_mapping_admin"]["before"]['_description']
        self.assertEqual(self.super_extension.admin(_sub, _obj, _act), _result)
        print("[SuperExtension] Mapping Delegate Privilege Before: ", _description)

        for i in range(len(results["delegate_mapping_privilege"])):
            _delegator_id = results["delegate_mapping_privilege"][i]['delegator_id']
            _privilege = results["delegate_mapping_privilege"][i]['privilege']
            _result = results["delegate_mapping_privilege"][i]['_result']
            self.assertEqual(self.super_extension.delegate(_delegator_id, _privilege), _result)
            print("[SuperExtension] Delegate Mapping Privilege ---------------- OK")

        _sub = results["delegate_mapping_admin"]["after"]['subject']
        _obj = results["delegate_mapping_admin"]["after"]['object']
        _act = results["delegate_mapping_admin"]["after"]['action']
        _result = results["delegate_mapping_admin"]["after"]['_result']
        _description = results["delegate_mapping_admin"]["after"]['_description']
        self.assertEqual(self.super_extension.admin(_sub, _obj, _act), _result)
        print("[SuperExtension] Mapping Delegate Privilege after: ", _description)

    # def test_delegate_collaboration(self):
    #     _sub = results["delegate_collaboration_admin"]["before"]['subject']
    #     _obj = results["delegate_collaboration_admin"]["before"]['object']
    #     _act = results["delegate_collaboration_admin"]["before"]['action']
    #     _result = results["delegate_collaboration_admin"]["before"]['_result']
    #     _description = results["delegate_collaboration_admin"]["before"]['_description']
    #     self.assertEqual(self.super_extension.admin(_sub, _obj, _act), _result)
    #     print("[InterExtension] Delegate Collaboration Privilege Before: ", _description)
    #
    #     for i in range(len(results["delegate_collaboration_privilege"])):
    #         _delegator_id = results["delegate_collaboration_privilege"][i]['delegator_id']
    #         _privilege = results["delegate_collaboration_privilege"][i]['privilege']
    #         _result = results["delegate_collaboration_privilege"][i]['_result']
    #         self.assertEqual(self.super_extension.delegate(_delegator_id, _privilege), _result)
    #         print("[InterExtension] Delegate Collaboration Privilege ---------------- OK")
    #
    #     _sub = results["delegate_collaboration_admin"]["after"]['subject']
    #     _obj = results["delegate_collaboration_admin"]["after"]['object']
    #     _act = results["delegate_collaboration_admin"]["after"]['action']
    #     _result = results["delegate_collaboration_admin"]["after"]['_result']
    #     _description = results["delegate_collaboration_admin"]["after"]['_description']
    #     self.assertEqual(self.super_extension.admin(_sub, _obj, _act), _result)
    #     print("[InterExtension] Delegate Collaboration Privilege after: ", _description)

if __name__ == "__main__":
    unittest.main()