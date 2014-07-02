from uuid import uuid4, UUID
try:
    from django.utils.safestring import mark_safe
except ImportError:
    mark_safe = str
import logging
from moon.inter_extension_manager import get_dispatcher

logger = logging.getLogger(__name__)


class VirtualEntity:

    def __init__(self, name, uuid=None):
        self.name = name
        self.dispatcher = get_dispatcher()
        self.type = "virtual_entity"
        if not uuid:
            self.uuid = str(uuid4()).replace("-", "")
        else:
            self.uuid = str(uuid).replace("-", "")

    def sync(self):
        post = dict()
        post["name"] = self.name
        post["uuid"] = self.uuid
        post["type"] = self.type
        self.dispatcher.add(attributes=post)

    def __repr__(self):
        return "Virtual Entity {}".format(self.name)


class Tenant:

    def __init__(
            self,
            name="",
            description="",
            enabled=True,
            domain="Default",
            uuid=None):
        self.name = name
        self.description = description
        self.enabled = enabled
        self.domain = domain
        self.type = "tenant"
        if uuid and type(uuid) in (str, unicode):
            self.uuid = uuid
        elif uuid and type(uuid) is UUID:
            self.uuid = str(uuid)
        else:
            self.uuid = str(uuid4()).replace("-", "")
        self.dispatcher = get_dispatcher()

    def create(self,
               name="",
               domain="",
               description="",
               enabled=True):
        """
        Create the tenant in Moon database and Keystone database
        """
        #TODO: add the creation process
        # ktenant = self.kclient.projects.create(
        #     name=name,
        #     domain=domain,
        #     description=description,
        #     enabled=enabled
        # )
        # mtenant = Tenant(
        #     name=name,
        #     domain=domain,
        #     uuid=ktenant.id,
        #     description=description,
        #     enabled=enabled
        # )
        # driver.set_tenant(mtenant)
        # # TODO: check if Keystone creation was successful
        # logger.info("Add tenant {}".format(str(mtenant)))
        # self.tenants[mtenant.uuid] = mtenant
        return None

    def sync(self):
        post = dict()
        post["name"] = self.name
        post["uuid"] = self.uuid
        post["description"] = self.description
        post["enabled"] = self.enabled
        post["domain"] = self.domain
        post["type"] = self.type
        self.dispatcher.add(attributes=post)

    def __repr__(self):
        return "{} ({}) enabled: {}".format(self.name, self.uuid, self.enabled)


class InterExtension:

    def __init__(
            self,
            name="",
            uuid=None,
            requesting_tenant=None,
            requested_tenant=None,
            requesting_tenant_name=None,
            requested_tenant_name=None,
            connection_type=None,
            category=None,
            description=""
    ):
        """ Create a relation between 2 tenants
        :param name: str: name of the relation
        :param uuid: str: uuid of the relation
        :param requesting_tenant: dict: source tenant of the relation (where subject is)
        :param requested_tenant: dict: destination tenant of the relation (where the object is)
        :param connection_type: str: type of connection (example trust, coordinate, ...)
        :param category: str: link to the Virtual entity
        :return: the extension
        """
        self.name = name
        if uuid and type(uuid) in (str, unicode):
            self.uuid = uuid.replace("-", "")
        elif uuid and type(uuid) is UUID:
            self.uuid = str(uuid).replace("-", "")
        else:
            self.uuid = str(uuid4()).replace("-", "")
        self.requesting_tenant = requesting_tenant
        self.requested_tenant = requested_tenant
        self.connection_type = connection_type
        self.category = category
        self.type = "assignment"
        self.description = description
        if requesting_tenant_name:
            self.requesting_tenant_name = requesting_tenant_name
        else:
            self.requesting_tenant_name = requesting_tenant
        if requested_tenant_name:
            self.requested_tenant_name = requested_tenant_name
        else:
            self.requested_tenant_name = requested_tenant
        self.dispatcher = get_dispatcher()

    def sync(self):
        post = dict()
        post['uuid'] = str(self.uuid)
        if type(self.requesting_tenant) in (str, unicode):
            post['requesting'] = self.requesting_tenant
        else:
            post['requesting'] = self.requesting_tenant["uuid"]
        if type(self.requested_tenant) in (str, unicode):
            post['requested'] = self.requested_tenant
        else:
            post['requested'] = self.requested_tenant["uuid"]
        post['connection_type'] = self.connection_type
        post['category'] = self.category
        post['type'] = self.type
        post['name'] = self.name
        post['description'] = self.description
        self.dispatcher.add(attributes=post)

    def __repr__(self):
        return "Extension {} ({}) ({} -> {}: {}/{})".format(
            self.name,
            self.uuid,
            self.requesting_tenant_name,
            self.requested_tenant_name,
            self.connection_type,
            self.category)

    def html(self):
        return mark_safe("<b>Extension</b> {} <br/>"
                         "{} -> {}<br/>connection type: {} <br/>vent: {}".format(
            self.name,
            self.requesting_tenant_name,
            self.requested_tenant_name,
            self.connection_type,
            self.category
        ))


class InterExtensions:

    def __init__(self):
        self.dispatcher = get_dispatcher()
        self.extensions = {}
        #TODO: put tenants outside
        self.tenants = {}
        self.virtual_entities = {}
        #FIXME: when using the link named "sync" in the interface after a drop database,
        # the InterExtensions is initialized twice
        for tenant in self.dispatcher.list(type="tenant"):
            t = Tenant(
                uuid=tenant["uuid"],
                name=tenant["name"],
                description=tenant["description"],
                enabled=tenant["enabled"],
                domain=tenant["domain"]
            )
            t.sync()
            self.tenants[tenant["uuid"]] = t
        for ext in self.dispatcher.list(type="assignment"):
            e = InterExtension(
                uuid=ext["uuid"],
                name=ext["name"],
                requesting_tenant=ext["requesting"],
                requesting_tenant_name=self.tenants[ext["requesting"]].name,
                requested_tenant=ext["requested"],
                requested_tenant_name=self.tenants[ext["requested"]].name,
                connection_type=ext["connection_type"],
                category=ext["category"]
            )
            e.sync()
            self.extensions[ext["uuid"]] = e
        for vent in self.dispatcher.list(type="virtual_entity"):
            v = VirtualEntity(
                uuid=vent["uuid"],
                name=vent["name"],
            )
            v.sync()
            self.virtual_entities[vent["uuid"]] = v

    def __getitem__(self, item):
        return self.extensions[item]

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
            uuids = map(lambda x: x["uuid"], tuple(self.dispatcher.get(attributes=attributes)))
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
        return self.dispatcher.delete(uuid=uuid)

    def delete_tables(self):
        logger.warning("Dropping Inter Extension Database")
        self.extensions = dict()
        self.tenants = dict()
        return self.dispatcher.drop()

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
        answer = self.dispatcher.add_tenant(
            attributes=attributes,
            name=name,
            description=description,
            enabled=enabled,
            domain=domain,
            uuid=uuid)
        if "err" in answer and answer["err"]:
            raise Exception("Error add tenant in DB ({})".format(answer["err"]))
        tenant = self.dispatcher.get({"uuid": uuid})
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
        self.tenants[tenant["uuid"]].sync()
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
            #FIXME vent can have the same name with this method
            vent = VirtualEntity(requesting+"->"+requested)
            vent.sync()
            self.virtual_entities[vent.uuid] = vent
            category = vent.uuid
        assignment = self.dispatcher.add_tenant_assignment(
            attributes=attributes,
            requesting=requesting,
            requested=requested,
            type=type,
            category=category,
            uuid=uuid)
        self.extensions[assignment] = InterExtension(
            requesting_tenant=requesting,
            requesting_tenant_name=self.tenants[requesting].name,
            requested_tenant=requested,
            requested_tenant_name=self.tenants[requested].name,
            connection_type=type,
            category=category,
            uuid=uuid
        )
        self.extensions[assignment].sync()
        return self.extensions[assignment]

inter_extentions = InterExtensions()


def get_inter_extentions():
    return inter_extentions