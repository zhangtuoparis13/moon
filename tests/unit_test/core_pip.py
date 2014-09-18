"""
unit test for moon/core/pap
"""

import unittest
from moon.core.pip import get_pip
import types


class TestCorePIP(unittest.TestCase):

    def setUp(self):
        self.pip = get_pip()

    def tearDown(self):
        self.pip = None

    def test_subjects(self):
        subjects = self.pip.get_subjects()
        self.assertIsInstance(subjects, types.GeneratorType)
        user_names = []
        for sub in subjects:
            self.assertIsInstance(sub, dict)
            for key in ['uuid', 'domain', 'enabled', 'name']:
                self.assertIn(key, sub.keys())
            user_names.append(sub["name"])
        self.assertIn("admin", user_names)
        new_user = dict()
        new_user['domain'] = "Default"
        new_user['enabled'] = True
        new_user['name'] = "TestCorePIP"
        new_user['project'] = "admin"
        new_user['password'] = "password"
        new_user['description'] = "Unit test user"
        uuid_test_user = self.pip.add_subject(new_user)
        subjects = self.pip.get_subjects()
        self.assertIsInstance(subjects, types.GeneratorType)
        user_names = []
        for sub in subjects:
            self.assertIsInstance(sub, dict)
            for key in ['uuid', 'domain', 'enabled', 'name']:
                self.assertIn(key, sub.keys())
            if sub["name"] == "TestCorePIP":
                self.assertEqual(uuid_test_user, sub["uuid"])
            user_names.append(sub["name"])
        self.assertIn("TestCorePIP", user_names)
        self.pip.del_subject(uuid_test_user)
        subjects = self.pip.get_subjects()
        self.assertIsInstance(subjects, types.GeneratorType)
        user_names = []
        for sub in subjects:
            self.assertIsInstance(sub, dict)
            for key in ['uuid', 'domain', 'enabled', 'name']:
                self.assertIn(key, sub.keys())
            user_names.append(sub["name"])
        self.assertNotIn("TestCorePIP", user_names)

    def test_subjects_error(self):
        new_user = dict()
        new_user['domain'] = "Default"
        new_user['enabled'] = True
        new_user['project'] = "admin"
        new_user['password'] = "password"
        new_user['description'] = "Unit test user"
        uuid_test_user = self.pip.add_subject(new_user)
        self.assertIsNone(uuid_test_user)

    def test_objects(self):
        objects = self.pip.get_objects("admin")
        self.assertIsInstance(objects, types.GeneratorType)
        for obj in objects:
            for key in ("name", "uuid", "description", "tenant", "enabled"):
                self.assertIn(key, obj.keys())
            self.assertEqual("admin", obj["tenant"])

    def test_tenants(self):
        tenants = self.pip.get_tenants()
        self.assertIsInstance(tenants, types.GeneratorType)
        for tenant in tenants:
            for key in ("name", "uuid", "description", "domain", "enabled"):
                self.assertIn(key, tenant.keys())
        tenants = self.pip.get_tenants(name="admin")
        self.assertIsInstance(tenants, types.GeneratorType)
        tenant_names = []
        for tenant in tenants:
            for key in ("name", "uuid", "description", "domain", "enabled"):
                self.assertIn(key, tenant.keys())
            tenant_names.append(tenant["name"])
        self.assertIn("admin", tenant_names)
        tenant = dict()
        tenant["name"] = "TestPIP"
        tenant["description"] = " this a test tenant"
        tenant["domain"] = "Default"
        tenant["enabled"] = True
        tenant_uuid = self.pip.add_tenant(tenant)
        tenants = self.pip.get_tenants()
        tenant_names = []
        self.assertIsInstance(tenants, types.GeneratorType)
        for tenant in tenants:
            for key in ("name", "uuid", "description", "domain", "enabled"):
                self.assertIn(key, tenant.keys())
            if tenant["name"] == "TestPIP":
                self.assertEqual(tenant_uuid, tenant["uuid"])
            tenant_names.append(tenant["name"])
        self.assertIn("TestPIP", tenant_names)
        self.pip.del_tenant(tenant_uuid)
        tenants = self.pip.get_tenants()
        tenant_names = []
        self.assertIsInstance(tenants, types.GeneratorType)
        for tenant in tenants:
            for key in ("name", "uuid", "description", "domain", "enabled"):
                self.assertIn(key, tenant.keys())
            tenant_names.append(tenant["name"])
        self.assertNotIn("TestPIP", tenant_names)

if __name__ == "__main__":
    unittest.main()
