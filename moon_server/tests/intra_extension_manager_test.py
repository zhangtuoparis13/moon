import unittest
from moon_server import settings
import uuid
from moon_server.intra_extension_manager import get_dispatcher
from moon_server.intra_extension_manager.models import Extension
test_extension = {
    "uuid": "extension_uuid1",
    "description": "one extension",
    "perimeter": {
        "subjects": {
            "user1_uuid": {
                "name": "admin",
                "description": "administrator"
            },
            "user2_uuid": {
                "name": "demo1",
                "description": "demo 1"
            },
            "user3_uuid": {
                "name": "demo2",
                "description": "demo 2"
            }
        },
        "objects": {
            "vm1_uuid": {
                "name": "Vitual1",
                "description": "first virtual machine"
            },
            "vmt2_uuid": {
                "name": "Virtual2",
                "description": "second virtual machine"
            }
        }
    },

    "configuration": {
        "metadata": {
            "subject": [ "role", "group" ],
            "object": [ "type", "security" ]
        },
        "rules": [
            {
                "name": "rule1",
                "s_attr": { "category": "role", "value": "s_attr_uuid1" },
                "o_attr": { "category": "type", "value": "o_attr_uuid1" },
                "a_attr": { "category": "action", "value": "list" },
                "description": "first rule"
            },
            {
                "name": "rule2",
                "s_attr": { "category": "role", "value": "s_attr_uuid1" },
                "o_attr": { "category": "type", "value": "o_attr_uuid1" },
                "a_attr": { "category": "action", "value": "list" },
                "description": "second rule "
            }
        ]
    },

    "profiles": {
        "s_attr": {
            "s_attr_uuid1": {
                "category": "role",
                "value": "admin",
                "description": "le role admin"
            },
            "s_attr_uuid2": {
                "category": "role",
                "value": "dev"
            },
            "s_attr_uuid3": {
                "category": "group",
                "value": "prog"
            }
        },
        "o_attr": {
            "o_attr_uuid1": {
                "category": "type",
                "value": "stockage",
                "description": ""
            },
            "o_attr_uuid2": {
                "category": "size",
                "value": "medium"
            }
        },
        "s_attr_assign": {
            "assign1_uuid": {
                "subject": "user1_uuid",
                "attributes": [
                    "s_attr_uuid1",
                    "s_attr_uuid2"
                ]
            },
            "assign2_uuid": {
                "subject": "user3_uuid",
                "attributes": [
                    "s_attr_uuid1",
                    "s_attr_uuid2",
                ]
            }
        },
        "o_attr_assign": {
            "assign3_uuid": {
                "object": "object1_uuid",
                "attributes": [
                    "o_attr_uuid1",
                    "o_attr_uuid2"
                ]
            },
            "assign4_uuid": {
                "object": "object3_uuid",
                "attributes": [
                    "o_attr_uuid1",
                    "o_attr_uuid2",
                    "o_attr_uuid3"
                ]
            }
        }
    }

}


class TestMongoDBFunctions(unittest.TestCase):

    def setUp(self):
        self.ie = get_dispatcher()

    def tearDown(self):
        pass

    def test_add_and_delete_element(self):
        self.ext = self.ie.new(
            name="test extension",
            subjects=test_extension['perimeter']['subjects'].values(),
            objects=test_extension['perimeter']['objects'].values(),
            metadata=test_extension['configuration']['metadata'],
            rules=test_extension['configuration']['rules'],
            description=test_extension['description'],
            profiles=test_extension['profiles']
        )
        self.assertIsInstance(self.ext, Extension)
        answer = self.ie.delete(uuid=self.ext.uuid)
        self.assertIsInstance(answer, dict)
        self.assertEqual(answer["err"], None)

    def test_add_and_delete_element_with_uuid(self):
        self.ext = self.ie.new(
            name="test extension",
            uuid=str(uuid.uuid4()).replace("-", ""),
            subjects=test_extension['perimeter']['subjects'].values(),
            objects=test_extension['perimeter']['objects'].values(),
            metadata=test_extension['configuration']['metadata'],
            rules=test_extension['configuration']['rules'],
            description=test_extension['description'],
            profiles=test_extension['profiles']
        )
        self.assertIsInstance(self.ext, Extension)
        answer = self.ie.delete(uuid=self.ext.uuid)
        self.assertIsInstance(answer, dict)
        self.assertEqual(answer["err"], None)

    def test_list_elements(self):
        self.ie.delete_tables()
        obj = self.ie.list()
        self.assertIsInstance(obj, list)
        self.assertEqual(len(obj), 0)
        self.ext = self.ie.new(
            name="test extension",
            subjects=test_extension['perimeter']['subjects'].values(),
            objects=test_extension['perimeter']['objects'].values(),
            metadata=test_extension['configuration']['metadata'],
            rules=test_extension['configuration']['rules'],
            description=test_extension['description'],
            profiles=test_extension['profiles']
        )
        self.assertIsInstance(self.ext, Extension)
        obj = self.ie.list()
        self.assertIsInstance(obj, list)
        self.assertEqual(len(obj), 1)
        self.assertIsInstance(obj[0], Extension)

    def test_update_element(self):
        self.ext = self.ie.new(
            name="test extension",
            uuid=str(uuid.uuid4()).replace("-", ""),
            subjects=test_extension['perimeter']['subjects'].values(),
            objects=test_extension['perimeter']['objects'].values(),
            metadata=test_extension['configuration']['metadata'],
            rules=test_extension['configuration']['rules'],
            description=test_extension['description'],
            profiles=test_extension['profiles']
        )
        self.assertIsInstance(self.ext, Extension)
        subjects = test_extension['perimeter']['subjects'].values()
        subjects.append(
            {
                "name": "demo3",
                "description": "demo 3"
            }
        )
        answer = self.ie.new(uuid=self.ext.uuid, subjects=subjects)
        self.assertIsInstance(answer, Extension)
        self.assertIn("demo3", map(lambda x: x["name"], answer.subjects))
        self.assertIn("demo 3", map(lambda x: x["description"], answer.subjects))
        obj = self.ie.get(uuid=self.ext.uuid)
        self.assertIsInstance(obj, list)
        self.assertIsInstance(obj[0], Extension)
        subject_names = map(lambda x: x["name"], obj[0].subjects)
        subject_descriptions = map(lambda x: x["description"], obj[0].subjects)
        self.assertIn("demo3", subject_names)
        self.assertIn("demo 3", subject_descriptions)
        #At last, delete the updated element
        answer = self.ie.delete(uuid=self.ext.uuid)
        self.assertIsInstance(answer, dict)
        self.assertEqual(answer["err"], None)
