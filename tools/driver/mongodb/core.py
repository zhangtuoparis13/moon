from pymongo import MongoClient
from uuid import UUID, uuid4
import logging

logger = logging.getLogger(__name__)
# client = MongoClient()
# database = client.moon
# collection = database.extensions


class DB:

    def __init__(self, name=None, collection_name="extensions"):
        self.client = MongoClient()
        self.database = self.client.moon
        self.collection = self.database.extensions
        if name:
            self.database = eval("self.client.{}".format(name))
        self.collection = eval("self.database.{}".format(collection_name))

    # def create(self, name=None, collection_name="extensions"):
    #     if name:
    #         self.database = eval("client.{}".format(name))
    #     collection = eval("database.{}".format(collection_name))
    #     print("mongodb collection={}".format(collection))

    def list(self, type=None):
        """Return a list of extensions with attributes"""
        if type:
            collections = tuple(self.collection.find({"type": type}))
        else:
            collections = tuple(self.collection.find({}))
        for item in collections:
            item["uuid"] = item.pop("_id")
        return collections

    def get(self, attributes=dict()):
        """Return a list of extensions with attributes"""
        if "uuid" in attributes:
            attributes["_id"] = attributes.pop("uuid")
        collections = tuple(self.collection.find(attributes))
        for item in collections:
            item["uuid"] = item.pop("_id")
        return collections

    def count(self, attributes=dict()):
        """Return the number of document in this collection given the attributes"""
        if "uuid" in attributes:
            attributes["_id"] = attributes.pop("uuid")
        return self.collection.find(attributes).count()

    # def new_extension(
    #         self,
    #         uuid=None,
    #         name="",
    #         subjects=[],
    #         objects=[],
    #         metadata=[],
    #         rules=[],
    #         profiles=[],
    #         description="",
    #         tenant={},
    #         json_data={}):
    #     """Create a new Intra-extension
    #     return: created UUID
    #     """
    #     if json_data:
    #         if "uuid" in json_data.keys():
    #             json_data["_id"] = str(json_data["uuid"])
    #             json_data.pop("uuid")
    #         elif "_id" not in json_data.keys():
    #             json_data["_id"] = str(uuid4())
    #         # print(json_data["_id"])
    #         # print(json_data["tenant"])
    #         return self.collection.insert(json_data)
    #     else:
    #         post = dict()
    #         if uuid:
    #             # if type(uuid) is str:
    #             #     uuid = UUID(uuid)
    #             post["_id"] = str(uuid)
    #         else:
    #             post["_id"] = str(uuid4())
    #         post["name"] = name
    #         post["tenant"] = tenant
    #         post["perimeter"] = {}
    #         post["perimeter"]["subjects"] = subjects
    #         post["perimeter"]["objects"] = objects
    #         post["description"] = description
    #         post["profiles"] = profiles
    #         post["configuration"] = {}
    #         post["configuration"]["metadata"] = metadata
    #         post["configuration"]["rules"] = rules
    #         post["type"] = "extension"
    #         myuuid = self.collection.insert(post)
    #         return myuuid

    # def set_extension(
    #         self,
    #         uuid=None,
    #         name="",
    #         subjects=None,
    #         objects=None,
    #         metadata=None,
    #         rules=None,
    #         profiles=None,
    #         description=None):
    #     new_uuid = None
    #     if not uuid:
    #         new_uuid = self.new_extension(
    #             name=name,
    #             subjects=subjects,
    #             objects=objects,
    #             metadata=metadata,
    #             rules=rules,
    #             profiles=profiles,
    #             description=description)
    #     else:
    #         attr = {}
    #         if subjects:
    #             attr["perimeter"] = dict()
    #             attr["perimeter"]['subjects'] = subjects
    #         if objects:
    #             if "perimeter" not in attr:
    #                 attr["perimeter"] = dict()
    #             attr["perimeter"]['objects'] = objects
    #         if metadata:
    #             attr["configuration"] = dict()
    #             attr['metadata'] = metadata
    #         if rules:
    #             if "configuration" not in attr:
    #                 attr["configuration"] = dict()
    #             attr['rules'] = rules
    #         if profiles:
    #             attr['profiles'] = profiles
    #         if description:
    #             attr['description'] = description
    #         attr['name'] = name
    #         if type(uuid) is str:
    #             uuid = str(uuid4())
    #         new_uuid = self.collection.update({"_id": uuid}, attr)
    #         if new_uuid != uuid:
    #             logger.warning("Updating element problem {}".format(uuid))
    #     return new_uuid

    def add(self, attributes={}, uuid=None, mandatory_attrs=[], **kwargs):
        if len(attributes.keys()) > 0:
            for attr in mandatory_attrs:
                if attr not in attributes.keys():
                    raise Exception("Mandatory attributes {} not found".format(attr))
            if "uuid" not in attributes.keys():
                attributes["_id"] = str(uuid4()).replace("-", "")
            else:
                attributes["_id"] = str(attributes.pop("uuid")).replace("-", "")
                if self.count({"_id": attributes["_id"]}) > 0:
                    # logger.info("Updating tenant {}".format(attributes["name"]))
                    uuid = attributes.pop("_id").replace("-", "")
                    return self.collection.update({"_id": uuid}, attributes)
            return self.collection.insert(attributes)
        else:
            post = dict()
            for arg in kwargs:
                post[arg] = kwargs[arg]
            if uuid:
                # if type(uuid) is not UUID:
                #     uuid = str(UUID(uuid))
                if self.count({"_id": str(uuid)}) > 0:
                    # logger.info("Updating tenant {}".format(name))
                    return self.collection.update({"_id": str(uuid)}, post)
                post["_id"] = str(uuid)
            else:
                post["_id"] = str(uuid4()).replace("-", "")
            return self.collection.insert(post)

    def new_extension(
            self,
            uuid=None,
            name="",
            subjects=[],
            objects=[],
            metadata=[],
            rules=[],
            profiles=[],
            description="",
            tenant={},
            json_data={}):
        """Create a new Intra-extension
        return: created UUID
        """
        perimeter = {
            "subjects": subjects,
            "objects": objects
        }
        configuration = {
            "metadata": metadata,
            "rules": rules
        }
        return self.add(
            uuid=uuid,
            mandatory_attrs=["name", "perimeter", "configuration", "profiles", "tenant"],
            name=name,
            perimeter=perimeter,
            configuration=configuration,
            profiles=profiles,
            description=description,
            tenant=tenant,
            type="extension")

    def add_user(
            self,
            attributes={},
            name="",
            mail="",
            description="",
            enabled=True,
            domain="",
            project="",
            uuid=None):
        return self.add(
            attributes=attributes,
            uuid=uuid,
            mandatory_attrs=["name", "enabled"],
            name=name,
            mail=mail,
            description=description,
            enabled=enabled,
            domain=domain,
            project=project
        )

    def add_role(
            self,
            attributes={},
            name="",
            description="",
            enabled=True,
            uuid=None):
        return self.add(
            attributes=attributes,
            uuid=uuid,
            mandatory_attrs=["value", "enabled"],
            name=name,
            description=description,
            enabled=enabled
        )

    def add_tenant(
            self,
            attributes={},
            name="",
            description="",
            enabled=True,
            domain="",
            uuid=None):
        return self.add(
            attributes=attributes,
            uuid=uuid,
            mandatory_attrs=["name", "enabled"],
            name=name,
            description=description,
            enabled=enabled,
            domain=domain,
            type="tenant"
        )
        # if len(attributes.keys()) > 0:
        #     for attr in ("name", "enabled"):
        #         if attr not in attributes.keys():
        #             return None
        #     if "uuid" not in attributes.keys():
        #         attributes["_id"] = uuid4()
        #     else:
        #         if type(attributes["uuid"]) is not UUID:
        #             attributes["uuid"] = UUID(attributes["uuid"])
        #         attributes["_id"] = attributes["uuid"]
        #         attributes.pop("uuid")
        #         if self.count({"_id": attributes["_id"]}) > 0:
        #             # logger.info("Updating tenant {}".format(attributes["name"]))
        #             uuid = attributes.pop("_id")
        #             return self.collection.update({"_id": uuid}, attributes)
        #     return self.collection.insert(attributes)
        # else:
        #     post = dict()
        #     post["name"] = name
        #     post["description"] = description
        #     post["enabled"] = enabled
        #     post["domain"] = domain
        #     if uuid:
        #         if type(uuid) is not UUID:
        #             uuid = UUID(uuid)
        #         if self.count({"_id": uuid}) > 0:
        #             # logger.info("Updating tenant {}".format(name))
        #             return self.collection.update({"_id": uuid}, post)
        #         post["_id"] = uuid
        #     else:
        #         post["_id"] = uuid4()
        #     return self.collection.insert(post)

    def add_tenant_assignment(
            self,
            attributes={},
            requesting=None,
            requested=None,
            type=None,
            category=None,
            uuid=None):
        return self.add(
            attributes=attributes,
            uuid=uuid,
            mandatory_attrs=["requesting", "requested", "connection_type", "category"],
            requesting=requesting,
            requested=requested,
            connection_type=type,
            category=category,
            type="assignment"
        )
        # if len(attributes.keys()) > 0:
        #     for attr in ("requesting", "requested", "type", "category"):
        #         if attr not in attributes.keys():
        #             return None
        #     return self.collection.insert(attributes)
        # else:
        #     post = dict()
        #     post["requesting"] = requesting
        #     post["requested"] = requested
        #     post["type"] = type
        #     post["category"] = category
        #     if uuid:
        #         if type(uuid) is not UUID:
        #             uuid = UUID(uuid)
        #         if self.count({"_id": uuid}) > 0:
        #             return self.collection.update({"_id": uuid}, post)
        #         post["_id"] = uuid
        #     else:
        #         post["_id"] = uuid4()
        #     return self.collection.insert(post)

    def drop(self):
        self.collection.drop()

    def delete(self, uuid):
        myuuid = self.collection.remove({"_id": uuid})
        return myuuid