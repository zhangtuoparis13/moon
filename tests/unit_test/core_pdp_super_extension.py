"""
unit test for moon/core/pdp/extension.py
"""

import unittest
import copy
from moon.core.pdp.super_extension.core import SuperExtension
from moon.tests.unit_test.samples.super_extension import results, requests


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
            print("[SuperExtension] Admin: ", _description, " ---------------- OK")

    def test_create_destroy_mapping(self):
        self.assertEqual(self.super_extension.list_mappings(), self._results["list_mappings"])
        print("[SuperExtension] list_mappings ---------------- OK")

        for i in range(len(results["create_mapping"])):
            _tenant_uuid = results["create_mapping"][i]['tenant_uuid']
            _intra_extension_uuid = results["create_mapping"][i]['intra_extension_uuid']
            _result = results["create_mapping"][i]['_result']
            self.assertEqual(self.super_extension.create_mapping(_tenant_uuid, _intra_extension_uuid), _result)
            print("[SuperExtension] Create Mapping  ---------------- OK")

        for i in range(len(results["destroy_mapping"])):
            _tenant_uuid = results["destroy_mapping"][i]['tenant_uuid']
            _intra_extension_uuid = results["destroy_mapping"][i]['intra_extension_uuid']
            _result = results["destroy_mapping"][i]['_result']
            self.assertEqual(self.super_extension.destroy_mapping(_tenant_uuid, _intra_extension_uuid), _result)
            print("[SuperExtension] Destroy Mapping  ---------------- OK")

    def test_delegate_mapping(self):
        _sub = results["delegate_test"]["before"]['subject']
        _obj = results["delegate_test"]["before"]['object']
        _act = results["delegate_test"]["before"]['action']
        _result = results["delegate_test"]["before"]['_result']
        _description = results["delegate_test"]["before"]['_description']
        self.assertEqual(self.super_extension.admin(_sub, _obj, _act), _result)
        print("[SuperExtension] Delegate Privilege Before: ", _description)

        for i in range(len(results["delegate_privilege"])):
            _delegator_id = results["delegate_privilege"][i]['delegator_id']
            _privilege = results["delegate_privilege"][i]['privilege']
            _result = results["delegate_privilege"][i]['_result']
            self.assertEqual(self.super_extension.delegate(_delegator_id, _privilege), _result)
            print("[SuperExtension] Delegate Privilege ---------------- OK")

        _sub = results["delegate_test"]["after"]['subject']
        _obj = results["delegate_test"]["after"]['object']
        _act = results["delegate_test"]["after"]['action']
        _result = results["delegate_test"]["after"]['_result']
        _description = results["delegate_test"]["after"]['_description']
        self.assertEqual(self.super_extension.admin(_sub, _obj, _act), _result)
        print("[SuperExtension] Delegate Privilege after: ", _description)

"""
    def test_get_subject_categories(self):
        self.assertIsInstance(self.extension.get_subject_categories(), list)
        self.assertEqual(self.extension.get_subject_categories(), self._results['subject_categories'])
        print("[Get Subject Categories]---------------- OK ")

    def test_get_object_categories(self):
        self.assertIsInstance(self.extension.get_object_categories(), list)
        self.assertEqual(self.extension.get_object_categories(), self._results['object_categories'])
        print("[Get Object Categories]---------------- OK ")

    def test_add_del_subject_category(self):
        self.assertEqual(self.extension.add_subject_category(self.extension.get_subject_categories()[0]),
                         "[ERROR] Add Subject Category: Subject Category Exists")
        print("[Add Subject Category] Subject Category Exists ---------------- OK ")

        self.assertEqual(self.extension.add_subject_category(self._results['new_subject_category']),
                         self._results['added_subject_category_list'])
        print("[Add Subject Category] add new subject category ---------------- OK ")

        self.assertEqual(self.extension.del_subject_category("xxxyyxxyy"),
                         "[ERROR] Del Subject Category: Subject Category Unknown")
        print("[Del Subject Category] Subject Category Unknown ---------------- ok")

        self.assertEqual(self.extension.del_subject_category(self._results['new_subject_category']),
                         self._results['subject_categories'])
        print("[Del Subject Category] del existing subject category ---------------- ok")

    def test_add_del_object_category(self):
        self.assertEqual(self.extension.add_object_category(self.extension.get_object_categories()[0]),
                         "[ERROR] Add Object Category: Object Category Exists")
        print("[Add Object Category] Object Category Exists ---------------- OK ")

        self.assertEqual(self.extension.add_object_category(self._results['new_object_category']),
                         self._results['added_object_category_list'])
        print("[Add Object Category] add new object category ---------------- OK ")

        self.assertEqual(self.extension.del_object_category("xxxyyxxyy"),
                         "[ERROR] Del Object Category: Object Category Unknown")
        print("[Del Object Category] Object Category Unknown ---------------- ok")

        self.assertEqual(self.extension.del_object_category(self._results['new_object_category']),
                         self._results['object_categories'])
        print("[Del Object Category] del existing object category ---------------- ok")

    def test_get_subject_category_values(self):
        for _sub_cat_id in self.extension.get_subject_categories():
            self.assertEqual(self.extension.get_subject_category_values(_sub_cat_id),
                             self._results["subject_category_values"][_sub_cat_id])
        print("[Get Subject Category Values] ---------------- OK ")

    def test_get_object_category_values(self):
        for _obj_cat_id in self.extension.get_object_categories():
            self.assertEqual(self.extension.get_object_category_values(_obj_cat_id),
                             self._results["object_category_values"][_obj_cat_id])
        print("[Get Object Category Values] ---------------- OK ")

    def test_add_del_subject_category_value(self):
        for _sub_cat_id in self.extension.get_subject_categories():
            _cat_values = self.extension.get_subject_category_values(_sub_cat_id)
            self.assertEqual(self.extension.add_subject_category_value(_sub_cat_id, _cat_values[0]),
                             "[ERROR] Add Subject Category Value: Subject Category Value Exists")
        print("[Add Subject Category Value] Subject Category Value Exists ---------------- OK ")

        for _sub_cat_id in self.extension.get_subject_categories():
            _result_added_cat_value = self._results['added_subject_category_values'][_sub_cat_id]
            self.assertEqual(self.extension.add_subject_category_value(_sub_cat_id, _result_added_cat_value),
                             self._results['new_subject_category_values'][_sub_cat_id])
        print("[Add Subject Category Value] add no existing subject category value ---------------- OK ")

        for _sub_cat_id in self.extension.get_subject_categories():
            self.assertEqual(self.extension.del_subject_category_value(_sub_cat_id, "xxooxxoo"),
                             "[ERROR] Del Subject Category Value: Subject Category Value Unknown")
        print("[Del Subject Category Value] Subject Category Value Unknown ---------------- OK")

        for _sub_cat_id in self.extension.get_subject_categories():
            _result_added_cat_value = self._results['added_subject_category_values'][_sub_cat_id]
            self.assertEqual(self.extension.del_subject_category_value(_sub_cat_id, _result_added_cat_value),
                             self._results['subject_category_values'][_sub_cat_id])
        print("[Del Subject Category Value] del existing subject category value ---------------- OK")

    def test_add_del_object_category_value(self):
        for _obj_cat_id in self.extension.get_object_categories():
            _cat_values = self.extension.get_object_category_values(_obj_cat_id)
            self.assertEqual(self.extension.add_object_category_value(_obj_cat_id, _cat_values[0]),
                             "[ERROR] Add Object Category Value: Object Category Value Exists")
        print("[Add Object Category Value] Object Category Value Exists ---------------- OK ")

        for _obj_cat_id in self.extension.get_object_categories():
            _result_added_cat_value = self._results['added_object_category_values'][_obj_cat_id]
            self.assertEqual(self.extension.add_object_category_value(_obj_cat_id, _result_added_cat_value),
                             self._results['new_object_category_values'][_obj_cat_id])
        print("[Add Object Category Value] add no existing object category value ---------------- OK ")

        for _obj_cat_id in self.extension.get_object_categories():
            self.assertEqual(self.extension.del_object_category_value(_obj_cat_id, "xxooxxoo"),
                             "[ERROR] Del Object Category Value: Object Category Value Unknown")
        print("[Del Object Category Value] Object Category Value Unknown ---------------- OK")

        for _obj_cat_id in self.extension.get_object_categories():
            _result_added_cat_value = self._results['added_object_category_values'][_obj_cat_id]
            self.assertEqual(self.extension.del_object_category_value(_obj_cat_id, _result_added_cat_value),
                             self._results['object_category_values'][_obj_cat_id])
        print("[Del Object Category Value] del existing object category value ---------------- OK")

    def test_get_rules(self):
        self.assertEqual(self.extension.get_rules(), self._results['rules'])
        print("[Get Rules]---------------- OK ")

    def test_add_del_rule(self):
        sub_cat_value = dict()
        obj_cat_value = dict()

        for _relation in self.extension.get_meta_rule()["sub_meta_rules"]:
            sub_cat_value[_relation] = dict()
            obj_cat_value[_relation] = dict()
            i = 0
            for _sub_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["subject_categories"]:
                sub_cat_value[_relation][_sub_cat_id] = self.extension.get_rules()[_relation][0][i]
                i += 1

            for _obj_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["object_categories"]:
                obj_cat_value[_relation][_obj_cat_id] = self.extension.get_rules()[_relation][0][i]
                i += 1
        self.assertEqual(self.extension.add_rule(sub_cat_value, obj_cat_value), "[Error] Add Rule: Rule Exists")
        print("[Add Rule] Rule Exists ---------------- OK ")

        for _relation in self.extension.get_meta_rule()["sub_meta_rules"]:
            sub_cat_value[_relation] = dict()
            obj_cat_value[_relation] = dict()
            for _sub_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["subject_categories"]:
                sub_cat_value[_relation][_sub_cat_id] = self._results["added_rule"][_relation][_sub_cat_id]

            for _obj_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["object_categories"]:
                obj_cat_value[_relation][_obj_cat_id] = self._results["added_rule"][_relation][_obj_cat_id]
        self.assertEqual(self.extension.add_rule(sub_cat_value, obj_cat_value),
                         "[Error] Add Rule: Subject Category Value Unknown")
        print("[Add Rule] Subject Category Value Unknown ---------------- OK ")

        for _relation in self.extension.get_meta_rule()["sub_meta_rules"]:
            sub_cat_value[_relation] = dict()
            obj_cat_value[_relation] = dict()
            for _sub_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["subject_categories"]:
                sub_cat_value[_relation][_sub_cat_id] = self._results["added_rule2"][_relation][_sub_cat_id]

            for _obj_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["object_categories"]:
                obj_cat_value[_relation][_obj_cat_id] = self._results["added_rule2"][_relation][_obj_cat_id]
        self.assertEqual(self.extension.add_rule(sub_cat_value, obj_cat_value),
                         "[Error] Add Rule: Object Category Value Unknown")
        print("[Add Rule] Object Category Value Unknown ---------------- OK ")

        for _relation in self.extension.get_meta_rule()["sub_meta_rules"]:
            sub_cat_value[_relation] = dict()
            obj_cat_value[_relation] = dict()
            for _sub_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["subject_categories"]:
                sub_cat_value[_relation][_sub_cat_id] = self._results["added_rule3"][_relation][_sub_cat_id]

            for _obj_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["object_categories"]:
                obj_cat_value[_relation][_obj_cat_id] = self._results["added_rule3"][_relation][_obj_cat_id]

        self.assertEqual(self.extension.add_rule(sub_cat_value, obj_cat_value), self._results["new_rules"])
        print("[Add Rule] add a no existing  rule ---------------- OK ")

        for _relation in self.extension.get_meta_rule()["sub_meta_rules"]:
            sub_cat_value[_relation] = dict()
            obj_cat_value[_relation] = dict()

            for _sub_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["subject_categories"]:
                sub_cat_value[_relation][_sub_cat_id] = "xxooxxoo"

            for _obj_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["object_categories"]:
                obj_cat_value[_relation][_obj_cat_id] = "xxooxxoo"

        self.assertEqual(self.extension.del_rule(sub_cat_value, obj_cat_value), "[Error] Del Rule: Rule Unknown")
        print("[Del Rule] Rule Unknown ---------------- OK ")

        for _relation in self.extension.get_meta_rule()["sub_meta_rules"]:
            sub_cat_value[_relation] = dict()
            obj_cat_value[_relation] = dict()
            for _sub_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["subject_categories"]:
                sub_cat_value[_relation][_sub_cat_id] = self._results["added_rule3"][_relation][_sub_cat_id]

            for _obj_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["object_categories"]:
                obj_cat_value[_relation][_obj_cat_id] = self._results["added_rule3"][_relation][_obj_cat_id]

        self.assertEqual(self.extension.del_rule(sub_cat_value, obj_cat_value), self._results['rules'])
        print("[Del Rule] del an existing  rule ---------------- OK ")

    def test_get_subjects(self):
        self.assertEqual(self.extension.get_subjects(), self._results["subjects"])
        print("[Get Subjects]---------------- OK ")

    def test_add_del_subject(self):
        self.assertEqual(self.extension.add_subject(self.extension.get_subjects()[0]),
                         "[ERROR] Add Subject: Subject Exists")
        print("[Add Subject] Subject Exists ---------------- OK ")

        self.assertEqual(self.extension.add_subject(self._results["added_subject"]), self._results["new_subjects"])
        print("[Add Subject] add a new subject ---------------- OK ")

        self.assertEqual(self.extension.del_subject("xxooxxoo"), "[ERROR] Del Subject: Subject Unknown")
        print("[Del Subject] Subject Unknown ---------------- ")

        self.assertEqual(self.extension.del_subject(self._results["added_subject"]), self._results["subjects"])
        print("[Del Subject] del an existing subject ---------------- OK ")

    def test_get_objects(self):
        self.assertEqual(self.extension.get_objects(), self._results["objects"])
        print("[Get Objects]---------------- OK ")

    def test_add_del_object(self):
        self.assertEqual(self.extension.add_object(self.extension.get_objects()[0]),
                         "[ERROR] Add Object: Object Exists")
        print("[Add Object] Object Exists ---------------- OK ")

        self.assertEqual(self.extension.add_object(self._results["added_object"]), self._results["new_objects"])
        print("[Add Object] add a new object ---------------- OK ")

        self.assertEqual(self.extension.del_object("xxooxxoo"), "[ERROR] Del Object: Object Unknown")
        print("[Del Object] Object Unknown ---------------- OK ")

        self.assertEqual(self.extension.del_object(self._results["added_object"]), self._results["objects"])
        print("[Del Object] del an existing object ---------------- OK ")

    def test_get_subject_assignments(self):
        self.assertEqual(self.extension.get_subject_assignments("xxooxxoo"),
                         "[ERROR] Get Subject Assignment: Subject Category Unknown")
        print("[Get Subject Assignment] Subject Category Unknown ---------------- OK ")

        for _sub_cat_id in self.extension.get_subject_categories():
            self.assertEqual(self.extension.get_subject_assignments(_sub_cat_id),
                             self._results["subject_category_assignments"][_sub_cat_id])
        print("[Get Subject Assignment] ---------------- OK ")

    def test_add_del_subject_assignment(self):
        for _sub_cat_id in self._results["added_subject_category_assignment1"]:
            for _sub_id in self._results["added_subject_category_assignment1"][_sub_cat_id]:
                self.assertEqual(self.extension.add_subject_assignment(
                    _sub_cat_id, _sub_id, self._results["added_subject_category_assignment1"][_sub_cat_id][_sub_id]),
                                 "[ERROR] Add Subject Assignment: Subject Category Unknown")
        print("[Add Subject Assignment] Subject Category Unknown ---------------- OK ")

        for _sub_cat_id in self._results["added_subject_category_assignment2"]:
            for _sub_id in self._results["added_subject_category_assignment2"][_sub_cat_id]:
                self.assertEqual(self.extension.add_subject_assignment(
                    _sub_cat_id, _sub_id, self._results["added_subject_category_assignment2"][_sub_cat_id][_sub_id]),
                                 "[ERROR] Add Subject Assignment: Subject Unknown")
        print("[Add Subject Assignment] Subject Unknown ---------------- OK ")

        for _sub_cat_id in self._results["added_subject_category_assignment3"]:
            for _sub_id in self._results["added_subject_category_assignment3"][_sub_cat_id]:
                self.assertEqual(self.extension.add_subject_assignment(
                    _sub_cat_id, _sub_id, self._results["added_subject_category_assignment3"][_sub_cat_id][_sub_id]),
                                 "[ERROR] Add Subject Assignment: Subject Category Value Unknown")
        print("[Add Subject Assignment] Subject Category Value Unknown ---------------- OK ")

        for _sub_cat_id in self._results["added_subject_category_assignment4"]:
            for _sub_id in self._results["added_subject_category_assignment4"][_sub_cat_id]:
                self.assertEqual(self.extension.add_subject_assignment(
                    _sub_cat_id, _sub_id, self._results["added_subject_category_assignment4"][_sub_cat_id][_sub_id]),
                                 "[ERROR] Add Subject Assignment: Subject Assignment Exists")
        print("[Add Subject Assignment] Subject Assignment Exists ---------------- OK ")

        for _sub_cat_id in self._results["added_subject_category_assignment5"]:
            for _sub_id in self._results["added_subject_category_assignment5"][_sub_cat_id]:

                self.assertEqual(self.extension.add_subject_assignment(
                    _sub_cat_id, _sub_id, self._results["added_subject_category_assignment5"][_sub_cat_id][_sub_id]),
                                 self._results["new_subject_category_assignments"])
        print("[Add Subject Assignment] ---------------- OK ")

        for _sub_cat_id in self._results["added_subject_category_assignment1"]:
            for _sub_id in self._results["added_subject_category_assignment1"][_sub_cat_id]:
                self.assertEqual(self.extension.del_subject_assignment(
                    _sub_cat_id, _sub_id, self._results["added_subject_category_assignment1"][_sub_cat_id][_sub_id]),
                                 "[ERROR] Del Subject Assignment: Subject Category Unknown")
        print("[Del Subject Assignment] Subject Category Unknown ---------------- OK ")

        for _sub_cat_id in self._results["added_subject_category_assignment2"]:
            for _sub_id in self._results["added_subject_category_assignment2"][_sub_cat_id]:
                self.assertEqual(self.extension.del_subject_assignment(
                    _sub_cat_id, _sub_id, self._results["added_subject_category_assignment2"][_sub_cat_id][_sub_id]),
                                 "[ERROR] Del Subject Assignment: Subject Unknown")
        print("[Del Subject Assignment] Subject Unknown ---------------- OK ")

        for _sub_cat_id in self._results["added_subject_category_assignment3"]:
            for _sub_id in self._results["added_subject_category_assignment3"][_sub_cat_id]:
                self.assertEqual(self.extension.del_subject_assignment(
                    _sub_cat_id, _sub_id, self._results["added_subject_category_assignment3"][_sub_cat_id][_sub_id]),
                                 "[ERROR] Del Subject Assignment: Assignment Unknown")
        print("[Del Subject Assignment] Assignment Unknown ---------------- OK ")

        for _sub_cat_id in self._results["added_subject_category_assignment5"]:
            for _sub_id in self._results["added_subject_category_assignment5"][_sub_cat_id]:
                self.assertEqual(self.extension.del_subject_assignment(
                    _sub_cat_id, _sub_id, self._results["added_subject_category_assignment5"][_sub_cat_id][_sub_id]),
                                 self._results["subject_category_assignments"])
        print("[Del Subject Assignment] ---------------- OK ")

    def test_get_object_assignments(self):
        self.assertEqual(self.extension.get_object_assignments("xxooxxoo"),
                         "[ERROR] Get Object Assignment: Object Category Unknown")
        print("[Get Object Assignment] Object Category Unknown ---------------- OK ")

        for _obj_cat_id in self.extension.get_object_categories():
            self.assertEqual(self.extension.get_object_assignments(_obj_cat_id),
                             self._results["object_category_assignments"][_obj_cat_id])
        print("[Get Object Assignment] ---------------- OK ")

    def test_add_del_object_assignment(self):
        for _obj_cat_id in self._results["added_object_category_assignment1"]:
            for _obj_id in self._results["added_object_category_assignment1"][_obj_cat_id]:
                self.assertEqual(self.extension.add_object_assignment(
                    _obj_cat_id, _obj_id, self._results["added_object_category_assignment1"][_obj_cat_id][_obj_id]),
                                 "[ERROR] Add Object Assignment: Object Category Unknown")
        print("[Add Object Assignment] Object Category Unknown ---------------- OK ")

        for _obj_cat_id in self._results["added_object_category_assignment2"]:
            for _obj_id in self._results["added_object_category_assignment2"][_obj_cat_id]:
                self.assertEqual(self.extension.add_object_assignment(
                    _obj_cat_id, _obj_id, self._results["added_object_category_assignment2"][_obj_cat_id][_obj_id]),
                                 "[ERROR] Add Object Assignment: Object Unknown")
        print("[Add Object Assignment] Object Unknown ---------------- OK ")

        for _obj_cat_id in self._results["added_object_category_assignment3"]:
            for _obj_id in self._results["added_object_category_assignment3"][_obj_cat_id]:
                self.assertEqual(self.extension.add_object_assignment(
                    _obj_cat_id, _obj_id, self._results["added_object_category_assignment3"][_obj_cat_id][_obj_id]),
                                 "[ERROR] Add Object Assignment: Object Category Value Unknown")
        print("[Add Object Assignment] Object Category Value Unknown ---------------- OK ")

        for _obj_cat_id in self._results["added_object_category_assignment4"]:
            for _obj_id in self._results["added_object_category_assignment4"][_obj_cat_id]:
                if _obj_cat_id == "action":
                    pass
                else:
                    self.assertEqual(self.extension.add_object_assignment(
                        _obj_cat_id, _obj_id, self._results["added_object_category_assignment4"][_obj_cat_id][_obj_id]),
                                     "[ERROR] Add Object Assignment: Object Assignment Exists")
        print("[Add Object Assignment] Object Assignment Exists ---------------- OK ")

        for _obj_cat_id in self._results["added_object_category_assignment5"]:
            for _obj_id in self._results["added_object_category_assignment5"][_obj_cat_id]:
                if _obj_cat_id == "action":
                    pass
                else:
                    self.assertEqual(self.extension.add_object_assignment(
                        _obj_cat_id, _obj_id, self._results["added_object_category_assignment5"][_obj_cat_id][_obj_id]),
                                     self._results["new_object_category_assignments"])
        print("[Add Object Assignment] ---------------- OK ")

        for _obj_cat_id in self._results["added_object_category_assignment1"]:
            for _obj_id in self._results["added_object_category_assignment1"][_obj_cat_id]:
                self.assertEqual(self.extension.del_object_assignment(
                    _obj_cat_id, _obj_id, self._results["added_object_category_assignment1"][_obj_cat_id][_obj_id]),
                                 "[ERROR] Del Object Assignment: Object Category Unknown")
        print("[Del Object Assignment] Object Category Unknown ---------------- OK ")

        for _obj_cat_id in self._results["added_object_category_assignment2"]:
            for _obj_id in self._results["added_object_category_assignment2"][_obj_cat_id]:
                self.assertEqual(self.extension.del_object_assignment(
                    _obj_cat_id, _obj_id, self._results["added_object_category_assignment2"][_obj_cat_id][_obj_id]),
                                 "[ERROR] Del Object Assignment: Object Unknown")
        print("[Del Object Assignment] Object Unknown ---------------- OK ")

        for _obj_cat_id in self._results["added_object_category_assignment3"]:
            for _obj_id in self._results["added_object_category_assignment3"][_obj_cat_id]:
                self.assertEqual(self.extension.del_object_assignment(
                    _obj_cat_id, _obj_id, self._results["added_object_category_assignment3"][_obj_cat_id][_obj_id]),
                                 "[ERROR] Del Object Assignment: Assignment Unknown")
        print("[Del Object Assignment] Assignment Unknown ---------------- OK ")

        for _obj_cat_id in self._results["added_object_category_assignment5"]:
            for _obj_id in self._results["added_object_category_assignment5"][_obj_cat_id]:
                if _obj_cat_id == "action":
                    pass
                else:
                    self.assertEqual(self.extension.del_object_assignment(
                        _obj_cat_id, _obj_id, self._results["added_object_category_assignment5"][_obj_cat_id][_obj_id]),
                                     self._results["object_category_assignments"])
        print("[Del Object Assignment] ---------------- OK ")

    def test_create_requested_collaboration(self):
        _vent_uuid = self._results["collaboration"]["requested"]["vent_uuid"]
        _objs = self._results["collaboration"]["requested"]["object_list"]
        _data = copy.deepcopy(self.extension.get_data())
        _dict = self.extension.create_requested_collaboration(_vent_uuid, _objs, "read")
        self.assertIsInstance(_dict, dict)
        self.assertEqual(self.extension.destroy_requested_collaboration(_vent_uuid, _objs,
                                                                        _dict["subject_category_value_dict"],
                                                                        _dict["object_category_value_dict"]),
                         "[Destroy Requested Collaboration] OK")
        self.assertEqual(self.extension.get_data(), _data)

    def test_get_set_data(self):
        print("[test_get_data]----------------: ", self.extension.get_data().keys())

        _extension = Extension()
        if self.extension.get_type() == "authz":
            _extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001/admin')
        elif self.extension.get_type() == "admin":
            _extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001/authz')
        _extension.load_from_json(_extension_setting_abs_dir)
        _data = _extension.get_data()
        self.extension.set_data(_data)
        print("[test_set_data]----------------: ", self.extension.get_data().keys())

"""

if __name__ == "__main__":
    unittest.main()