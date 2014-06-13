from uuid import uuid4, UUID


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
            connection_type=None,
            category=None
    ):
        self.name = name
        if uuid and type(uuid) is str:
            self.uuid = UUID(uuid)
        elif uuid and type(uuid) is UUID:
            self.uuid = uuid
        else:
            self.uuid = uuid4().replace("-", "")
        self.requesting_tenant = requesting_tenant,
        self.requested_tenant = requested_tenant,
        self.connection_type = connection_type,
        self.category = category

    def sync(self, db):
        post = dict()
        post['name'] = self.name
        post['uuid'] = str(self.uuid)
        if type(self.requesting_tenant) is str:
            post['requesting_tenant'] = self.requesting_tenant
        else:
            post['requesting_tenant'] = self.requesting_tenant["uuid"]
        if type(self.requested_tenant) is str:
            post['requested_tenant'] = self.requested_tenant
        else:
            post['requested_tenant'] = self.requested_tenant["uuid"]
        post['connection_type'] = self.connection_type
        post['category'] = self.category
        db.add(attributes=post)

    def __repr__(self):
        return "Extension {} ({}) enabled: {} ({}->{}:{}/{})".format(
            self.name,
            self.uuid,
            self.requesting_tenant,
            self.requested_tenant,
            self.connection_type,
            self.category)