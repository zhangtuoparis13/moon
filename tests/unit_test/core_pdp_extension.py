"""
unit test for moon/core/pdp/extension.py
"""

import os.path
import unittest
import pkg_resources
from moon.core.pdp.extension import Extension
from moon.tests.unit_test.samples.mls001.extension import results, requests


class TestCorePDPExtension(unittest.TestCase):

    def setUp(self):
        _sample = 'mls001'
        _genre = 'authz'
        #_genre = 'admin'
        _sample_path = os.path.join('samples', _sample, _genre)
        extension_setting_abs_dir = pkg_resources.resource_filename('moon', _sample_path)
        self.extension = Extension()
        self.extension.load_from_json(extension_setting_abs_dir)
        self._requests = requests
        self._results = results[_genre]

    def tearDown(self):
        pass

    def test_get_name(self):

        self.assertIsInstance(self.extension.get_name(), unicode)
        self.assertEqual(self.extension.get_name(), self._results['name'])
        print("[test_get_name]---------------- OK")

    def test_get_type(self):
        self.assertIsInstance(self.extension.get_genre(), unicode)
        self.assertEqual(self.extension.get_genre(), self._results['genre'])
        print("[test_get_genre]---------------- OK")

    def test_authz(self):
        _genre = self.extension.get_genre()
        for i in range(len(requests[_genre])):
            _sub = requests[_genre][i]['subject']
            _obj = requests[_genre][i]['object']
            _act = requests[_genre][i]['action']
            _result = requests[_genre][i]['_result']
            _description = requests[_genre][i]['_description']
            self.assertEqual(self.extension.authz(_sub, _obj, _act), _result)
            print("[test_authz] ", _description, " ---------------- OK")

    def test_get_subject_categories(self):
        self.assertIsInstance(self.extension.get_subject_categories(), list)
        self.assertEqual(self.extension.get_subject_categories(), self._results['subject_categories'])
        print("[test_get_subject_categories]---------------- OK ")

    def test_get_object_categories(self):
        self.assertIsInstance(self.extension.get_object_categories(), list)
        self.assertEqual(self.extension.get_object_categories(), self._results['object_categories'])
        print("[test_get_object_categories]---------------- OK ")

    def test_add_del_subject_category(self):
        self.assertEqual(self.extension.add_subject_category(self.extension.get_subject_categories()[0]), False)
        print("[test_add_subject_category] add existing subject category ---------------- OK ")

        self.assertEqual(self.extension.add_subject_category(self._results['new_subject_category']),
                         self._results['added_subject_category_list'])
        print("[test_add_subject_category] add new subject category ---------------- OK ")

        self.assertEqual(self.extension.del_subject_category("xxxyyxxyy"), False)
        print("[test_del_subject_category] del no-existing subject category ---------------- ok")

        self.assertEqual(self.extension.del_subject_category(self._results['new_subject_category']),
                         self._results['subject_categories'])
        print("[test_del_subject_category] del existing subject category ---------------- ok")

    def test_add_del_object_category(self):
        self.assertEqual(self.extension.add_object_category(self.extension.get_object_categories()[0]), False)
        print("[test_add_object_category] add existing object category ---------------- OK ")

        self.assertEqual(self.extension.add_object_category(self._results['new_object_category']),
                         self._results['added_object_category_list'])
        print("[test_add_object_category] add new object category ---------------- OK ")

        self.assertEqual(self.extension.del_object_category("xxxyyxxyy"), False)
        print("[test_del_object_category] del no-existing object category ---------------- ok")

        self.assertEqual(self.extension.del_object_category(self._results['new_object_category']),
                         self._results['object_categories'])
        print("[test_del_object_category] del existing object category ---------------- ok")

    def test_get_subject_category_values(self):
        for _sub_cat_id in self.extension.get_subject_categories():
            self.assertEqual(self.extension.get_subject_category_values(_sub_cat_id),
                             self._results["subject_category_values"][_sub_cat_id])
        print("[test_get_subject_category_values] ---------------- OK ")

    def test_get_object_category_values(self):
        for _obj_cat_id in self.extension.get_object_categories():
            self.assertEqual(self.extension.get_object_category_values(_obj_cat_id),
                             self._results["object_category_values"][_obj_cat_id])
        print("[test_get_object_category_values] ---------------- OK ")

    def test_add_del_subject_category_value(self):
        for _sub_cat_id in self.extension.get_subject_categories():
            _cat_values = self.extension.get_subject_category_values(_sub_cat_id)
            self.assertEqual(self.extension.add_subject_category_value(_sub_cat_id, _cat_values[0]), False)
        print("[test_add_subject_category_value] add existing subject category value ---------------- OK ")

        for _sub_cat_id in self.extension.get_subject_categories():
            _result_added_cat_value = self._results['added_subject_category_values'][_sub_cat_id]
            self.assertEqual(self.extension.add_subject_category_value(_sub_cat_id, _result_added_cat_value),
                             self._results['new_subject_category_values'][_sub_cat_id])
        print("[test_add_subject_category_value] add no existing subject category value ---------------- OK ")

        for _sub_cat_id in self.extension.get_subject_categories():
            self.assertEqual(self.extension.del_subject_category_value(_sub_cat_id, "xxooxxoo"), False)
        print("[test_del_subject_category_value] del no existing subject category value ---------------- OK")

        for _sub_cat_id in self.extension.get_subject_categories():
            _result_added_cat_value = self._results['added_subject_category_values'][_sub_cat_id]
            self.assertEqual(self.extension.del_subject_category_value(_sub_cat_id, _result_added_cat_value),
                             self._results['subject_category_values'][_sub_cat_id])
        print("[test_del_subject_category_value] del existing subject category value ---------------- OK")

    def test_add_del_object_category_value(self):
        for _obj_cat_id in self.extension.get_object_categories():
            _cat_values = self.extension.get_object_category_values(_obj_cat_id)
            self.assertEqual(self.extension.add_object_category_value(_obj_cat_id, _cat_values[0]), False)
        print("[test_add_object_category_value] add existing object category value ---------------- OK ")

        for _obj_cat_id in self.extension.get_object_categories():
            _result_added_cat_value = self._results['added_object_category_values'][_obj_cat_id]
            self.assertEqual(self.extension.add_object_category_value(_obj_cat_id, _result_added_cat_value),
                             self._results['new_object_category_values'][_obj_cat_id])
        print("[test_add_object_category_value] add no existing object category value ---------------- OK ")

        for _obj_cat_id in self.extension.get_object_categories():
            self.assertEqual(self.extension.del_object_category_value(_obj_cat_id, "xxooxxoo"), False)
        print("[test_del_object_category_value] del no existing object category value ---------------- OK")

        for _obj_cat_id in self.extension.get_object_categories():
            _result_added_cat_value = self._results['added_object_category_values'][_obj_cat_id]
            self.assertEqual(self.extension.del_object_category_value(_obj_cat_id, _result_added_cat_value),
                             self._results['object_category_values'][_obj_cat_id])
        print("[test_del_object_category_value] del existing object category value ---------------- OK")

    def test_get_rules(self):
        self.assertEqual(self.extension.get_rules(), self._results['rules'])
        print("[test_get_rules]---------------- OK ")

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

        self.assertEqual(self.extension.add_rule(sub_cat_value, obj_cat_value), False)
        print("[test_add_rule] add an existing  rule ---------------- OK ")

        for _relation in self.extension.get_meta_rule()["sub_meta_rules"]:
            sub_cat_value[_relation] = dict()
            obj_cat_value[_relation] = dict()
            for _sub_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["subject_categories"]:
                sub_cat_value[_relation][_sub_cat_id] = self._results["added_rule"][_relation][_sub_cat_id]

            for _obj_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["object_categories"]:
                obj_cat_value[_relation][_obj_cat_id] = self._results["added_rule"][_relation][_obj_cat_id]

        self.assertEqual(self.extension.add_rule(sub_cat_value, obj_cat_value), self._results["new_rules"])
        print("[test_add_rule] add a no existing  rule ---------------- OK ")

        for _relation in self.extension.get_meta_rule()["sub_meta_rules"]:
            sub_cat_value[_relation] = dict()
            obj_cat_value[_relation] = dict()

            for _sub_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["subject_categories"]:
                sub_cat_value[_relation][_sub_cat_id] = "xxooxxoo"

            for _obj_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["object_categories"]:
                obj_cat_value[_relation][_obj_cat_id] = "xxooxxoo"

        self.assertEqual(self.extension.del_rule(sub_cat_value, obj_cat_value), False)
        print("[test_del_rule] del a no existing  rule ---------------- OK ")

        for _relation in self.extension.get_meta_rule()["sub_meta_rules"]:
            sub_cat_value[_relation] = dict()
            obj_cat_value[_relation] = dict()
            for _sub_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["subject_categories"]:
                sub_cat_value[_relation][_sub_cat_id] = self._results["added_rule"][_relation][_sub_cat_id]

            for _obj_cat_id in self.extension.get_meta_rule()["sub_meta_rules"][_relation]["object_categories"]:
                obj_cat_value[_relation][_obj_cat_id] = self._results["added_rule"][_relation][_obj_cat_id]

        self.assertEqual(self.extension.del_rule(sub_cat_value, obj_cat_value), self._results['rules'])
        print("[test_add_rule] del an existing  rule ---------------- OK ")

"""
    def test_get_subjects(self):
        print("[test_get_subjects]----------------: ", self.extension.get_subjects())
        self.assertIsInstance(self.extension.get_subjects(), list)

    def test_add_subject(self):
        print("[test_add_subject]----------------: ", self.extension.get_subjects())
        self.extension.add_subject("aaaa")
        print("[test_add_subject]----------------: ", self.extension.get_subjects())
        self.extension.del_subject("aaaa")

    def test_del_subject(self):
        self.extension.add_subject("aaaa")
        print("[test_del_subject]----------------: ", self.extension.get_subjects())
        self.extension.del_subject("aaaa")
        print("[test_del_subject]----------------: ", self.extension.get_subjects())

    def test_get_objects(self):
        print("[test_get_objects]----------------: ", self.extension.get_objects())
        self.assertIsInstance(self.extension.get_objects(), list)

    def test_add_object(self):
        print("[test_add_object]----------------: ", self.extension.get_objects())
        self.extension.add_object("bbbb")
        print("[test_add_object]----------------: ", self.extension.get_objects())
        self.extension.del_object("bbbb")

    def test_del_object(self):
        self.extension.add_object("bbbb")
        print("[test_del_object]----------------: ", self.extension.get_objects())
        self.extension.del_object("bbbb")
        print("[test_del_object]----------------: ", self.extension.get_objects())

    def test_get_subject_assignments(self):
        _sub_cat_id = self.extension.get_subject_categories()[0]
        print("[test_get_subject_assignments] for ", _sub_cat_id, "----------------: ",
              self.extension.get_subject_assignments(_sub_cat_id))
        self.assertIsInstance(self.extension.get_subject_assignments(_sub_cat_id), dict)

    def test_add_subject_assignment(self):
        _sub_cat_id = self.extension.get_subject_categories()[0]
        print("[test_add_subject_assignment] for ", _sub_cat_id, "----------------: ",
              self.extension.get_subject_assignments(_sub_cat_id))
        self.extension.add_subject_assignment(_sub_cat_id, "userx", "aaaa")
        self.extension.add_subject_assignment(_sub_cat_id, "userx", "aaaa2")
        self.extension.add_subject_assignment(_sub_cat_id, "user2", "aaaa3")
        print("[test_add_subject_assignment] for ", _sub_cat_id, "----------------: ",
              self.extension.get_subject_assignments(_sub_cat_id))
        self.extension.del_subject_assignment(_sub_cat_id, "userx", "aaaa")
        self.extension.del_subject_assignment(_sub_cat_id, "userx", "aaaa2")
        self.extension.del_subject_assignment(_sub_cat_id, "user2", "aaaa3")

    def test_del_subject_assignment(self):
        _sub_cat_id = self.extension.get_subject_categories()[0]
        self.extension.add_subject_assignment(_sub_cat_id, "userx", "aaaa")
        self.extension.add_subject_assignment(_sub_cat_id, "userx", "aaaa2")
        self.extension.add_subject_assignment(_sub_cat_id, "user2", "aaaa3")
        print("[test_del_subject_assignment] for ", _sub_cat_id, "----------------: ",
              self.extension.get_subject_assignments(_sub_cat_id))
        self.extension.del_subject_assignment(_sub_cat_id, "userx", "aaaa")
        self.extension.del_subject_assignment(_sub_cat_id, "userx", "aaaa2")
        self.extension.del_subject_assignment(_sub_cat_id, "user2", "aaaa3")
        print("[test_del_subject_assignment] for ", _sub_cat_id, "----------------: ",
              self.extension.get_subject_assignments(_sub_cat_id))

    def test_get_subject_category_attr(self):
        _sub_cat_id = self.extension.get_subject_categories()[0]
        _subject_id = self.extension.get_subjects()[0]
        print("[test_get_subject_category_attr] for ", _sub_cat_id, _subject_id, "----------------: ",
              self.extension.get_subject_category_attr(_sub_cat_id, _subject_id))
        self.assertIsInstance(self.extension.get_subject_category_attr(_sub_cat_id, _subject_id), list)

    def test_get_object_assignments(self):
        _obj_cat_id = self.extension.get_object_categories()[0]
        print("[test_get_object_assignments] for ", _obj_cat_id, "----------------: ",
              self.extension.get_object_assignments(_obj_cat_id))
        self.assertIsInstance(self.extension.get_object_assignments(_obj_cat_id), dict)

    def test_add_object_assignment(self):
        _obj_cat_id = self.extension.get_object_categories()[0]
        print("[test_add_object_assignment] for ", _obj_cat_id, "----------------: ",
              self.extension.get_object_assignments(_obj_cat_id))
        self.extension.add_object_assignment(_obj_cat_id, "vmx", "bbbb")
        self.extension.add_object_assignment(_obj_cat_id, "vmx", "bbbb2")
        self.extension.add_object_assignment(_obj_cat_id, "vm3", "bbbb3")
        print("[test_add_object_assignment] for ", _obj_cat_id, "----------------: ",
              self.extension.get_object_assignments(_obj_cat_id))
        self.extension.del_object_assignment(_obj_cat_id, "vmx", "bbbb")
        self.extension.del_object_assignment(_obj_cat_id, "vmx", "bbbb2")
        self.extension.del_object_assignment(_obj_cat_id, "vm3", "bbbb3")

    def test_del_object_assignment(self):
        _obj_cat_id = self.extension.get_object_categories()[0]
        self.extension.add_object_assignment(_obj_cat_id, "vmx", "bbbb")
        self.extension.add_object_assignment(_obj_cat_id, "vm3", "bbbb3")
        print("[test_del_object_assignment] for ", _obj_cat_id, "----------------: ",
              self.extension.get_object_assignments(_obj_cat_id))
        self.extension.del_object_assignment(_obj_cat_id, "vmx", "bbbb")
        self.extension.del_object_assignment(_obj_cat_id, "vm3", "bbbb3")
        print("[test_del_object_assignment] for ", _obj_cat_id, "----------------: ",
              self.extension.get_object_assignments(_obj_cat_id))

    def test_get_object_category_attr(self):
        _obj_cat_id = self.extension.get_object_categories()[0]
        _object_id = self.extension.get_objects()[0]
        print("[test_get_object_category_attr] for ", _obj_cat_id, _object_id, "----------------: ",
              self.extension.get_object_category_attr(_obj_cat_id, _object_id))
        self.assertIsInstance(self.extension.get_object_category_attr(_obj_cat_id, _object_id), list)

    def test_get_data(self):
        print("[test_get_data]----------------: ", self.extension.get_data().keys())

    def test_set_data(self):
        _extension = Extension()
        if self.extension.get_type() == "authz":
            _extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001/admin')
        elif self.extension.get_type() == "admin":
            _extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001/authz')
        _extension.load_from_json(_extension_setting_abs_dir)
        _data = _extension.get_data()
        self.extension.set_data(_data)
        print("[test_set_data]----------------: ", self.extension.get_data().keys())

    def test_create_requesting_collaboration(self):
        _vent1 = VirtualEntity("trust")
        _subs = ["user1", "user2"]

        print("[test_create_requesting_collaboration] get_subjects ----------------: ", self.extension.get_subjects())

        for _sc in self.extension.get_subject_categories():
            print("[test_create_requesting_collaboration] get_subject_category_values ----------------: ",
                  self.extension.get_subject_category_values(_sc))
            print("[test_create_requesting_collaboration] get_subject_assignments ----------------: ",
                  self.extension.get_subject_assignments(_sc))

        print("[test_create_requesting_collaboration] get_objects ----------------: ",
              self.extension.get_objects())

        for _oc in self.extension.get_object_categories():
            print("[test_create_requesting_collaboration] get_object_category_values ----------------: ",
                  self.extension.get_object_category_values(_oc))
            print("[test_create_requesting_collaboration] get_object_assignments ----------------: ",
                  self.extension.get_object_assignments(_oc))

        print("[test_create_requesting_collaboration] get_rules ----------------: ", self.extension.get_rules())

        self.extension.create_requesting_collaboration(_subs, _vent1, "read")

        print("[test_create_requesting_collaboration] get_subjects ----------------: ", self.extension.get_subjects())

        for _sc in self.extension.get_subject_categories():
            print("[test_create_requesting_collaboration] get_subject_category_values ----------------: ",
                  self.extension.get_subject_category_values(_sc))
            print("[test_create_requesting_collaboration] get_subject_assignments ----------------: ",
                  self.extension.get_subject_assignments(_sc))

        print("[test_create_requesting_collaboration] get_objects ----------------: ",
              self.extension.get_objects())

        for _oc in self.extension.get_object_categories():
            print("[test_create_requesting_collaboration] get_object_category_values ----------------: ",
                  self.extension.get_object_category_values(_oc))
            print("[test_create_requesting_collaboration] get_object_assignments ----------------: ",
                  self.extension.get_object_assignments(_oc))

        print("[test_create_requesting_collaboration] get_rules ----------------: ", self.extension.get_rules())

    def test_create_requested_collaboration(self):
        _vent1 = VirtualEntity("trust")
        _objs = ["vm1", "vm2"]

        print("[test_create_requested_collaboration] get_subjects ----------------: ", self.extension.get_subjects())

        for _sc in self.extension.get_subject_categories():
            print("[test_create_requested_collaboration] get_subject_category_values ----------------: ",
                  self.extension.get_subject_category_values(_sc))
            print("[test_create_requested_collaboration] get_subject_assignments ----------------: ",
                  self.extension.get_subject_assignments(_sc))

        print("[test_create_requested_collaboration] get_objects ----------------: ",
              self.extension.get_objects())

        for _oc in self.extension.get_object_categories():
            print("[test_create_requested_collaboration] get_object_category_values ----------------: ",
                  self.extension.get_object_category_values(_oc))
            print("[test_create_requested_collaboration] get_object_assignments ----------------: ",
                  self.extension.get_object_assignments(_oc))

        print("[test_create_requested_collaboration] get_rules ----------------: ", self.extension.get_rules())

        self.extension.create_requested_collaboration(_vent1, _objs, "read")

        print("[test_create_requested_collaboration] get_subjects ----------------: ", self.extension.get_subjects())

        for _sc in self.extension.get_subject_categories():
            print("[test_create_requested_collaboration] get_subject_category_values ----------------: ",
                  self.extension.get_subject_category_values(_sc))
            print("[test_create_requested_collaboration] get_subject_assignments ----------------: ",
                  self.extension.get_subject_assignments(_sc))

        print("[test_create_requested_collaboration] get_objects ----------------: ",
              self.extension.get_objects())

        for _oc in self.extension.get_object_categories():
            print("[test_create_requested_collaboration] get_object_category_values ----------------: ",
                  self.extension.get_object_category_values(_oc))
            print("[test_create_requested_collaboration] get_object_assignments ----------------: ",
                  self.extension.get_object_assignments(_oc))

        print("[test_create_requested_collaboration] get_rules ----------------: ", self.extension.get_rules())
"""

if __name__ == "__main__":
    unittest.main()