"""
unit test for moon/core/pap
"""

import unittest
import pkg_resources
from moon.core.pdp.core import IntraExtension
from moon.core.pap import get_pap


class TestCorePDPExtension(unittest.TestCase):

    def setUp(self):
        self.extension = IntraExtension()
        extension_setting_abs_dir = pkg_resources.resource_filename("moon", 'samples/mls001')
        self.extension.load_from_json(extension_setting_abs_dir)
        self.pap = get_pap()

    def tearDown(self):
        pass

    def test_subjects(self):
        subjects = self.pap.get_subjects(self.extension.get_uuid(), "user1")
        self.assertIsInstance(subjects, list)
        self.assertIn("user1", subjects)
        #Test adding a new subject
        self.pap.add_subject(self.extension.get_uuid(), "user1", subject_id="user3")
        subjects = self.pap.get_subjects(self.extension.get_uuid(), "user1")
        self.assertIsInstance(subjects, list)
        self.assertIn("user3", subjects)
        self.pap.del_subject(self.extension.get_uuid(), "user1", subject_id="user3")
        subjects = self.pap.get_subjects(self.extension.get_uuid(), "user1")
        self.assertIsInstance(subjects, list)
        self.assertNotIn("user3", subjects)

    def test_subjects_user_error(self):
        subjects = self.pap.get_subjects(self.extension.get_uuid(), "userX")
        self.assertEqual(subjects, None)
        #Test adding a new subject with a wrong user
        self.pap.add_subject(self.extension.get_uuid(), "user2", subject_id="user3")
        subjects = self.pap.get_subjects(self.extension.get_uuid(), "user1")
        self.assertIsInstance(subjects, list)
        self.assertNotIn("user3", subjects)
        self.pap.del_subject(self.extension.get_uuid(), "user2", subject_id="user1")
        subjects = self.pap.get_subjects(self.extension.get_uuid(), "user1")
        self.assertIsInstance(subjects, list)
        self.assertIn("user1", subjects)

    def test_objects(self):
        objects = self.pap.get_objects(self.extension.get_uuid(), "user1")
        self.assertIsInstance(objects, list)
        self.assertIn("vm1", objects)
        #Test adding a new object
        self.pap.add_object(self.extension.get_uuid(), "user1", object_id="vm4")
        objects = self.pap.get_objects(self.extension.get_uuid(), "user1")
        self.assertIsInstance(objects, list)
        self.assertIn("vm4", objects)
        self.pap.del_object(self.extension.get_uuid(), "user1", object_id="vm4")
        objects = self.pap.get_oubjects(self.extension.get_uuid(), "user1")
        self.assertIsInstance(objects, list)
        self.assertNotIn("vm4", objects)

    def test_objects_user_error(self):
        objects = self.pap.get_objects(self.extension.get_uuid(), "user3")
        self.assertEqual(objects, None)
        self.pap.add_object(self.extension.get_uuid(), "user2", object_id="vm4")
        objects = self.pap.get_objects(self.extension.get_uuid(), "user1")
        self.assertIsInstance(objects, list)
        self.assertNotIn("vm4", objects)
        self.pap.del_object(self.extension.get_uuid(), "user2", object_id="vm1")
        objects = self.pap.get_objects(self.extension.get_uuid(), "user1")
        self.assertIsInstance(objects, list)
        self.assertIn("vm1", objects)

    def test_subject_categories(self):
        subject_categories = self.pap.get_subject_categories(self.extension.get_uuid(), "user1")
        self.assertIsInstance(subject_categories, list)
        self.assertIn("subject_security_level", subject_categories)
        self.pap.add_subject_category(self.extension.get_uuid(), "user1", category_id="tmp_cat")
        subject_categories = self.pap.get_subject_categories(self.extension.get_uuid(), "user1")
        self.assertIsInstance(subject_categories, list)
        self.assertIn("tmp_cat", subject_categories)
        self.pap.del_subject_category(self.extension.get_uuid(), "user1", category_id="tmp_cat")
        subject_categories = self.pap.get_subject_categories(self.extension.get_uuid(), "user1")
        self.assertIsInstance(subject_categories, list)
        self.assertNotIn("tmp_cat", subject_categories)

    def test_subject_categories_user_error(self):
        subject_categories = self.pap.get_subject_categories(self.extension.get_uuid(), "user3")
        self.assertEqual(subject_categories, None)
        self.pap.add_subject_category(self.extension.get_uuid(), "user2", category_id="tmp_cat")
        subject_categories = self.pap.get_subject_categories(self.extension.get_uuid(), "user1")
        self.assertIsInstance(subject_categories, list)
        self.assertNotIn("tmp_cat", subject_categories)
        self.pap.del_subject_category(self.extension.get_uuid(), "user2", category_id="subject_security_level")
        subject_categories = self.pap.get_subject_categories(self.extension.get_uuid(), "user1")
        self.assertIsInstance(subject_categories, list)
        self.assertIn("subject_security_level", subject_categories)

    def test_object_categories(self):
        object_categories = self.pap.get_object_categories(self.extension.get_uuid(), "user1")
        self.assertIsInstance(object_categories, list)
        self.assertIn("object_security_level", object_categories)
        self.assertIn("action", object_categories)
        self.pap.add_object_category(self.extension.get_uuid(), "user1", category_id="tmp_cat")
        object_categories = self.pap.get_object_categories(self.extension.get_uuid(), "user1")
        self.assertIsInstance(object_categories, list)
        self.assertIn("tmp_cat", object_categories)
        self.pap.del_object_category(self.extension.get_uuid(), "user1", category_id="tmp_cat")
        object_categories = self.pap.get_object_categories(self.extension.get_uuid(), "user1")
        self.assertIsInstance(object_categories, list)
        self.assertNotIn("tmp_cat", object_categories)

    def test_object_categories_user_error(self):
        object_categories = self.pap.get_object_categories(self.extension.get_uuid(), "user3")
        self.assertEqual(object_categories, None)
        self.pap.add_object_category(self.extension.get_uuid(), "user2", category_id="tmp_cat")
        object_categories = self.pap.get_object_categories(self.extension.get_uuid(), "user1")
        self.assertIsInstance(object_categories, list)
        self.assertNotIn("tmp_cat", object_categories)
        self.pap.del_object_category(self.extension.get_uuid(), "user2", category_id="object_security_level")
        object_categories = self.pap.get_object_categories(self.extension.get_uuid(), "user1")
        self.assertIsInstance(object_categories, list)
        self.assertIn("object_security_level", object_categories)

    def test_meta_rules(self):
        meta_rules = self.pap.get_meta_rules(self.extension.get_uuid(), "user1")
        self.assertIn(meta_rules, dict)
        self.assertIn("sub_meta_rules", meta_rules.keys())
        self.assertIn("subject_categories", meta_rules["sub_meta_rules"].keys())
        self.assertIn("object_categories", meta_rules["sub_meta_rules"].keys())
        self.assertIn("relation", meta_rules["sub_meta_rules"].keys())
        rule = {
            "subject_categories": ["subject_security_level"],
            "object_categories": ["object_security_level", "action"],
            "relation": "relation_super"
        }
        self.pap.add_meta_rules(self.extension.get_uuid(), "user1", rule)

    def test_meta_rules_user_error(self):
        meta_rules = self.pap.get_meta_rules(self.extension.get_uuid(), "user3")
        self.assertEqual(meta_rules, None)

    # def test_add_meta_rules(self):
    #     self.pap.add_meta_rules(self.extension.get_uuid(), "user1", rule)
    #
    # def test_del_meta_rules(self):
    #     self.pap.del_meta_rules(self.extension.get_uuid(), "user1", rule_id)
    #
    # def test_get_subject_category_values(self):
    #     self.pap.get_subject_category_values(self.extension.get_uuid(), "user1", category_id)
    #
    # def test_add_subject_category_values(self):
    #     self.pap.add_subject_category_values(self.extension.get_uuid(), "user1", category_id, category_value)
    #
    # def test_del_subject_category_values(self):
    #     self.pap.del_subject_category_values(self.extension.get_uuid(), "user1", category_id, category_value)
    #
    # def test_get_object_category_values(self):
    #     self.pap.get_object_category_values(self.extension.get_uuid(), "user1", category_id)
    #
    # def test_add_object_category_values(self):
    #     self.pap.add_object_category_values(self.extension.get_uuid(), "user1", category_id, category_value)
    #
    # def test_del_object_category_values(self):
    #     self.pap.del_object_category_values(self.extension.get_uuid(), "user1", category_id, category_value)
    #
    # def test_get_subject_assignments(self):
    #     self.pap.get_subject_assignments(self.extension.get_uuid(), "user1", category_id)
    #
    # def test_add_subject_assignment(self):
    #     self.pap.add_subject_assignment(
    #                 self.extension.get_uuid(), "user1", category_id, subject_id, category_value
    #             )
    #
    # def test_del_subject_assignment(self):
    #     self.pap.del_subject_assignment(
    #                 self.extension.get_uuid(), "user1", category_id, subject_id, category_value
    #             )
    #
    # def test_get_object_assignments(self):
    #     self.pap.get_object_assignments(self.extension.get_uuid(), "user1", category_id)
    #
    # def test_add_object_assignment(self):
    #     self.pap.add_object_assignment(
    #                 self.extension.get_uuid(), "user1", category_id, object_id, category_value
    #             )
    #
    # def test_del_object_assignment(self):
    #     self.pap.del_object_assignment(
    #                 self.extension.get_uuid(), "user1", category_id, object_id, category_value
    #             )
    #
    # def test_get_rules(self):
    #     self.pap.get_rules(self.extension.get_uuid(), "user1")
    #
    # def test_add_rule(self):
    #     self.pap.add_rules(self.extension.get_uuid(), "user1", name, subject_attrs, object_attrs, description)
    #
    # def test_del_rule(self, rule_id):
    #     self.pap.add_rules(self.extension.get_uuid(), "user1", rule_id)


if __name__ == "__main__":
    unittest.main()
