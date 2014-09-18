"""
unit test for moon/core/pdp
"""

import unittest
import pkg_resources
from moon.core.pdp.extension import Extension
from moon.core.pdp.sync_db import IntraExtensionSyncer, IntraExtensionsSyncer
from moon.core.pdp.intra_extension import IntraExtension
from moon.core.pdp.core import IntraExtensions
from moon.core.pdp.inter_extension import VirtualEntity, InterExtension


REQUESTS = {
    'authz': [
        {
            'subject': 'user1',
            'object': 'vm1',
            'action': 'read',
            '_result': 'KO'
        },
        {
            'subject': 'user1',
            'object': 'vm2',
            'action': 'read',
            '_result': 'OK'
        },
        {
            'subject': 'user1',
            'object': 'vm3',
            'action': 'write',
            '_result': 'KO'
        }
    ],
    'admin': [
        {
            'subject': 'user1',
            'object': 'subjects',
            'action': 'read',
            '_result': 'OK'
        },
        {
            'subject': 'user2',
            'object': 'subjects',
            'action': 'write',
            '_result': 'KO'
        }
    ]
}

INTRAREQUESTS = {
    'authz': [
        {
            'subject': 'user1',
            'object': 'vm1',
            'action': 'read',
            '_result': 'KO'
        },
        {
            'subject': 'user1',
            'object': 'vm2',
            'action': 'read',
            '_result': 'OK'
        },
        {
            'subject': 'user1',
            'object': 'vm3',
            'action': 'write',
            '_result': 'KO'
        },
        {
            'subject': 'userx',
            'object': 'vm3',
            'action': 'write',
            '_result': 'Out of Scope'
        }
    ],
    'admin': [
        {
            'subject': 'user1',
            'object': 'subjects',
            'action': 'read',
            '_result': 'OK'
        },
        {
            'subject': 'user2',
            'object': 'subjects',
            'action': 'write',
            '_result': 'KO'
        },
        {
            'subject': 'userx',
            'object': 'subjects',
            'action': 'write',
            '_result': 'Out of Scope'
        }
    ]
}

"""
class TestCorePDPExtension(unittest.TestCase):

    def setUp(self):
        self.extension = Extension()
        extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001/authz')
        # extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001/admin')
        self.extension.load_from_json(extension_setting_abs_dir)

    def tearDown(self):
        pass

    def test_get_name(self):
        print("[test_get_name]----------------: ", self.extension.get_name())
        self.assertIsInstance(self.extension.get_name(), unicode)

    def test_get_type(self):
        print("[test_get_type]----------------: ", self.extension.get_type())
        self.assertIsInstance(self.extension.get_type(), unicode)

    def test_authz(self):
        _type = self.extension.get_type()
        for i in range(len(REQUESTS[_type])):
            sub = REQUESTS[_type][i]['subject']
            obj = REQUESTS[_type][i]['object']
            act = REQUESTS[_type][i]['action']
            _result = REQUESTS[_type][i]['_result']
            self.assertIs(self.extension.authz(sub, obj, act), _result)

    def test_get_subject_categories(self):
        print("[test_get_subject_categories]----------------: ", self.extension.get_subject_categories())
        self.assertIsInstance(self.extension.get_subject_categories(), list)

    def test_add_subject_category(self):
        print("[test_add_subject_category]----------------: ", self.extension.get_subject_categories())
        self.extension.add_subject_category("ssss")
        print("[test_add_subject_category]----------------: ", self.extension.get_subject_categories())
        self.extension.del_subject_category("ssss")

    def test_del_subject_category(self):
        self.extension.add_subject_category("ssss")
        print("[test_del_subject_category]----------------: ", self.extension.get_subject_categories())
        self.extension.del_subject_category("ssss")
        print("[test_del_subject_category]----------------: ", self.extension.get_subject_categories())

    def test_get_object_categories(self):
        print("[test_get_object_categories]----------------: ", self.extension.get_object_categories())
        self.assertIsInstance(self.extension.get_object_categories(), list)

    def test_add_object_category(self):
        print("[test_add_object_category]----------------: ", self.extension.get_object_categories())
        self.extension.add_object_category("oooo")
        print("[test_add_object_category]----------------: ", self.extension.get_object_categories())
        self.extension.del_object_category("oooo")

    def test_del_object_category(self):
        self.extension.add_object_category("oooo")
        print("[test_del_object_category]----------------: ", self.extension.get_object_categories())
        self.extension.del_object_category("oooo")
        print("[test_del_object_category]----------------: ", self.extension.get_object_categories())

    def test_get_subject_category_values(self):
        _sub_cat_id = self.extension.get_subject_categories()[0]
        print("[test_get_subject_category_values] for ", _sub_cat_id, "----------------: ",
              self.extension.get_subject_category_values(_sub_cat_id))
        self.assertIsInstance(self.extension.get_subject_category_values(_sub_cat_id), list)

    def test_add_subject_category_value(self):
        _sub_cat_id = self.extension.get_subject_categories()[0]
        print("[test_add_subject_category_value] for ", _sub_cat_id, "----------------: ",
              self.extension.get_subject_category_values(_sub_cat_id))
        self.extension.add_subject_category_value(_sub_cat_id, "xxxx")
        print("[test_add_subject_category_value] for ", _sub_cat_id, "----------------: ",
              self.extension.get_subject_category_values(_sub_cat_id))
        self.extension.del_subject_category_value(_sub_cat_id, "xxxx")

    def test_del_subject_category_value(self):
        _sub_cat_id = self.extension.get_subject_categories()[0]
        self.extension.add_subject_category_value(_sub_cat_id, "xxxx")
        print("[test_del_subject_category_value] for ", _sub_cat_id, "----------------: ",
              self.extension.get_subject_category_values(_sub_cat_id))
        self.extension.del_subject_category_value(_sub_cat_id, "xxxx")
        print("[test_del_subject_category_value] for ", _sub_cat_id, "----------------: ",
              self.extension.get_subject_category_values(_sub_cat_id))

    def test_get_object_category_values(self):
        _obj_cat_id = self.extension.get_object_categories()[0]
        print("[test_get_object_category_values] for ", _obj_cat_id, "----------------: ",
              self.extension.get_object_category_values(_obj_cat_id))
        self.assertIsInstance(self.extension.get_object_category_values(_obj_cat_id), list)

    def test_add_object_category_value(self):
        _obj_cat_id = self.extension.get_object_categories()[0]
        print("[test_add_object_category_value] for ", _obj_cat_id, "----------------: ",
              self.extension.get_object_category_values(_obj_cat_id))
        self.extension.add_object_category_value(_obj_cat_id, "yyyy")
        print("[test_add_object_category_value] for ", _obj_cat_id, "----------------: ",
              self.extension.get_object_category_values(_obj_cat_id))
        self.extension.del_object_category_value(_obj_cat_id, "yyyy")

    def test_del_object_category_value(self):
        _obj_cat_id = self.extension.get_object_categories()[0]
        self.extension.add_object_category_value(_obj_cat_id, "yyyy")
        print("[test_del_object_category_value] for ", _obj_cat_id, "----------------: ",
              self.extension.get_object_category_values(_obj_cat_id))
        self.extension.del_object_category_value(_obj_cat_id, "yyyy")
        print("[test_del_object_category_value] for ", _obj_cat_id, "----------------: ",
              self.extension.get_object_category_values(_obj_cat_id))

    def test_get_rules(self):
        print("[test_get_rules]----------------: ", self.extension.get_rules())
        self.assertIsInstance(self.extension.get_rules(), list)
        self.assertIsInstance(self.extension.get_rules()[0], list)

    def test_add_rule(self):
        print("[test_add_rule]----------------: ", self.extension.get_rules())

        if self.extension.get_type() == "authz":
            sub_cat_value = {self.extension.get_subject_categories()[0]: "xxxx"}
            obj_cat_value = {self.extension.get_object_categories()[0]: "yyy", self.extension.get_object_categories()[1]: "zzz"}
        elif self.extension.get_type() == "admin":
            sub_cat_value = {self.extension.get_subject_categories()[0]: "xxxx"}
            obj_cat_value = {self.extension.get_object_categories()[0]: "yyyy", self.extension.get_object_categories()[1]: "zzz"}

        self.extension.add_rule(sub_cat_value, obj_cat_value)

        print("[test_add_rule]----------------: ", self.extension.get_rules())

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
"""
class TestCorePDPIntraExtension(unittest.TestCase):

    def setUp(self):
        self.intra_extension = IntraExtension()
        intra_extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001')
        self.intra_extension.load_from_json(intra_extension_setting_abs_dir)

    def tearDown(self):
        pass

    def test_get_uuid(self):
        print("[test_get_uuid]----------------: ", self.intra_extension.get_uuid())

    def test_get_tenant_uuid(self):
        print("[test_get_tenant_uuid]----------------: ", self.intra_extension.get_tenant_uuid())

    def test_authz(self):
        _type = 'authz'
        for i in range(len(INTRAREQUESTS[_type])):
            sub = INTRAREQUESTS[_type][i]['subject']
            obj = INTRAREQUESTS[_type][i]['object']
            act = INTRAREQUESTS[_type][i]['action']
            _result = INTRAREQUESTS[_type][i]['_result']
            self.assertEqual(self.intra_extension.authz(sub, obj, act), _result)

    def test_admin(self):
        _type = 'admin'
        for i in range(len(INTRAREQUESTS[_type])):
            sub = INTRAREQUESTS[_type][i]['subject']
            obj = INTRAREQUESTS[_type][i]['object']
            act = INTRAREQUESTS[_type][i]['action']
            _result = INTRAREQUESTS[_type][i]['_result']
            self.assertEqual(self.intra_extension.admin(sub, obj, act), _result)

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

    def test_create_requesting_collaboration(self):
        _vent = VirtualEntity("trust")
        _sub_list = ["user1", "user2"]
        type = "trust"

        if type == "trust":
            _extension = self.intra_extension.intra_extension_authz
        elif type == "coordinate":
            _extension = self.intra_extension.intra_extension_admin

        print("[test_create_requesting_collaboration] get_subjects ----------------: ", _extension.get_subjects())
        for _sc in _extension.get_subject_categories():
            print("[test_create_requesting_collaboration] get_subject_category_values ----------------: ",
                  _extension.get_subject_category_values(_sc))
            print("[test_create_requesting_collaboration] get_subject_assignments ----------------: ",
                  _extension.get_subject_assignments(_sc))
        print("[test_create_requesting_collaboration] get_objects ----------------: ",
              _extension.get_objects())
        for _oc in _extension.get_object_categories():
            print("[test_create_requesting_collaboration] get_object_category_values ----------------: ",
                  _extension.get_object_category_values(_oc))
            print("[test_create_requesting_collaboration] get_object_assignments ----------------: ",
                  _extension.get_object_assignments(_oc))
        print("[test_create_requesting_collaboration] get_rules ----------------: ", _extension.get_rules())

        _dict = _extension.create_requesting_collaboration(_sub_list, _vent.get_uuid(), "read")

        print("[test_create_requesting_collaboration] get_subjects ----------------: ", _extension.get_subjects())
        for _sc in _extension.get_subject_categories():
            print("[test_create_requesting_collaboration] get_subject_category_values ----------------: ",
                  _extension.get_subject_category_values(_sc))
            print("[test_create_requesting_collaboration] get_subject_assignments ----------------: ",
                  _extension.get_subject_assignments(_sc))
        print("[test_create_requesting_collaboration] get_objects ----------------: ",
              _extension.get_objects())
        for _oc in _extension.get_object_categories():
            print("[test_create_requesting_collaboration] get_object_category_values ----------------: ",
                  _extension.get_object_category_values(_oc))
            print("[test_create_requesting_collaboration] get_object_assignments ----------------: ",
                  _extension.get_object_assignments(_oc))
        print("[test_create_requesting_collaboration] get_rules ----------------: ", _extension.get_rules())

        _extension.destory_requesting_collaboration(_vent.get_uuid(), _sub_list, _dict["subject_category_value_dict"], _dict["object_category_value_dict"])

        print("[test_create_requesting_collaboration] get_subjects ----------------: ", _extension.get_subjects())
        for _sc in _extension.get_subject_categories():
            print("[test_create_requesting_collaboration] get_subject_category_values ----------------: ",
                  _extension.get_subject_category_values(_sc))
            print("[test_create_requesting_collaboration] get_subject_assignments ----------------: ",
                  _extension.get_subject_assignments(_sc))
        print("[test_create_requesting_collaboration] get_objects ----------------: ",
              _extension.get_objects())
        for _oc in _extension.get_object_categories():
            print("[test_create_requesting_collaboration] get_object_category_values ----------------: ",
                  _extension.get_object_category_values(_oc))
            print("[test_create_requesting_collaboration] get_object_assignments ----------------: ",
                  _extension.get_object_assignments(_oc))
        print("[test_create_requesting_collaboration] get_rules ----------------: ", _extension.get_rules())

    def test_create_requested_collaboration(self):
        _vent = VirtualEntity("trust")
        _obj_list = ["vm1", "vm2"]
        type = "trust"

        if type == "trust":
            _extension = self.intra_extension.intra_extension_authz
        elif type == "coordinate":
            _extension = self.intra_extension.intra_extension_admin

        print("[test_create_requested_collaboration] get_subjects ----------------: ", _extension.get_subjects())
        for _sc in _extension.get_subject_categories():
            print("[test_create_requested_collaboration] get_subject_category_values ----------------: ",
                  _extension.get_subject_category_values(_sc))
            print("[test_create_requested_collaboration] get_subject_assignments ----------------: ",
                  _extension.get_subject_assignments(_sc))
        print("[test_create_requested_collaboration] get_objects ----------------: ",
              _extension.get_objects())
        for _oc in _extension.get_object_categories():
            print("[test_create_requested_collaboration] get_object_category_values ----------------: ",
                  _extension.get_object_category_values(_oc))
            print("[test_create_requested_collaboration] get_object_assignments ----------------: ",
                  _extension.get_object_assignments(_oc))
        print("[test_create_requested_collaboration] get_rules ----------------: ", _extension.get_rules())

        _dict = _extension.create_requested_collaboration(_vent.get_uuid(), _obj_list, "read")

        print("[test_create_requested_collaboration] get_subjects ----------------: ", _extension.get_subjects())
        for _sc in _extension.get_subject_categories():
            print("[test_create_requested_collaboration] get_subject_category_values ----------------: ",
                  _extension.get_subject_category_values(_sc))
            print("[test_create_requested_collaboration] get_subject_assignments ----------------: ",
                  _extension.get_subject_assignments(_sc))
        print("[test_create_requested_collaboration] get_objects ----------------: ",
              _extension.get_objects())
        for _oc in _extension.get_object_categories():
            print("[test_create_requested_collaboration] get_object_category_values ----------------: ",
                  _extension.get_object_category_values(_oc))
            print("[test_create_requested_collaboration] get_object_assignments ----------------: ",
                  _extension.get_object_assignments(_oc))
        print("[test_create_requested_collaboration] get_rules ----------------: ", _extension.get_rules())


        _extension.destory_requested_collaboration(_vent.get_uuid(), _dict["subject_category_value_dict"], _obj_list, _dict["object_category_value_dict"])

        print("[test_create_requested_collaboration] get_subjects ----------------: ", _extension.get_subjects())
        for _sc in _extension.get_subject_categories():
            print("[test_create_requested_collaboration] get_subject_category_values ----------------: ",
                  _extension.get_subject_category_values(_sc))
            print("[test_create_requested_collaboration] get_subject_assignments ----------------: ",
                  _extension.get_subject_assignments(_sc))
        print("[test_create_requested_collaboration] get_objects ----------------: ",
              _extension.get_objects())
        for _oc in _extension.get_object_categories():
            print("[test_create_requested_collaboration] get_object_category_values ----------------: ",
                  _extension.get_object_category_values(_oc))
            print("[test_create_requested_collaboration] get_object_assignments ----------------: ",
                  _extension.get_object_assignments(_oc))
        print("[test_create_requested_collaboration] get_rules ----------------: ", _extension.get_rules())
"""

class TestCorePDPInterExtension(unittest.TestCase):

    def setUp(self):
        self.requesting_intra_extension = IntraExtension()
        self.requested_intra_extension = IntraExtension()
        intra_extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001')
        self.requesting_intra_extension.load_from_json(intra_extension_setting_abs_dir)
        self.requested_intra_extension.load_from_json(intra_extension_setting_abs_dir)
        self.inter_extension = InterExtension(self.requesting_intra_extension, self.requested_intra_extension)

    def tearDown(self):
        pass

    def test_create_destroy_collaboration(self):
        _sub_list = ['user1', 'user2']
        _obj_list = ['vm2', 'vm3']
        _act = "read"

        _vent_uuid = self.inter_extension.create_collaboration("trust", _sub_list, _obj_list, _act)

        print("[test_create_collaboration]----------------: ", self.inter_extension.get_vent_data_dict(_vent_uuid))

        print("[test_create_collaboration] authz ----------------: ", self.inter_extension.authz('user1', 'vm2', 'read'))

        print("[test_destory_collaboration] vents ----------------: ", self.inter_extension.get_vents())

        self.inter_extension.destroy_collaboration(_vent_uuid)

        print("[test_destory_collaboration] vents ----------------: ", self.inter_extension.get_vents())


"""
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


class TestCorePDPCore(unittest.TestCase):

    def setUp(self):
        self.intra_extensions = IntraExtensions()

    def tearDown(self):
        pass

    def test_intra_extensions_get_installed_intra_extensions(self):
        print("[test_intra_extensions_get_installed_intra_extensions]----------------: ",
              self.intra_extensions.get_installed_intra_extensions())

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