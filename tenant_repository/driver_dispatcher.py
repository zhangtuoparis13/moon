import logging
from moon import settings
import importlib
from models import Tenant

logger = logging.getLogger("moon.driver_dispatcher")

DATABASES = getattr(settings, "DATABASES")
if not 'tenant_db' in DATABASES or not 'ENGINE' in DATABASES['tenant_db']:
    raise(Exception("Unknown database engine {engine}".format(engine=DATABASES['tenant_db']['ENGINE'])))

drivername = DATABASES['tenant_db']['ENGINE']
driver = importlib.import_module(drivername)


class Tenants:
    """
    Class for all tenants
    """
    def __init__(self, kclient):
        self.kclient = kclient
        __tenants = driver.get_tenants()
        self.tenants = {}
        for tenant in __tenants:
            self.tenants[tenant.uuid] = tenant

    def create(self,
               name="",
               domain="",
               description="",
               enabled=True):
        """
        Create the tenant in Moon database and Keystone database
        """
        ktenant = self.kclient.projects.create(
            name=name,
            domain=domain,
            description=description,
            enabled=enabled
        )
        mtenant = Tenant(
            name=name,
            domain=domain,
            uuid=ktenant.id,
            description=description,
            enabled=enabled
        )
        driver.set_tenant(mtenant)
        # TODO: check if Keystone creation was successful
        logger.info("Add tenant {}".format(str(mtenant)))
        self.tenants[mtenant.uuid] = mtenant
        return mtenant

    def list(self, sort=True):
        """
        Return all users from the Keystone service.
        """
        if sort:
            tenants = sorted(self.tenants.values(), key=lambda _tenant: _tenant.name)
        else:
            tenants = self.tenants.values()
        return tenants

    def get_tenant(self, name=None, uuid=None):
        """
        Return a specific user.
        """
        __tenant = None
        if uuid and uuid in self.tenants.keys():
            __tenant = self.tenants[uuid]
        elif name and name in self.tenants.keys():
            __tenant = self.tenants[name]
        else:
            for tenant in self.tenants.values():
                if name and name == tenant.name:
                    __tenant = tenant
        return __tenant

    def create_tables(self):
        """
        Create all tables in database.
        """
        driver.create_tables()

    def add_element_from_keystone(self, tenant=None):
        """
        Add an object in a database table based on Keystone object
        """
        t = Tenant()
        t.uuid = tenant.id
        t.name = tenant.name
        t.domain = tenant.domain_id
        t.enabled = tenant.enabled
        t.children = list()
        t.parent = ""
        self.tenants[tenant.id] = t
        driver.add_project_to_tenantdb(tenant=t)

    # def get_tenant(self, uuid=None):
    #     return driver.get_tenant(uuid=uuid)
    #
    def get_tenants(self):
        return self.tenants.values()
        # return driver.get_tenants()

    def set_tenant_relationship(self, tenant_up="", tenant_bottom=""):
        """
        Set relationship between 2 tenants
        Attributes can be uuid or name
        """
        # TODO: search for circular connections
        tenant_up_obj = self.get_tenant(tenant_up)
        if not tenant_up_obj:
            raise Exception("Error in setting relationship tenant {} is unknown...".format(tenant_up))
        tenant_bottom_obj = self.get_tenant(tenant_bottom)
        if not tenant_bottom_obj:
            raise Exception("Error in setting relationship tenant {} is unknown...".format(tenant_bottom))
        __children = tenant_up_obj.children
        __children.append(tenant_bottom)
        tenant_up_obj.children = __children
        tenant_bottom_obj.parent = tenant_up
        driver.set_tenant_relationship(tenant_up=tenant_up, tenant_bottom=tenant_bottom)

    def unset_tenant_relationship(self, tenant_up="", tenant_bottom=""):
        """
        Unset relationship between 2 tenants
        Attributes can be uuid or name
        """
        driver.unset_tenant_relationship(tenant_up=tenant_up, tenant_bottom=tenant_bottom)


def add_element_from_keystone(tenant=None):
    """
    Add an object in a database table based on Keystone object
    """
    t = Tenant()
    t.uuid = tenant.id
    t.name = tenant.name
    t.domain = tenant.domain_id
    t.enabled = tenant.enabled
    t.children = list()
    t.parent = ""
    driver.add_project_to_tenantdb(tenant=t)
    print("add tenant {}".format(t.name))

# def populate_dbs(username="admin", password=None, domain="Default"):
#     """
#     Populated for the first time the User DB with the content of the Keystone DB.
#     """
#     logger.info("Populate Database with information from Keystone server")
#     if not password:
#         import getpass
#         password = getpass.getpass("Keystone password for {user} on [{url}]:".format(
#             user=username,
#             url=getattr(settings, 'OPENSTACK_KEYSTONE_URL', "")
#         ))
#     from keystoneclient.v3 import client
#     c = client.Client(
#         username=username,
#         password=password,
#         user_domain_name=domain,
#         region_name="regionOne",
#         #endpoint=getattr(settings, 'OPENSTACK_KEYSTONE_URL', ""),
#         # insecure=True,
#         # cacert=None,
#         auth_url=getattr(settings, 'OPENSTACK_KEYSTONE_URL', ""),
#         # debug=settings.DEBUG
#     )
#     c.management_url = getattr(settings, 'OPENSTACK_KEYSTONE_URL', "")
#     for p in c.projects.list():
#         driver.add_project_to_tenantdb(p)
#     #     # logger.debug("User {}".format(dir(u)))
#     # for r in c.roles.list():
#     #     for u in c.users.list():
#     #         for t in c.projects.list(user=u):
#     #             # try:
#     #                 # logger.info("{user} {role} {tenant}, {bool}".format(
#     #                 #     user=u,
#     #                 #     role=r,
#     #                 #     tenant=t,
#     #                 #     bool=c.roles.check(r, user=u, project=t))
#     #                 # )
#     #             driver.add_role_to_userdb(role=r, project=t)
#     #             driver.add_userroleassignment_to_userdb(user=u, role=r)
#     #             # except: pass

