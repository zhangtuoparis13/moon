import logging
import json
from moon import settings
import importlib
from models import Extension

logger = logging.getLogger(__name__)

DATABASES = getattr(settings, "DATABASES")
if not 'intra-extensions' in DATABASES or not 'ENGINE' in DATABASES['intra-extensions']:
    raise(Exception("Unknown database engine {engine}".format(engine=DATABASES['intra-extensions']['ENGINE'])))

drivername = DATABASES['intra-extensions']['ENGINE']
db_name = DATABASES['intra-extensions']['NAME']
driver = importlib.import_module(drivername)


class IntraExtensions:

    def __init__(self):
        self.db = driver.DB(name=db_name, collection_name="extensions")
        # print(self.db.list(type="extension"))
        self.extensions = {}
        for ext in self.db.list(type="extension"):
            # print("__init__ {}".format(str(ext)))
            self.extensions[ext["uuid"]] = Extension(
                name=ext["name"],
                uuid=ext["uuid"],
                subjects=ext["perimeter"]["subjects"],
                objects=ext["perimeter"]["objects"],
                metadata=ext["configuration"]["metadata"],
                rules=ext["configuration"]["rules"],
                profiles=ext["profiles"],
                description=ext["description"],
                tenant=ext["tenant"]
            )

    def list(self, ):
        # return self.db.list(type="extensions")
        return self.extensions.values()

    def get(self, uuid=None, attributes=dict()):
        if uuid:
            attributes = {"uuid": uuid}
        return tuple(self.db.get(attributes=attributes))

    # def sync_extension(self, tenant_uuid, users, roles, groups):
    #     for ext in self.db.list():
    #         if ext["tenant"]["uuid"] == tenant_uuid:
    #             print("found extension", tenant_uuid)

    def new_from_json(self, json_data):
        # name = json_data["name"]
        # subjects = json_data["perimeter"]["subjects"]
        # objects = json_data["perimeter"]["objects"]
        # metadata = json_data["configuration"]["metadata"]
        # rules = json_data["configuration"]["rules"]
        # profiles = json_data["profiles"]
        # description = json_data["description"]
        # # print(json.dumps(json_data, indent=4))
        # return self.db.new_extension(
        #     uuid=None,
        #     name=name,
        #     subjects=subjects,
        #     objects=objects,
        #     metadata=metadata,
        #     rules=rules,
        #     profiles=profiles,
        #     description=description)
        all_tenants = map(lambda x: x.tenant["uuid"], self.extensions.values())
        if json_data["tenant"]["uuid"] not in all_tenants:
            ext = Extension(
                name=json_data["name"],
                uuid=json_data["uuid"],
                subjects=json_data["perimeter"]["subjects"],
                objects=json_data["perimeter"]["objects"],
                metadata=json_data["configuration"]["metadata"],
                rules=json_data["configuration"]["rules"],
                profiles=json_data["profiles"],
                description=json_data["description"],
                tenant=json_data["tenant"]
            )
            ext.sync(self.db)
            self.extensions[json_data["uuid"]] = ext
            return ext
        else:
            return None

    # def set(
    #         self,
    #         name="",
    #         uuid=None,
    #         subjects=None,
    #         objects=None,
    #         metadata=None,
    #         rules=None,
    #         profiles=None,
    #         description=""):
    #     return self.db.set_extension(
    #         uuid=uuid,
    #         name=name,
    #         subjects=subjects,
    #         objects=objects,
    #         metadata=metadata,
    #         rules=rules,
    #         profiles=profiles,
    #         description=description)

    def new(
            self,
            uuid=None,
            name="",
            subjects=None,
            objects=None,
            metadata=None,
            rules=None,
            profiles=None,
            description=""):
        """Create a new Intra-extension
        :param uuid: uuid of this extension (optional)
        :param name: name of this extension
        :param subjects: list of subjects example:
            [{
                "uuid": "user1_uuid",
                "name": "admin",
                "mail": "admin@localhost",
                "tenant_id": "0123456789",
                "description": "an administrator",
                "enabled": True
            },]
        :param objects: list of objects example:
            [{
                "uuid": "object1_uuid",
                "name": "vm1",
                "description": "the virtual machine number 1",
                "enabled": True
            },]
        :param metadata: list of authorized attributes for subject and object, example:
            {
                "subject": [
                    "role",
                    "group"
                ],
                "object": [
                    "type",
                    "security"
                ]
            }
        :param rules: list of rules, example:
            [{
                "name": "rule1",
                "s_attr": { "category": "role", "value": "subject_attribute_uuid1" },
                "o_attr": { "category": "type", "value": "object_attribute_uuid1" },
                "a_attr": { "category": "action", "value": "list" },
                "description": "..."
            },]
        :param profiles: list of profiles, example:
            {
                "s_attr": {
                    "s_attr_uuid1": {
                        "category": "role",
                        "value": "admin",
                        "description": "le role admin"
                    },
                    "s_uuid2": {
                        "category": "role",
                        "value": "dev"
                    },
                    "s_uuid3": {
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
                    "o_uuid2": {
                        "category": "size",
                        "value": "medium"
                    }
                },
                "s_attr_assign": {
                    "assign1_uuid": {
                        "subject": "user1_uuid",
                        "attributes": [ "s_uuid1", "s_uuid3" ]
                    },
                    "assign2_uuid": {
                        "subject": "user3_uuid",
                        "attributes": [ "s_uuid1", "s_uuid2", "s_uuid3" ]
                    }
                },
                "o_attr_assign": {
                    "assign3_uuid": {
                        "object": "object1_uuid",
                        "attributes": [ "o_uuid1", "o_uuid3" ]
                    },
                    "assign4_uuid": {
                        "object": "object3_uuid",
                        "attributes": [ "o_uuid1", "o_uuid2", "o_uuid3" ]
                    }
                }
            }
        :param description: string describing the new extension.
        :return the created UUID
        """
        return self.db.new_extension(
            uuid=uuid,
            name=name,
            subjects=subjects,
            objects=objects,
            metadata=metadata,
            rules=rules,
            profiles=profiles,
            description=description)

    # def add_user(self, user):
    #     return self.db.add_user(user)
    #
    # def add_role(self, role):
    #     return self.db.add_role(role)

    def delete(self, uuid):
        self.extensions.pop(uuid)
        return self.db.delete(uuid=uuid)

    def delete_tables(self):
        logger.warning("Dropping Intra Extension Database")
        self.extensions = dict()
        return self.db.drop()

driver_dispatcher = IntraExtensions()


def get_dispatcher():
    return driver_dispatcher