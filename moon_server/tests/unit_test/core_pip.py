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
unit test for moon/core/pap
"""

import unittest
from moon_server.core.pip import get_pip
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
        from uuid import uuid4
        vm_name = "PIPTest-" + str(uuid4())
        image = "Cirros3.2"
        images = map(lambda x: x["name"], get_pip().get_images())
        for _img in images:
            if "irros" in _img:
                image = _img
        self.pip.add_object(name=vm_name, image_name=image)
        max_cpt = 0
        vm_names = list()
        vm_uuid = None
        while max_cpt < 12:
            objects = self.pip.get_objects("admin")
            self.assertIsInstance(objects, types.GeneratorType)
            vm_names = list()
            for obj in objects:
                for key in ("name", "uuid", "description", "tenant", "enabled"):
                    self.assertIn(key, obj.keys())
                self.assertEqual("admin", obj["tenant"])
                vm_names.append(obj["name"])
                if vm_name == obj["name"]:
                    vm_uuid = obj["uuid"]
            if vm_name in vm_names:
                break
            max_cpt += 1
        else:
            self.assertIn(vm_name, vm_names)
        self.assertIsNotNone(vm_uuid)
        self.pip.del_object(uuid=vm_uuid)
        objects = self.pip.get_objects("admin")
        self.assertIsInstance(objects, types.GeneratorType)
        max_cpt = 0
        vm_names = list()
        while max_cpt < 12:
            objects = self.pip.get_objects("admin")
            self.assertIsInstance(objects, types.GeneratorType)
            vm_names = list()
            for obj in objects:
                for key in ("name", "uuid", "description", "tenant", "enabled"):
                    self.assertIn(key, obj.keys())
                self.assertEqual("admin", obj["tenant"])
                vm_names.append(obj["name"])
            if vm_name not in vm_names:
                break
            max_cpt += 1
        self.assertNotIn(vm_name, vm_names)

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

    def test_roles(self):
        roles = self.pip.get_roles()
        self.assertIsInstance(roles, types.GeneratorType)
        for role in roles:
            for key in ("value", "uuid", "description", "enabled"):
                self.assertIn(key, role.keys())
        roles = self.pip.get_roles(tenant_name="admin")
        self.assertIsInstance(roles, types.GeneratorType)
        role_uuid = self.pip.add_role(name="TestCorePIP")
        roles = self.pip.get_roles()
        self.assertIsInstance(roles, types.GeneratorType)
        role_names = list()
        for role in roles:
            for key in ("value", "uuid", "description", "enabled"):
                self.assertIn(key, role.keys())
            role_names.append(role["value"])
        self.assertIn("TestCorePIP", role_names)
        self.pip.del_role(uuid=role_uuid)
        roles = self.pip.get_roles()
        self.assertIsInstance(roles, types.GeneratorType)
        role_names = list()
        for role in roles:
            for key in ("value", "uuid", "description", "enabled"):
                self.assertIn(key, role.keys())
            role_names.append(role["value"])
        self.assertNotIn("TestCorePIP", role_names)

    def test_groups(self):
        groups = self.pip.get_groups()
        self.assertIsInstance(groups, types.GeneratorType)
        for group in groups:
            for key in ("value", "uuid", "description", "enabled"):
                self.assertIn(key, group.keys())
        groups = self.pip.get_groups(tenant_name="admin")
        self.assertIsInstance(groups, types.GeneratorType)
        group_uuid = self.pip.add_group(name="TestCorePIP")
        groups = self.pip.get_groups()
        self.assertIsInstance(groups, types.GeneratorType)
        group_names = list()
        for group in groups:
            for key in ("value", "uuid", "description", "enabled"):
                self.assertIn(key, group.keys())
            group_names.append(group["value"])
        self.assertIn("TestCorePIP", group_names)
        self.pip.del_group(uuid=group_uuid)
        groups = self.pip.get_groups()
        self.assertIsInstance(groups, types.GeneratorType)
        group_names = list()
        for group in groups:
            for key in ("value", "uuid", "description", "enabled"):
                self.assertIn(key, group.keys())
            group_names.append(group["value"])
        self.assertNotIn("TestCorePIP", group_names)

    def test_roles_assignment(self):
        #Get the admin user
        admin = filter(lambda x: x["name"] == "admin", self.pip.get_subjects(tenant="admin"))[0]
        admin_uuid = admin["uuid"]
        #Add a new role for the test
        role_uuid = self.pip.add_role(name="TestCorePIP")
        roles = self.pip.get_roles()
        self.assertIsInstance(roles, types.GeneratorType)
        roles = list(roles)
        role_names = list()
        for role in roles:
            for key in ("value", "uuid", "description", "enabled"):
                self.assertIn(key, role.keys())
            role_names.append(role["value"])
        self.assertIn("TestCorePIP", role_names)
        role = filter(lambda x: x["value"], roles)[0]
        #Do the tests on assignments
        assignments = self.pip.get_users_roles_assignment()
        user_uuids = list()
        for assign in assignments:
            for key in ("subject", "uuid", "description", "attributes"):
                self.assertIn(key, assign.keys())
            user_uuids.append(assign["subject"])
            if assign["subject"] == admin_uuid:
                self.assertGreater(len(assign["attributes"]), 0)
        self.assertIn(admin_uuid, user_uuids)
        #Add a new assignment
        self.pip.add_users_roles_assignment(tenant_name="admin", user_uuid=admin_uuid, role_uuid=role["uuid"])
        assignments = self.pip.get_users_roles_assignment()
        user_uuids = dict()
        for assign in assignments:
            for key in ("subject", "uuid", "description", "attributes"):
                self.assertIn(key, assign.keys())
            user_uuids[assign["subject"]] = assign["attributes"]
            if assign["subject"] == admin_uuid:
                self.assertGreater(len(assign["attributes"]), 0)
        self.assertIn(admin_uuid, user_uuids.keys())
        self.assertIn(role["uuid"], user_uuids[admin_uuid])
        # self.pip.set_creds_for_tenant()
        #Delete the added assignment
        # self.pip.del_users_roles_assignment(tenant_name="admin", user_uuid=admin_uuid, role_uuid=role["uuid"])
        # assignments = self.pip.get_users_roles_assignment()
        # user_uuids = dict()
        # for assign in assignments:
        #     for key in ("subject", "uuid", "description", "attributes"):
        #         self.assertIn(key, assign.keys())
        #     user_uuids[assign["subject"]] = assign["attributes"]
        #     if assign["subject"] == admin_uuid:
        #         self.assertGreater(len(assign["attributes"]), 0)
        # self.assertIn(admin_uuid, user_uuids.keys())
        # self.assertNotIn(role_uuid, user_uuids[admin_uuid])
        # #Delete the added role
        # self.pip.del_role(uuid=role_uuid)
        # roles = self.pip.get_roles()
        # self.assertIsInstance(roles, types.GeneratorType)
        # role_names = list()
        # for role in roles:
        #     for key in ("value", "uuid", "description", "enabled"):
        #         self.assertIn(key, role.keys())
        #     role_names.append(role["value"])
        # self.assertNotIn("TestCorePIP", role_names)

    def test_groups_assignment(self):
        admin = filter(lambda x: x["name"] == "admin", self.pip.get_subjects(tenant="admin"))[0]
        admin_uuid = admin["uuid"]
        assignments = self.pip.get_users_groups_assignment()
        user_uuids = list()
        for assign in assignments:
            for key in ("subject", "uuid", "description", "attributes"):
                self.assertIn(key, assign.keys())
            user_uuids.append(assign["subject"])
        self.assertIn(admin_uuid, user_uuids)

if __name__ == "__main__":
    unittest.main()
