import logging
from moon import settings
import importlib

logger = logging.getLogger("moon.driver_dispatcher")

DATABASES = getattr(settings, "DATABASES")
if not 'user_db' in DATABASES or not 'ENGINE' in DATABASES['user_db']:
    raise(Exception("Unknown database engine {engine}".format(engine=DATABASES['user_db']['ENGINE'])))

drivername = DATABASES['user_db']['ENGINE']
driver = importlib.import_module(drivername)


class Users:
    """
    Class for all users
    """
    def __init__(self, kclient):
        self.kclient = kclient

    def create(self,
               name="",
               password="",
               domain="",
               project="",
               email="",
               description="",
               enabled=True):
        """
        Create the user in Moon database and Keystone database
        """
        kuser = self.kclient.users.create(
            name=name,
            password=password,
            domain=domain,
            project=project,
            email=email,
            description=description,
            enabled=enabled
        )
        muser = driver.User(
            name=name,
            password=password,
            uuid=kuser.id,
            domain=domain,
            project=project,
            email=email,
            description=description,
            enabled=enabled
        )
        logger.info("Add {}".format(str(muser)))
        # TODO: check if Keystone creation was successfull
        driver.add_user_to_userdb(kuser)
        return muser

    def list(self, sort=True):
        """
        Return all users from the Keystone service.
        """
        if sort:
            users = sorted(self.kclient.users.list(), key=lambda _user: _user.name)
        else:
            users = self.kclient.users.list()
        return users

    def get_user(self, name=None, uuid=None):
        """
        Return a specific user from the Keystone service.
        """
        user = ()
        # TODO: add search by name
        for _user in self.kclient.users.list():
            if _user.id == uuid:
                user = _user
        user.project = user.default_project_id
        for _project in self.kclient.projects.list():
            if user.default_project_id == _project.id:
                user.project = _project.name
        user.domain = user.domain_id
        return user


def get_user_session():
    """
    Return the session associated with the User DB
    """
    return driver.UserSession()


def create_tables():
    """
    Create all tables in database.
    """
    driver.create_tables()


def populate_dbs(username="admin", password=None, domain="Default"):
    """
    Populated for the first time the User DB with the content of the Keystone DB.
    """
    logger.info("Populate Database with information from Keystone server")
    if not password:
        import getpass
        password = getpass.getpass("Keystone password for {user} on [{url}]:".format(
            user=username,
            url=getattr(settings, 'OPENSTACK_KEYSTONE_URL', "")
        ))
    from keystoneclient.v3 import client
    c = client.Client(
        username=username,
        password=password,
        user_domain_name=domain,
        region_name="regionOne",
        #endpoint=getattr(settings, 'OPENSTACK_KEYSTONE_URL', ""),
        # insecure=True,
        # cacert=None,
        auth_url=getattr(settings, 'OPENSTACK_KEYSTONE_URL', ""),
        # debug=settings.DEBUG
    )
    c.management_url = getattr(settings, 'OPENSTACK_KEYSTONE_URL', "")
    for u in c.users.list():
        driver.add_user_to_userdb(u)
        # logger.debug("User {}".format(dir(u)))
    for r in c.roles.list():
        for u in c.users.list():
            for t in c.projects.list(user=u):
                # try:
                    # logger.info("{user} {role} {tenant}, {bool}".format(
                    #     user=u,
                    #     role=r,
                    #     tenant=t,
                    #     bool=c.roles.check(r, user=u, project=t))
                    # )
                driver.add_role_to_userdb(role=r, project=t)
                driver.add_userroleassignment_to_userdb(user=u, role=r)
                # except: pass


def sync_user_db():
    """
    Synchronise when needed from the remote Keystone DB to the local User DB.
    """
    # TODO: define arguments and add synchronisation.
    pass


def get_user(uuid=None, name=None):
    """
    Get a user with his name or UUID
    """
    return driver.get_user(uuid=uuid, name=name)


def get_role(uuid=None, name=None, project_uuid=None):
    """
    Get a role with his name or UUID on a specific project
    """
    return driver.get_role(uuid=uuid, name=name, project_uuid=project_uuid)