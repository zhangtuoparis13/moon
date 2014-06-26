from pymongo import MongoClient
from uuid import UUID, uuid4
import logging

logger = logging.getLogger(__name__)


class DB:

    def __init__(self, name=None, collection_name="extensions"):
        self.client = MongoClient()
        self.database = self.client.moon
        self.collection = self.database.extensions
        if name:
            self.database = eval("self.client.{}".format(name))
        self.collection = eval("self.database.{}".format(collection_name))

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
        print(self.collection)
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
            project=project,
            type="subject"
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
            enabled=enabled,
            type="role"
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

    def drop(self):
        self.collection.drop()

    def delete(self, uuid):
        myuuid = self.collection.remove({"_id": uuid})
        return myuuid