"""
Policy information Point
"""
from moon.user_repository import driver_dispatcher
from moon import settings
import logging

logger = logging.getLogger("moon.pip")


def create_tables():
    """
    Create all tables in database.
    """
    driver_dispatcher.create_tables()


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
        driver_dispatcher.add_user_to_userdb(u)
        # logger.debug("User {}".format(dir(u)))
    for r in c.roles.list():
        for u in c.users.list():
            for t in c.projects.list(user=u):
                driver_dispatcher.add_role_to_userdb(role=r, project=t)
                driver_dispatcher.add_userroleassignment_to_userdb(user=u, role=r)

