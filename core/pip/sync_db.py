"""
Policy information Point
Database synchronisation between Keystone and Moon
"""
from moon.info_repository import driver_dispatcher as user_dd
from moon.tenant_repository import driver_dispatcher as tenant_dd
from moon import settings
import logging
import json

logger = logging.getLogger("moon.pip")

API = json.loads(file(getattr(settings, "OPENSTACK_API")).read())


def create_tables():
    """
    Create all tables in database.
    """
    # driver_dispatcher.build_class_from_dict(cls=getattr(settings, "INITIAL_DB"))
    user_dd.create_tables(cls=getattr(settings, "INITIAL_DB"))


def populate_dbs(username="admin", password=None, domain="Default", test_only=False):
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
        if not test_only:
            user_dd.add_element_from_keystone(user)
    for role in c.roles.list():
        # logger.info("Role {}".format(role.name))
        user_dd.add_element_from_keystone(role=role)
        for user in c.users.list():
            # logger.info("\tUser {}".format(user.name))
            for tenant in c.projects.list(user=user):
                if not test_only:
                    user_dd.add_element_from_keystone(user=user, role=role, tenant=tenant)
                    # print("\033[31m")
                    # print(tenant)
                    # print("\033[m")
                logger.info("Add cnx between {}/{} and tenant {}".format(user.name, role.name, tenant.name))
                # tenant_dd.add_element_from_keystone(tenant=tenant)
    for tenant in c.projects.list(user=None):
        logger.info("add tenant {}".format(tenant.name))
        if not test_only:
            tenant_dd.add_element_from_keystone(tenant=tenant)
    # object_created = []
    # action_created = []
    for action in API["actions"]: #getattr(settings, 'ACTIONS', ""):
        # if len(action["action"]) > 0 and action["action"] not in action_created:
        user_dd.create_element(table="Action", values={
            "name": action,
            "description": action,
            "enabled": True
        })
            # action_created.append(action["action"])
    for obj in API["objects"]:
        # if len(action["object"]) > 0 and action["object"] not in object_created:
        if type(obj) in (list, tuple):
            obj = obj[0]
        user_dd.create_element(table="Object", values={
            "name": obj,
            "description": obj,
            "enabled": True
        })
            # object_created.append(action["object"])


def delete_tables():
    user_dd.delete_tables()