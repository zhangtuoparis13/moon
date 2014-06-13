import logging
import json
from moon import settings
import importlib
from models import Extension, Tenant
from uuid import uuid4

logger = logging.getLogger(__name__)

DATABASES = getattr(settings, "DATABASES")
if not 'inter-extensions' in DATABASES or not 'ENGINE' in DATABASES['inter-extensions']:
    raise(Exception("Unknown database engine {engine}".format(engine=DATABASES['inter-extensions']['ENGINE'])))

drivername = DATABASES['inter-extensions']['ENGINE']
db_name = DATABASES['inter-extensions']['NAME']
driver = importlib.import_module(drivername)


class InterExtensions:

    def __init__(self):
        self.db = driver.DB(name=db_name, collection_name="relations")
        self.extensions = {}
        self.tenants = {}
        for tenant in self.db.list(type="tenant"):
            t = Tenant(
                uuid=tenant["uuid"],
                name=tenant["name"],
                description=tenant["description"],
                enabled=tenant["enabled"],
                domain=tenant["domain"]
            )
            t.sync(self.db)
            self.tenants[tenant["uuid"]] = t
        for ext in self.db.list(type="assignment"):
            e = Extension(
                uuid=ext["uuid"],
                name=ext["name"],
                requesting_tenant=ext["questioning_tenant"],
                requested_tenant=ext["questioned_tenant"],
                connection_type=ext["connection_type"],
                category=ext["category"]
            )
            e.sync(self.db)
            self.extensions[ext["uuid"]] = e

    def list(self, type="tenants"):
        if type == "tenants":
            return self.tenants
        else:
            return self.extensions.values()

    def get(self, uuid=None, name=None, attributes=dict()):
        """
        :param uuid: uuid of the extension
        :param name: name of the extension
        :param attributes: other attributes to look for
        :return: a list of extensions
        """
        if not uuid and not name:
            return self.extensions
        elif uuid:
            try:
                return [self.extensions[uuid], ]
            except KeyError:
                return [self.tenants[uuid], ]
        elif name:
            for ext in self.extensions.values():
                if ext.name == name:
                    return [ext, ]
        else:
            #TODO: delete this part ?
            logger.warning("intra_extension_manager in get/else")
            uuids = map(lambda x: x["uuid"], tuple(self.db.get(attributes=attributes)))
            exts = []
            for uuid in uuids:
                try:
                    exts.append(self.extensions[uuid])
                except KeyError:
                    exts.append(self.tenants[uuid])
            return exts

    def delete(self, uuid):
        try:
            self.extensions.pop(uuid)
        except KeyError:
            self.tenants.pop(uuid)
        return self.db.delete(uuid=uuid)

    def delete_tables(self):
        logger.warning("Dropping Inter Extension Database")
        self.extensions = dict()
        self.tenants = dict()
        return self.db.drop()

    def add_tenant(
            self,
            attributes={},
            name="",
            description="",
            enabled=True,
            domain="",
            uuid=None):
        if not uuid:
            uuid = str(uuid4()).replace("-", "")
        answer = self.db.add_tenant(
            attributes=attributes,
            name=name,
            description=description,
            enabled=enabled,
            domain=domain,
            uuid=uuid)
        if "err" in answer and answer["err"]:
            raise Exception("Error add tenant in DB ({})".format(answer["err"]))
        tenant = self.db.get({"uuid": uuid})
        if len(tenant) > 1:
            raise Exception("Error in UUID attribution, multiple tenant have the same UUID ({})".format(uuid))
        tenant = tenant[0]
        self.tenants[tenant["uuid"]] = Tenant(
            name=tenant["name"],
            description=tenant["description"],
            enabled=tenant["enabled"],
            domain=tenant["domain"],
            uuid=tenant["uuid"]
        )
        self.tenants[tenant["uuid"]].sync(self.db)
        return self.tenants[tenant["uuid"]]

    def add_tenant_assignment(
            self,
            attributes={},
            requesting=None,
            requested=None,
            type=None,
            category=None,
            uuid=None):
        assignment = self.db.add_tenant_assignment(
            attributes=attributes,
            requesting=requesting,
            requested=requested,
            type=type,
            category=category,
            uuid=uuid)
        self.extensions[assignment["uuid"]] = Extension(
            requesting_tenant=requesting,
            requested_tenant=requested,
            connection_type=type,
            category=category,
            uuid=uuid
        )
        self.extensions[assignment["uuid"]].sync(self.db)
        return self.extensions[assignment["uuid"]]

driver_dispatcher = InterExtensions()


def get_dispatcher():
    return driver_dispatcher