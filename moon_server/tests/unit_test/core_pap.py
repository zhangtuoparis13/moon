"""
unit test for moon/core/pap
"""

import unittest
import pkg_resources
from moon_server.core.pdp.core import IntraExtension
from moon_server.core.pap import get_pap
from moon_server.core.pip import get_pip
from moon_server.tests.unit_test.samples.super_extension import results as super_extension_results
from moon_server.tests.unit_test.samples.mls001.core import results as mls001_results

class TestCorePAPIntraExtensions(unittest.TestCase):

    def setUp(self):
        extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001')
        self.pap = get_pap()
        self.pip = get_pip()
        self.pap.install_intra_extension_from_json("admin", extension_setting_dir=extension_setting_abs_dir)
        self.ext_uuid = self.pap.get_intra_extensions("admin").keys()[0]
        # self.extension = IntraExtension()
        # print(self.extension.get_uuid())
        # print(self.pap.get_intra_extensions().keys())

    def tearDown(self):
        self.ext_uuid = None

    def test_subjects(self):
        subjects = self.pap.get_subjects(self.ext_uuid, "user1")
        self.assertIsInstance(subjects, list)
        self.assertIn("user1", subjects)
        #Test adding a new subject
        user3 = {
                "name": "user3",
                'domain': "Default",
                'enabled': True,
                'project': "admin",
                'password': "user3",
                'description': "test user"}
        subject_id = self.pap.add_subject(self.ext_uuid, "user1", subject=user3)
        subjects = self.pap.get_subjects(self.ext_uuid, "user1")
        self.assertIsInstance(subjects, list)
        self.assertIn(subject_id, subjects)
        self.pap.del_subject(self.ext_uuid, "user1", subject_id=subject_id)
        subjects = self.pap.get_subjects(self.ext_uuid, "user1")
        self.assertIsInstance(subjects, list)
        self.assertNotIn(subject_id, subjects)

    def test_subjects_user_error(self):
        subjects = self.pap.get_subjects(self.ext_uuid, "userX")
        self.assertEqual(subjects, None)
        #Test adding a new subject with a wrong user
        user3 = {
            "name": "user3",
            'domain': "Default",
            'enabled': True,
            'project': "admin",
            'password': "user3",
            'description': "test user"}
        subject_id = self.pap.add_subject(self.ext_uuid, "user2", subject=user3)
        subjects = list(self.pap.get_subjects(self.ext_uuid, "user1"))
        sbj = list(self.pip.get_subjects())
        self.assertIsInstance(subjects, list)
        self.assertNotIn(subject_id, subjects)
        self.pap.del_subject(self.ext_uuid, "user2", subject_id=sbj[0]["uuid"])
        subjects = list(self.pap.get_subjects(self.ext_uuid, "user1"))
        self.assertIsInstance(subjects, list)
        self.assertIn(sbj[0]["uuid"], subjects)

    def test_objects(self):
        objects = self.pap.get_objects(self.ext_uuid, "user1")
        self.assertIsInstance(objects, list)
        self.assertIn("vm1", objects)
        #Test adding a new object
        server = {
            "name": "TestVMForMoon",
            "image_name": "Cirros3.2",
            "flavor_name": "m1.nano"
        }
        images = map(lambda x: x["name"], get_pip().get_images())
        for _img in images:
            if "irros" in _img:
                server["image_name"] = _img
        object_uuid = self.pap.add_object(self.ext_uuid, "user1", object=server)
        objects = self.pap.get_objects(self.ext_uuid, "user1")
        self.assertIsInstance(objects, list)
        self.assertIn(object_uuid, objects)
        self.pap.del_object(self.ext_uuid, "user1", object_id=object_uuid)
        objects = self.pap.get_objects(self.ext_uuid, "user1")
        self.assertIsInstance(objects, list)
        self.assertNotIn(object_uuid, objects)

    def test_objects_user_error(self):
        objects = self.pap.get_objects(self.ext_uuid, "user3")
        self.assertEqual(objects, None)
        server = {
            "name": "TestVMForMoon",
            "image_name": "Cirros3.2",
            "flavor_name": "m1.nano"
        }
        object_uuid = self.pap.add_object(self.ext_uuid, "user2", object=server)
        objects = list(self.pap.get_objects(self.ext_uuid, "user1"))
        object_uuid_to_delete = objects[0]
        self.assertIsInstance(objects, list)
        self.assertNotIn(object_uuid, objects)
        self.pap.del_object(self.ext_uuid, "user2", object_id=object_uuid_to_delete)
        objects = self.pap.get_objects(self.ext_uuid, "user1")
        self.assertIsInstance(objects, list)
        self.assertIn(object_uuid_to_delete, objects)

    def test_subject_categories(self):
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user1")
        self.assertIsInstance(subject_categories, list)
        self.assertIn("subject_security_level", subject_categories)
        self.pap.add_subject_category(self.ext_uuid, "user1", category_id="tmp_cat")
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user1")
        self.assertIsInstance(subject_categories, list)
        self.assertIn("tmp_cat", subject_categories)
        self.pap.del_subject_category(self.ext_uuid, "user1", category_id="tmp_cat")
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user1")
        self.assertIsInstance(subject_categories, list)
        self.assertNotIn("tmp_cat", subject_categories)

    def test_subject_categories_user_error(self):
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user3")
        self.assertEqual(subject_categories, None)
        self.pap.add_subject_category(self.ext_uuid, "user2", category_id="tmp_cat")
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user1")
        self.assertIsInstance(subject_categories, list)
        self.assertNotIn("tmp_cat", subject_categories)
        self.pap.del_subject_category(self.ext_uuid, "user2", category_id="subject_security_level")
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user1")
        self.assertIsInstance(subject_categories, list)
        self.assertIn("subject_security_level", subject_categories)

    def test_object_categories(self):
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user1")
        self.assertIsInstance(object_categories, list)
        self.assertIn("object_security_level", object_categories)
        self.assertIn("action", object_categories)
        self.pap.add_object_category(self.ext_uuid, "user1", category_id="tmp_cat")
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user1")
        self.assertIsInstance(object_categories, list)
        self.assertIn("tmp_cat", object_categories)
        self.pap.del_object_category(self.ext_uuid, "user1", category_id="tmp_cat")
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user1")
        self.assertIsInstance(object_categories, list)
        self.assertNotIn("tmp_cat", object_categories)

    def test_object_categories_user_error(self):
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user3")
        self.assertEqual(object_categories, None)
        self.pap.add_object_category(self.ext_uuid, "user2", category_id="tmp_cat")
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user1")
        self.assertIsInstance(object_categories, list)
        self.assertNotIn("tmp_cat", object_categories)
        self.pap.del_object_category(self.ext_uuid, "user2", category_id="object_security_level")
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user1")
        self.assertIsInstance(object_categories, list)
        self.assertIn("object_security_level", object_categories)

    def test_subject_category_values(self):
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user1")
        for category_id in subject_categories:
            values = self.pap.get_subject_category_values(self.ext_uuid, "user1", category_id)
            self.assertIsInstance(values, list)
            if category_id == "subject_security_level":
                for _values in [u'high', u'medium', u'low']:
                    self.assertIn(_values, values)
        self.pap.add_subject_category_value(self.ext_uuid, "user1", "subject_security_level", "ultra_low")
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user1")
        for category_id in subject_categories:
            values = self.pap.get_subject_category_values(self.ext_uuid, "user1", category_id)
            self.assertIsInstance(values, list)
            if category_id == "subject_security_level":
                for _values in [u'high', u'medium', u'low', u"ultra_low"]:
                    self.assertIn(_values, values)
        self.pap.del_subject_category_value(self.ext_uuid, "user1", "subject_security_level", "ultra_low")
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user1")
        for category_id in subject_categories:
            values = self.pap.get_subject_category_values(self.ext_uuid, "user1", category_id)
            self.assertIsInstance(values, list)
            if category_id == "subject_security_level":
                for _values in [u'high', u'medium', u'low']:
                    self.assertIn(_values, values)
                self.assertNotIn(u"ultra_low", values)

    def test_subject_category_values_user_error(self):
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user3")
        self.assertEqual(subject_categories, None)
        self.pap.add_subject_category_value(self.ext_uuid, "user2", "subject_security_level", "ultra_low")
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user1")
        for category_id in subject_categories:
            values = self.pap.get_subject_category_values(self.ext_uuid, "user1", category_id)
            self.assertIsInstance(values, list)
            if category_id == "subject_security_level":
                for _values in [u'high', u'medium', u'low']:
                    self.assertIn(_values, values)
                self.assertNotIn(u"ultra_low", values)
        self.pap.del_subject_category_value(self.ext_uuid, "user2", "subject_security_level", "low")
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user1")
        for category_id in subject_categories:
            values = self.pap.get_subject_category_values(self.ext_uuid, "user1", category_id)
            self.assertIsInstance(values, list)
            if category_id == "subject_security_level":
                for _values in [u'high', u'medium', u'low']:
                    self.assertIn(_values, values)

    def test_object_category_values(self):
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user1")
        for category_id in object_categories:
            values = self.pap.get_object_category_values(self.ext_uuid, "user1", category_id)
            self.assertIsInstance(values, list)
            if category_id == "object_security_level":
                for _values in [u'high', u'medium', u'low']:
                    self.assertIn(_values, values)
            if category_id == "action":
                for _values in [u'read', u'write', u'execute']:
                    self.assertIn(_values, values)
        self.pap.add_object_category_value(self.ext_uuid, "user1", "object_security_level", "ultra_low")
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user1")
        for category_id in object_categories:
            values = self.pap.get_object_category_values(self.ext_uuid, "user1", category_id)
            self.assertIsInstance(values, list)
            if category_id == "object_security_level":
                for _values in [u'high', u'medium', u'low', u"ultra_low"]:
                    self.assertIn(_values, values)
        self.pap.del_object_category_value(self.ext_uuid, "user1", "object_security_level", "ultra_low")
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user1")
        for category_id in object_categories:
            values = self.pap.get_object_category_values(self.ext_uuid, "user1", category_id)
            self.assertIsInstance(values, list)
            if category_id == "object_security_level":
                for _values in [u'high', u'medium', u'low']:
                    self.assertIn(_values, values)
                self.assertNotIn(u"ultra_low", values)

    def test_object_category_values_user_error(self):
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user3")
        self.assertEqual(object_categories, None)
        self.pap.add_object_category_value(self.ext_uuid, "user2", "object_security_level", "ultra_low")
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user1")
        for category_id in object_categories:
            values = self.pap.get_object_category_values(self.ext_uuid, "user1", category_id)
            self.assertIsInstance(values, list)
            if category_id == "object_security_level":
                for _values in [u'high', u'medium', u'low']:
                    self.assertIn(_values, values)
                self.assertNotIn(u"ultra_low", values)
        self.pap.del_object_category_value(self.ext_uuid, "user2", "object_security_level", "low")
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user1")
        for category_id in object_categories:
            values = self.pap.get_object_category_values(self.ext_uuid, "user1", category_id)
            self.assertIsInstance(values, list)
            if category_id == "object_security_level":
                for _values in [u'high', u'medium', u'low']:
                    self.assertIn(_values, values)

    def test_subject_assignments(self):
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user1")
        for category_id in subject_categories:
            assign = self.pap.get_subject_assignments(self.ext_uuid, "user1", category_id)
            self.assertIsInstance(assign, dict)
            if category_id == "subject_security_level":
                for user in ["user1", "user2"]:
                    self.assertIn(user, assign.keys())
                    self.assertIsInstance(assign[user], list)
        self.pap.add_subject_assignment(
            self.ext_uuid, "user1", "subject_security_level", "user2", "high"
        )
        assign = self.pap.get_subject_assignments(self.ext_uuid, "user1", "subject_security_level")
        self.assertIsInstance(assign, dict)
        self.assertIsInstance(assign["user2"], list)
        self.assertIn("high", assign["user2"])
        self.pap.del_subject_assignment(
            self.ext_uuid, "user1", "subject_security_level", "user2", "high"
        )
        assign = self.pap.get_subject_assignments(self.ext_uuid, "user1", "subject_security_level")
        self.assertIsInstance(assign, dict)
        self.assertIsInstance(assign["user2"], list)
        self.assertNotIn("high", assign["user2"])

    def test_subject_assignments_user_error(self):
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user3")
        self.assertIsNone(subject_categories)
        subject_categories = self.pap.get_subject_categories(self.ext_uuid, "user1")
        for category_id in subject_categories:
            assign = self.pap.get_subject_assignments(self.ext_uuid, "user3", category_id)
            self.assertIsNone(assign)
        self.pap.add_subject_assignment(
            self.ext_uuid, "user2", "subject_security_level", "user2", "high"
        )
        assign = self.pap.get_subject_assignments(self.ext_uuid, "user1", "subject_security_level")
        self.assertIsInstance(assign, dict)
        self.assertIsInstance(assign["user2"], list)
        self.assertNotIn("high", assign["user2"])
        self.pap.del_subject_assignment(
            self.ext_uuid, "user2", "subject_security_level", "user1", "high"
        )
        assign = self.pap.get_subject_assignments(self.ext_uuid, "user1", "subject_security_level")
        self.assertIsInstance(assign, dict)
        self.assertIsInstance(assign["user1"], list)
        self.assertIn("high", assign["user1"])

    def test_object_assignments(self):
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user1")
        for category_id in object_categories:
            assign = self.pap.get_object_assignments(self.ext_uuid, "user1", category_id)
            self.assertIsInstance(assign, dict)
            if category_id == "object_security_level":
                for obj in ["vm1", "vm2", "vm3"]:
                    self.assertIn(obj, assign.keys())
                    self.assertIsInstance(assign[obj], list)
            if category_id == "action":
                for obj in ["vm1", "vm2", "vm3"]:
                    self.assertIn(obj, assign.keys())
                    self.assertIsInstance(assign[obj], list)
                    #Assignments for action must be empty
                    self.assertEqual(assign[obj], list())
        self.pap.add_object_assignment(
            self.ext_uuid, "user1", "object_security_level", "vm2", "high"
        )
        assign = self.pap.get_object_assignments(self.ext_uuid, "user1", "object_security_level")
        self.assertIsInstance(assign, dict)
        self.assertIsInstance(assign["vm2"], list)
        self.assertIn("high", assign["vm2"])
        self.pap.del_object_assignment(
            self.ext_uuid, "user1", "object_security_level", "vm2", "high"
        )
        assign = self.pap.get_object_assignments(self.ext_uuid, "user1", "object_security_level")
        self.assertIsInstance(assign, dict)
        self.assertIsInstance(assign["vm2"], list)
        self.assertNotIn("high", assign["vm2"])

    def test_object_assignments_user_error(self):
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user3")
        self.assertIsNone(object_categories)
        object_categories = self.pap.get_object_categories(self.ext_uuid, "user1")
        for category_id in object_categories:
            assign = self.pap.get_object_assignments(self.ext_uuid, "user3", category_id)
            self.assertIsNone(assign)
        assign = self.pap.get_object_assignments(self.ext_uuid, "user1", "object_security_level")
        self.assertIsInstance(assign, dict)
        self.assertIsInstance(assign["vm2"], list)
        self.assertNotIn("high", assign["vm2"])
        self.pap.add_object_assignment(
            self.ext_uuid, "user2", "object_security_level", "vm2", "high"
        )
        assign = self.pap.get_object_assignments(self.ext_uuid, "user1", "object_security_level")
        self.assertIsInstance(assign, dict)
        self.assertIsInstance(assign["vm2"], list)
        self.assertNotIn("high", assign["vm2"])
        self.pap.del_object_assignment(
            self.ext_uuid, "user2", "object_security_level", "vm1", "high"
        )
        assign = self.pap.get_object_assignments(self.ext_uuid, "user1", "object_security_level")
        self.assertIsInstance(assign, dict)
        self.assertIsInstance(assign["vm1"], list)
        self.assertIn("high", assign["vm1"])

    def test_rules(self):
        rules = self.pap.get_rules(self.ext_uuid, "user1")
        self.assertIsInstance(rules, dict)
        for rule in rules:
            self.assertIsInstance(rule, unicode)
            self.assertEqual(len(rules[rule]), 3)
        sub_cat_value = {"relation_super": {"subject_security_level": "medium"}}
        obj_cat_value = {"relation_super": {"object_security_level": "medium", "action": "read"}}
        self.pap.add_rule(self.ext_uuid, "user1", sub_cat_value, obj_cat_value)
        rules = self.pap.get_rules(self.ext_uuid, "user1")
        self.assertIsInstance(rules, dict)
        for rule in rules:
            self.assertIsInstance(rule, unicode)
            for _rule in rules[rule]:
                self.assertEqual(len(_rule), 3)
        self.assertIn([u'medium', u'medium', u'read'], rules['relation_super'])

    def test_rules_user_error(self):
        rules = self.pap.get_rules(self.ext_uuid, "user3")
        self.assertIsNone(rules)
        rules = self.pap.get_rules(self.ext_uuid, "user1")
        for rule in rules:
            self.assertIsInstance(rule, unicode)
            for _rule in rules[rule]:
                self.assertEqual(len(_rule), 3)
        sub_cat_value = {"subject_security_level": "low"}
        obj_cat_value = {"object_security_level": "medium", "action": "read"}
        self.pap.add_rule(self.ext_uuid, "user2", sub_cat_value, obj_cat_value)
        rules = self.pap.get_rules(self.ext_uuid, "user1")
        self.assertIsInstance(rules, dict)
        for rule in rules:
            self.assertIsInstance(rule, unicode)
            for _rule in rules[rule]:
                self.assertEqual(len(_rule), 3)
        self.assertNotIn([u'low', u'medium', u'read'], rules['relation_super'])


class TestSuperExtension(unittest.TestCase):

    def setUp(self):
        self.pap = get_pap()

    def tearDown(self):
        pass

    def test_mapping(self):
        mappings = self.pap.list_mappings("admin")
        self.assertIsInstance(mappings, list)
        for mapping in mappings:
            self.assertIsInstance(mapping, dict)
            for key in ('intra_extension_uuids', 'tenant_uuid'):
                self.assertIn(key, mapping)

    def test_create_mapping(self):
        for i in range(len(mls001_results["create_mapping"])):
            _tenant_uuid = mls001_results["create_mapping"][i]['tenant_uuid']
            _intra_extension_uuid = mls001_results["create_mapping"][i]['intra_extension_uuid']
            _result = mls001_results["create_mapping"][i]['_result']
            self.assertEqual(self.pap.create_mapping("admin", _tenant_uuid, _intra_extension_uuid), _result)
        for i in range(len(mls001_results["destroy_mapping"])):
            _tenant_uuid = mls001_results["destroy_mapping"][i]['tenant_uuid']
            _intra_extension_uuid = mls001_results["destroy_mapping"][i]['intra_extension_uuid']
            _result = mls001_results["destroy_mapping"][i]['_result']
            self.assertEqual(self.pap.destroy_mapping("admin", _tenant_uuid, _intra_extension_uuid), _result)

    # def test_delegate_mapping(self):
    #     for i in range(len(super_extension_results["delegate_mapping_privilege"])):
    #         _delegator_id = super_extension_results["delegate_mapping_privilege"][i]['delegator_id']
    #         _privilege = super_extension_results["delegate_mapping_privilege"][i]['privilege']
    #         _result = super_extension_results["delegate_mapping_privilege"][i]['_result']
    #         self.assertEqual(self.pap.delegate_privilege("admin", _delegator_id, "mapping", _privilege), _result)

    # def test_delegate_collaboration(self):
    #     for i in range(len(super_extension_results["delegate_collaboration_privilege"])):
    #         _delegator_id = super_extension_results["delegate_collaboration_privilege"][i]['delegator_id']
    #         _privilege = super_extension_results["delegate_collaboration_privilege"][i]['privilege']
    #         _result = super_extension_results["delegate_collaboration_privilege"][i]['_result']
    #         self.assertEqual(self.pap.delegate_privilege("admin", _delegator_id, "collaboration", _privilege), _result)

# class TestCorePAPInterExtensions(unittest.TestCase):
#
#     def setUp(self):
#         extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001')
#         self.pap = get_pap()
#         self.requesting_intra_extension_uuid = self.pap.add_from_json(extension_setting_abs_dir)
#         self.requested_intra_extension_uuid = self.pap.add_from_json(extension_setting_abs_dir)
#
#         # self.inter_extension = InterExtension(self.requesting_intra_extension, self.requested_intra_extension)
#
#     def tearDown(self):
#         pass
#
#     def test_create_destroy_collaboration(self):
#         _sub_list = ['user1', 'user2']
#         _obj_list = ['vm2', 'vm3']
#         _act = "read"
#
#         _inter_extension_uuid, _vent_uuid = self.pap.create_collaboration(
#             user_uuid="user1",
#             requesting_intra_extension_uuid=self.requesting_intra_extension_uuid,
#             requested_intra_extension_uuid=self.requested_intra_extension_uuid,
#             genre="trust",
#             sub_list=_sub_list,
#             obj_list=_obj_list,
#             act=_act
#         )
#         print("xxxxxxxxxxxxxxxxxxxx", _inter_extension_uuid, _vent_uuid)
#
#         self.assertIsInstance(_inter_extension_uuid, str)
#         self.assertIsInstance(_vent_uuid, str)
#         inter_extension = self.pap.get_installed_inter_extensions('user1', _inter_extension_uuid).next()
#         self.assertEqual(inter_extension.get_uuid(), _inter_extension_uuid)
#
#         vent_data_dict = inter_extension.get_vent_data_dict(_vent_uuid)
#         self.assertIsInstance(vent_data_dict, dict)
#         for key in (
#                 'uuid',
#                 'type',
#                 'requested_subject_category_value_dict',
#                 'requested_object_list',
#                 'requesting_rule_alist',
#                 'requesting_object_category_value_dict',
#                 'requesting_subject_category_value_dict',
#                 'requesting_subject_list',
#                 'requested_object_category_value_dict'):
#             self.assertIn(key, vent_data_dict.keys())
#
#         self.assertEqual(inter_extension.authz('user1', 'vm2', 'read'), "OK")
#         self.assertEqual(inter_extension.authz('user3', 'vm2', 'read'), "KO")
#
#         vents = inter_extension.get_vents()
#         self.assertIsInstance(vents, dict)
#         from moon.core.pdp.inter_extension import VirtualEntity
#         for vent in vents.values():
#             self.assertIsInstance(vent, VirtualEntity)
#         self.assertIn(_vent_uuid, vents)
#
#         self.pap.destroy_collaboration('user1', _inter_extension_uuid, _vent_uuid)
#
#         vents = inter_extension.get_vents()
#         self.assertIsInstance(vents, dict)
#         for vent in vents.values():
#             self.assertIsInstance(vent, VirtualEntity)
#         self.assertNotIn(_vent_uuid, vents)

if __name__ == "__main__":
    unittest.main()
