import logging
import json
from moon import settings
import importlib
from models import Extension, Tenant, VirtualEntity
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
        self.virtual_entities = {}
        #FIXME: when using the link named "sync" in the interface after a drop database,
        # the InterExtensions is initialized twice
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
                requesting_tenant=ext["requesting"],
                requesting_tenant_name=self.tenants[ext["requesting"]].name,
                requested_tenant=ext["requested"],
                requested_tenant_name=self.tenants[ext["requested"]].name,
                connection_type=ext["connection_type"],
                category=ext["category"]
            )
            e.sync(self.db)
            self.extensions[ext["uuid"]] = e
        for vent in self.db.list(type="virtual_entity"):
            v = VirtualEntity(
                uuid=vent["uuid"],
                name=vent["name"],
            )
            v.sync(self.db)
            self.virtual_entities[vent["uuid"]] = v

    def list(self, type="tenants"):
        if type == "tenants":
            return self.tenants.values()
        else:
            return self.extensions.values()

    def get(self, uuid=None, name=None, attributes=dict()):
        """
        :param uuid: uuid of the tenant or extension
        :param name: name of the tenant or extension
        :param attributes: other attributes to look for
        :return: a list of tenants or extensions
        """
        if not uuid and not name and not attributes:
            return self.extensions.values()
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
            uuids = map(lambda x: x["uuid"], tuple(self.db.get(attributes=attributes)))
            exts = []
            for uuid in uuids:
                try:
                    exts.append(self.extensions[uuid])
                except KeyError:
                    exts.append(self.tenants[uuid])
            return exts

    def get_virtual_entity(self, uuid=None, name=None):
        if not uuid and not name:
            return self.virtual_entities.values()
        elif uuid:
            return [self.virtual_entities[uuid], ]
        else:
            for vent in self.virtual_entities:
                if vent.name == name:
                    return [vent, ]

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
        if not uuid:
            uuid = str(uuid4()).replace("-", "")
        if not category:
            vent = VirtualEntity(requesting+"->"+requested)
            vent.sync(self.db)
            self.virtual_entities[vent.uuid] = vent
            category = vent.uuid
        assignment = self.db.add_tenant_assignment(
            attributes=attributes,
            requesting=requesting,
            requested=requested,
            type=type,
            category=category,
            uuid=uuid)
        self.extensions[assignment] = Extension(
            requesting_tenant=requesting,
            requesting_tenant_name=self.tenants[requesting].name,
            requested_tenant=requested,
            requested_tenant_name=self.tenants[requested].name,
            connection_type=type,
            category=category,
            uuid=uuid
        )
        self.extensions[assignment].sync(self.db)
        return self.extensions[assignment]

driver_dispatcher = InterExtensions()


def get_dispatcher():
    return driver_dispatcher