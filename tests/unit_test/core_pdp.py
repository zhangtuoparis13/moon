"""
unit test for moon/core/pdp
"""

import unittest
import pkg_resources
import argparse
from moon.core.pdp.intra_extension import IntraExtension
from moon.core.pdp.extension import Extension


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


class TestCorePDPExtension(unittest.TestCase):

    def setUp(self):
        self.extension = Extension()
        # extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001/authz')
        extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001/admin')
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
        # sub_cat_value = {"subject_security_level": "xxxx"}
        # obj_cat_value = {"object_security_level": "yyyy", "action": "zzz"}
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
        print("[test_get_data]----------------: ", self.extension.get_data())

    def test_set_data(self):
        _extension = Extension()
        extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001/authz')
        _extension.load_from_json(extension_setting_abs_dir)
        _data = _extension.get_data()
        self.extension.set_data(_data)
        print("[test_set_data]----------------: ", self.extension.get_data())

# class TestCorePDPIntraExtension(unittest.TestCase):
#
#     def setUp(self):
#         self.intra_extension = IntraExtension()
#         intra_extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001')
#         self.intra_extension.load_from_json(intra_extension_setting_abs_dir)
#
#     def tearDown(self):
#         pass
#
#     def test_get_uuid(self):
#         print("[test_get_uuid]----------------: ", self.intra_extension.get_uuid())
#
#     def test_get_tenant_uuid(self):
#         print("[test_get_tenant_uuid]----------------: ", self.intra_extension.get_tenant_uuid())
#
#     def test_authz(self):
#         _type = 'authz'
#         for i in range(len(INTRAREQUESTS[_type])):
#             sub = INTRAREQUESTS[_type][i]['subject']
#             obj = INTRAREQUESTS[_type][i]['object']
#             act = INTRAREQUESTS[_type][i]['action']
#             _result = INTRAREQUESTS[_type][i]['_result']
#             self.assertIs(self.intra_extension.authz(sub, obj, act), _result)
#
#     def test_admin(self):
#         _type = 'admin'
#         for i in range(len(INTRAREQUESTS[_type])):
#             sub = INTRAREQUESTS[_type][i]['subject']
#             obj = INTRAREQUESTS[_type][i]['object']
#             act = INTRAREQUESTS[_type][i]['action']
#             _result = INTRAREQUESTS[_type][i]['_result']
#             self.assertIs(self.intra_extension.admin(sub, obj, act), _result)
#
#     def test_get_data(self):
#         print("[test_get_tenant_uuid]----------------: ")


class TestCorePDPInterExtension(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_name(self):
        pass


class TestCorePDPSyncdb(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_name(self):
        pass


class TestCorePDPCore(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_name(self):
        pass


if __name__ == "__main__":
    unittest.main()


    # parser = argparse.ArgumentParser()
    # parser.add_argument('--extension', action='store_true')
    # parser.add_argument('--intra_extension', action='store', choices=('extension', 'authz', 'admin', 'intra'))
    # parser.add_argument('--inter_extension', action='store_true')
    # parser.add_argument('--core', action='store_true')
    # args = parser.parse_args()
    #
    # if args.core:
    #     pass
    #
    # if args.intra_extension:
    #     print('testing core/pdp/intra_extension.py/'+args.intra_extension+' function starting ...')
    #
    #     if args.intra_extension == 'extension':
    #         intra_extensions = get_intra_extensions()
    #         intra_extensions.install_intra_extension_from_json('core/pdp/extension_setting/mls001')
    #         for ixk in intra_extensions.get_installed_intra_extensions():
    #             for i in range(len(REQUESTS['authz'])):
    #                 sub = REQUESTS['authz'][i]['subject']
    #                 obj = REQUESTS['authz'][i]['object']
    #                 act = REQUESTS['authz'][i]['action']
    #                 result = intra_extensions.get_installed_intra_extensions()[ixk].authz(sub, obj, act)
    #                 print('xxxxxxxx test authz: ', result)
    #
    #             for i in range(len(REQUESTS['admin'])):
    #                 sub = REQUESTS['admin'][i]['subject']
    #                 obj = REQUESTS['admin'][i]['object']
    #                 act = REQUESTS['admin'][i]['action']
    #                 result = intra_extensions.get_installed_intra_extensions()[ixk].admin(sub, obj, act)
    #                 print('yyyyyyyy test admin: ', result)
    #
    #             intra_extensions.get_installed_intra_extensions()[ixk].sync()
    #
    #     elif args.intra_extension == 'authz':
    #         print ('authz option is: '+args.intra_extension)
    #     elif args.intra_extension == 'admin':
    #         pass
    #     elif args.intra_extension == 'intra':
    #         pass
    #
    #     print('testing core/pdp/intra_extension.py/'+args.intra_extension+' function succeed')
    #
    # if args.inter_extension:
    #     pass
    #
    # if args.core:
    #     pass