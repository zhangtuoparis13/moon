import logging
from moon import settings
import importlib

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

    def create(self,
               name="",
               domain="",
               description="",
               enabled=True):
        """
        Create the user in Moon database and Keystone database
        """
        mtenant = driver.Tenant(
            name=name,
            domain=domain,
            description=description,
            enabled=enabled
        )
        kuser = self.kclient.create(name, domain, description, enabled)
        # TODO: check if Keystone creation was successfull
        driver.add_user_to_userdb(mtenant)
        return None

    def list(self, sort=True):
        """
        Return all users from the Keystone service.
        """
        # if sort:
        #     users = sorted(self.kclient.users.list(), key=lambda _user: _user.name)
        # else:
        #     users = self.kclient.users.list()
        return []

    def get_tenant(self, name=None, uuid=None):
        """
        Return a specific user from the Keystone service.
        """
        # user = ()
        # # TODO: add search by name
        # for _user in self.kclient.users.list():
        #     if _user.id == uuid:
        #         user = _user
        # user.project = user.default_project_id
        # for _project in self.kclient.projects.list():
        #     if user.default_project_id == _project.id:
        #         user.project = _project.name
        # user.domain = user.domain_id
        return None


# def get_user_session():
#     """
#     Return the session associated with the User DB
#     """
#     return driver.UserSession()


def create_tables():
    """
    Create all tables in database.
    """
    driver.create_tables()


def add_element_from_keystone(tenant=None):
    """
    Add an object in a database table based on Keystone object
    """
    driver.add_project_to_tenantdb(tenant=tenant)


def get_tenant(uuid=None):
    return driver.get_tenant(uuid=uuid)


def get_tenants():
    return driver.get_tenants()


def set_tenant_relationship(tenant_up="", tenant_bottom=""):
    """
    Set relationship between 2 tenants
    Attributes can be uuid or name
    """
    driver.set_tenant_relationship(tenant_up=tenant_up, tenant_bottom=tenant_bottom)


def unset_tenant_relationship(tenant_up="", tenant_bottom=""):
    """
    Unset relationship between 2 tenants
    Attributes can be uuid or name
    """
    driver.unset_tenant_relationship(tenant_up=tenant_up, tenant_bottom=tenant_bottom)

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

