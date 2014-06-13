import unittest
from moon import settings
import uuid
from moon.intra_extension_manager import get_dispatcher
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
        self.uuid = self.ie.new(
            name="test extension",
            subjects=test_extension['perimeter']['subjects'].values(),
            objects=test_extension['perimeter']['objects'].values(),
            metadata=test_extension['configuration']['metadata'],
            rules=test_extension['configuration']['rules'],
            description=test_extension['description'],
            profiles=test_extension['profiles']
        )
        self.assertIsInstance(self.uuid, uuid.UUID)
        answer = self.ie.delete(uuid=self.uuid)
        self.assertIsInstance(answer, dict)
        self.assertEqual(answer["err"], None)

    def test_add_and_delete_element_with_uuid(self):
        self.uuid = self.ie.new(
            name="test extension",
            uuid=uuid.uuid4(),
            subjects=test_extension['perimeter']['subjects'].values(),
            objects=test_extension['perimeter']['objects'].values(),
            metadata=test_extension['configuration']['metadata'],
            rules=test_extension['configuration']['rules'],
            description=test_extension['description'],
            profiles=test_extension['profiles']
        )
        self.assertIsInstance(self.uuid, uuid.UUID)
        answer = self.ie.delete(uuid=self.uuid)
        self.assertIsInstance(answer, dict)
        self.assertEqual(answer["err"], None)

    def test_list_elements(self):
        self.ie.delete_tables()
        obj = self.ie.list()
        self.assertIsInstance(obj, tuple)
        self.assertEqual(len(obj), 0)
        self.uuid = self.ie.new(
            name="test extension",
            subjects=test_extension['perimeter']['subjects'].values(),
            objects=test_extension['perimeter']['objects'].values(),
            metadata=test_extension['configuration']['metadata'],
            rules=test_extension['configuration']['rules'],
            description=test_extension['description'],
            profiles=test_extension['profiles']
        )
        self.assertIsInstance(self.uuid, uuid.UUID)
        obj = self.ie.list()
        self.assertIsInstance(obj, tuple)
        self.assertEqual(len(obj), 1)
        self.assertIsInstance(obj[0], dict)

    def test_update_element(self):
        self.uuid = self.ie.new(
            name="test extension",
            uuid=uuid.uuid4(),
            subjects=test_extension['perimeter']['subjects'].values(),
            objects=test_extension['perimeter']['objects'].values(),
            metadata=test_extension['configuration']['metadata'],
            rules=test_extension['configuration']['rules'],
            description=test_extension['description'],
            profiles=test_extension['profiles']
        )
        self.assertIsInstance(self.uuid, uuid.UUID)
        subjects = test_extension['perimeter']['subjects'].values()
        subjects.append(
            {
                "name": "demo3",
                "description": "demo 3"
            }
        )
        answer = self.ie.set(uuid=self.uuid, subjects=subjects)
        self.assertIsInstance(answer, dict)
        self.assertEqual(answer["err"], None)
        obj = self.ie.get(uuid=self.uuid)
        self.assertIsInstance(obj, tuple)
        self.assertIsInstance(obj[0], dict)
        subject_names = map(lambda x: x["name"], obj[0]['perimeter']['subjects'])
        subject_descriptions = map(lambda x: x["description"], obj[0]['perimeter']['subjects'])
        self.assertIn("demo3", subject_names)
        self.assertIn("demo 3", subject_descriptions)
        #At last, delete the updated element
        answer = self.ie.delete(uuid=self.uuid)
        self.assertIsInstance(answer, dict)
        self.assertEqual(answer["err"], None)
