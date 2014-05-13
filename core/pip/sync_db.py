"""
Policy information Point
Database synchronisation between Keystone and Moon
"""
from moon.info_repository import driver_dispatcher as user_dd
from moon.tenant_repository import driver_dispatcher as tenant_dd
from moon import settings
import logging

logger = logging.getLogger("moon.pip")


def create_tables():
    """
    Create all tables in database.
    """
    # driver_dispatcher.build_class_from_dict(cls=getattr(settings, "INITIAL_DB"))
    user_dd.create_tables(cls=getattr(settings, "INITIAL_DB"))


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
    for user in c.users.list():
        user_dd.add_element_from_keystone(user)
    for role in c.roles.list():
        for user in c.users.list():
            for tenant in c.projects.list(user=user):
                user_dd.add_element_from_keystone(role=role, tenant=tenant)
                tenant_dd.add_element_from_keystone(tenant=tenant)
                # driver_dispatcher.add_role_to_userdb(role=role, project=tenant)
                # driver_dispatcher.add_userroleassignment_to_userdb(user=user, role=role)

