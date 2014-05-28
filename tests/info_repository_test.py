import unittest
from moon.info_repository import driver_dispatcher as dd
from moon.info_repository import models
from moon import settings

test_user = {
    "name": "testman",
    "mail": "testman@orange.com",
    "project": "admin",
    "domain": "Default",
    "enabled": True,
    "description": "the user testman."
}

dd.create_tables(cls=getattr(settings, "INITIAL_DB"))


class TestMySQLFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_element(self):
        """test the addition of a new element in the database"""
        user = dd.create_element(table="Subject", values=test_user)
        self.assertIsInstance(user, models.__list__['Subject'])
        for key in test_user.keys():
            self.assertEqual(test_user[key], getattr(user, key))
        test_user["uuid"] = user.uuid
        self.assertIsInstance(user.uuid, str)
        self.assertEqual(len(user.uuid), 32)

    def test_get_elements(self):
        """test the listing of all elements in the database"""
        elements = dd.get_elements()
        for element in elements:
            self.assertIsInstance(element, models.__list__['Subject'])
            for key in test_user.keys():
                self.assertIn(key, dir(element))
                self.assertIsInstance(element.uuid, str)
                self.assertEqual(len(element.uuid), 32)

    def test_get_element(self):
        """test the listing of a specific element in the database"""
        users = dd.get_element(attributes={"uuid": test_user["uuid"]})
        for user in users:
            self.assertIsInstance(user, models.__list__['Subject'])
            for key in test_user.keys():
                self.assertEqual(test_user[key], getattr(user, key))

    def test_delete_element(self):
        """test the deletion of a new element in the database"""
        dd.delete_element(values={"uuid": test_user["uuid"]})
        user = dd.get_element(attributes={"uuid": test_user["uuid"]})
        self.assertEqual(len(user), 0)

if __name__ == '__main__':
    unittest.main()
