from uuid import uuid4, UUID
try:
    from django.utils.safestring import mark_safe
except ImportError:
    mark_safe = str


class VirtualEntity:

    def __init__(self, name, uuid=None):
        self.name = name
        self.db = None
        self.type = "virtual_entity"
        if not uuid:
            self.uuid = str(uuid4()).replace("-", "")
        else:
            self.uuid = str(uuid).replace("-", "")

    def sync(self, db):
        self.db = db
        post = dict()
        post["name"] = self.name
        post["uuid"] = self.uuid
        post["type"] = self.type
        self.db.add(attributes=post)

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

    def sync(self, db):
        post = dict()
        post["name"] = self.name
        post["uuid"] = self.uuid
        post["description"] = self.description
        post["enabled"] = self.enabled
        post["domain"] = self.domain
        post["type"] = self.type
        db.add(attributes=post)

    def __repr__(self):
        return "{} ({}) enabled: {}".format(self.name, self.uuid, self.enabled)


class Extension:

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

    def sync(self, db):
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
        db.add(attributes=post)

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