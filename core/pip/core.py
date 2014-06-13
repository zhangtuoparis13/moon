"""
Policy information Point
Information gathering from the infrastructure
"""
# from moon.info_repository import driver_dispatcher as dd
from moon import settings
from moon.intra_extension_manager import get_dispatcher as get_intra_dd
from moon.inter_extension_manager import get_dispatcher as get_inter_dd
from tools.openstack_credentials import get_keystone_creds, get_nova_creds
import logging
import uuid
import json
from keystoneclient.openstack.common.apiclient.exceptions import Unauthorized, Forbidden

logger = logging.getLogger("moon.pip")


class PIP:

    def __init__(self):
        self.kclient = None
        self.nclient = None
        from keystoneclient.v3 import client as keystone_client
        kcreds = get_keystone_creds()
        #WORKAROUND: if in version 2.0, Keystone connection doesn't work
        kcreds["auth_url"] = kcreds["auth_url"].replace("2.0", "3")
        self.kclient = keystone_client.Client(**kcreds)
        from novaclient import client as nova_client
        ncreds = get_nova_creds()
        self.nclient = nova_client.Client("1.1", **ncreds)

    def set_creds_for_tenant(self, tenant_name="admin"):
        from keystoneclient.v3 import client as keystone_client
        kcreds = get_keystone_creds()
        #WORKAROUND: if in version 2.0, Keystone connection doesn't work
        kcreds["auth_url"] = kcreds["auth_url"].replace("2.0", "3")
        kcreds["tenant_name"] = tenant_name
        self.kclient = keystone_client.Client(**kcreds)
        from novaclient import client as nova_client
        ncreds = get_nova_creds()
        ncreds["project_id"] = tenant_name
        self.nclient = nova_client.Client("1.1", **ncreds)

    def get_subjects(self, tenant=None):
        # logger.info("Getting subjects")
        for user in self.kclient.users.list(project_id=tenant["uuid"]):
            s = dict()
            s["name"] = user.name
            try:
                s["mail"] = user.email
            except AttributeError:
                pass
            try:
                s["description"] = user.description
            except AttributeError:
                pass
            try:
                s["project"] = user.default_project_id
            except AttributeError:
                pass
            s["enabled"] = user.enabled
            try:
                s["domain"] = user.domain_id
            except AttributeError:
                pass
            s["uuid"] = user.id
            yield s

    def get_objects(self, tenant=None):
        # logger.info("Getting objects")
        s = dict()
        for server in self.nclient.servers.list():
            o = dict()
            o["name"] = server.name
            o["uuid"] = server.id
            try:
                o["description"] = server.description
            except AttributeError:
                o["description"] = ""
            try:
                o["enabled"] = server.enabled
            except AttributeError:
                o["enabled"] = True
            o["category"] = "object"
            yield o

    def get_roles(self, tenant=None):
        # logger.info("Getting roles")
        for role in self.kclient.roles.list(project_id=tenant["uuid"]):
            o = dict()
            o["value"] = role.name
            try:
                o["description"] = role.description
            except AttributeError:
                o["description"] = ""
            try:
                o["enabled"] = role.enabled
            except AttributeError:
                o["enabled"] = True
            o["category"] = "role"
            o["uuid"] = role.id
            yield o

    def get_groups(self, tenant=None):
        # logger.info("Getting groups")
        for group in self.kclient.groups.list(project_id=tenant["uuid"]):
            g = dict()
            g["value"] = group.name
            try:
                g["description"] = group.description
            except AttributeError:
                g["description"] = ""
            try:
                g["enabled"] = group.enabled
            except AttributeError:
                g["enabled"] = True
            g["category"] = "group"
            g["uuid"] = group.id
            yield g

    def get_users_roles_assignment(self, tenant_uuid, users=None):
        if not users:
            users = self.get_subjects(tenant_uuid)
        for user in users:
            assignment = {}
            _uuid = str(uuid.uuid4())
            assignment[_uuid] = {}
            assignment[_uuid]["object"] = user["uuid"]
            assignment[_uuid]["description"] = "Role assignment for {}".format(user["name"])
            assignment[_uuid]["attributes"] = []
            # for tenant in client.projects.list():
            roles = map(lambda x: x.id, self.kclient.roles.list(user=user["uuid"], project=tenant_uuid))
            if len(roles) > 0:
                assignment[_uuid]["attributes"].extend(roles)
            # print(assignment)
            yield assignment

    def get_users_groups_assignment(self, tenant_uuid, users=None):
        if not users:
            users = self.get_subjects(tenant_uuid)
        for user in users:
            assignments = {}
            _uuid = str(uuid.uuid4())
            assignments[_uuid] = {}
            assignments[_uuid]["object"] = user["uuid"]
            assignments[_uuid]["description"] = "Group assignment for {}".format(user["name"])
            assignments[_uuid]["attributes"] = []
            # for tenant in client.projects.list():
            groups = map(lambda x: x.id, self.kclient.groups.list(user=user["uuid"], project=tenant_uuid))
            if len(groups) > 0:
                assignments[_uuid]["attributes"].extend(groups)
            yield assignments

    def get_tenants(self):
        # logger.info("Getting tenants")
        for tenant in self.kclient.projects.list():
            t = dict()
            t["name"] = tenant.name
            try:
                t["description"] = tenant.description
            except AttributeError:
                t["description"] = ""
            try:
                t["enabled"] = tenant.enabled
            except AttributeError:
                t["enabled"] = True
            t["domain"] = tenant.domain_id
            t["uuid"] = tenant.id
            yield t

    def get_keystone_client(self, username=None, password=None, domain="Default"):
        # from keystoneclient.v3 import client
        # if not username and not password:
        #     creds = get_keystone_creds()
        #     self.kclient = client.Client(**creds)
        #     return self.kclient
        # if not password:
        #     import getpass
        #     password = getpass.getpass("Keystone password for {user} on [{url}]:".format(
        #         user=username,
        #         url=getattr(settings, 'OPENSTACK_KEYSTONE_URL', "")
        #     ))
        # self.kclient = self.kclient.Client(
        #     username=username,
        #     password=password,
        #     user_domain_name=domain,
        #     region_name="regionOne",
        #     #endpoint=getattr(settings, 'OPENSTACK_KEYSTONE_URL', ""),
        #     # insecure=True,
        #     # cacert=None,
        #     auth_url=getattr(settings, 'OPENSTACK_KEYSTONE_URL', ""),
        #     # debug=settings.DEBUG
        # )
        # self.kclient.management_url = getattr(settings, 'OPENSTACK_KEYSTONE_URL', "")
        # return self.kclient
        return None

    # def get_nova_client(self, username=None, password=None):
    #     from novaclient import client
    #     if not username and not password:
    #         creds = get_nova_creds()
    #         self.nclient = client.Client(**creds)
    #         return self.nclient
        # if not password:
        #     import getpass
        #     password = getpass.getpass("Nova password for {user} on [{url}]:".format(
        #         user=username,
        #         url=getattr(settings, 'OPENSTACK_KEYSTONE_URL', "")
        #     ))
        # self.kclient = client.Client(
        #     username=username,
        #     password=password,
        #     user_domain_name=domain,
        #     region_name="regionOne",
        #     #endpoint=getattr(settings, 'OPENSTACK_KEYSTONE_URL', ""),
        #     # insecure=True,
        #     # cacert=None,
        #     auth_url=getattr(settings, 'OPENSTACK_KEYSTONE_URL', ""),
        #     # debug=settings.DEBUG
        # )
        # self.kclient.management_url = getattr(settings, 'OPENSTACK_KEYSTONE_URL', "")
        # return self.kclient

    def new_intra_extension(self, tenant, test_only=False, json_data=None):
        if not json_data:
            filename = getattr(settings, "DEFAULT_EXTENSION_TABLE")
            json_data = json.loads(file(filename).read())
        # for tenant in client.projects.list():
        json_data["uuid"] = uuid.uuid4()
        json_data["tenant"] = {"uuid": tenant["uuid"], "name": tenant["name"]}
        json_data["perimeter"]["subjects"] = list(self.get_subjects(tenant=tenant))
        json_data["perimeter"]["objects"] = list(self.get_objects(tenant=tenant))
        attributes = list(json_data["configuration"]["metadata"]["subject"])
        s_attr = []
        s_attr_assign = []
        if "roles" in attributes:
            roles = list(self.get_roles(tenant=tenant))
            s_attr.extend(roles)
            s_attr_assign.extend(list(self.get_users_roles_assignment(
                tenant_uuid=tenant["uuid"],
                users=json_data["perimeter"]["subjects"])))
            attributes.remove("roles")
        if "groups" in attributes:
            groups = list(self.get_groups(tenant=tenant))
            s_attr.extend(groups)
            s_attr_assign.extend(list(self.get_users_groups_assignment(
                tenant_uuid=tenant["uuid"],
                users=json_data["perimeter"]["subjects"])))
            attributes.remove("groups")
        json_data["profiles"]["s_attr"] = s_attr
        json_data["profiles"]["s_attr_assign"] = s_attr_assign
        if "rules" not in json_data["configuration"].keys():
            json_data["configuration"]["rules"] = []
        if len(attributes) > 0:
            logger.warning("All attributes have not been parsed in configuration.metadata.subject {}".format(attributes))
        if not test_only:
            get_intra_dd().new_from_json(json_data=json_data)

    def sync_db_with_keystone(self):
        # #synchronize all intra extensions
        # logger.error("Call sync_db_with_keystone")
        for tenant in self.get_tenants():
            #TODO: if new tenant
            #       -> need to add a new intra extension
            #       -> need to add a new inter extension with a new vent
            #TODO: if not new tenant -> need to synchronize users, roles, ...
            # extension = get_intra_dd().sync_extension(
            #     tenant_uuid=tenant["uuid"],
            #     users=self.get_subjects(client),
            #     roles=self.get_roles(client),
            #     groups=self.get_groups(client))
            logger.info("Working with tenant {}".format(tenant["name"]))
            try:
                self.set_creds_for_tenant(tenant["name"])
            except Unauthorized:
                logger.warning("Cannot authenticate in tenant {}".format(tenant["name"]))
                continue
            get_inter_dd().add_tenant(
                name=tenant["name"],
                description=tenant["description"],
                enabled=tenant["enabled"],
                domain=tenant["domain"],
                uuid=tenant["uuid"]
            )
            try:
                self.new_intra_extension(tenant=tenant)
            except Forbidden:
                logger.warning("Cannot list users in tenant {}".format(tenant["name"]))
                continue
        # #synchronize all inter extensions
        # for subject in self.get_subjects(client):
        #     get_intra_dd().add_user(subject)
        # for role in self.get_roles(client):
        #     get_intra_dd().add_role(role)

    @staticmethod
    def delete_tables():
        get_intra_dd().delete_tables()
        get_inter_dd().delete_tables()


pip = PIP()


def get_pip():
    return pip

# def update_request_attributes(
#         subject=None,
#         action=None,
#         object_name=None,
#         tenant=None,
#         attributes=None):
#     """
#     Get a list of attribute values for user user_uuid in tenant tenant_uuid
#     Return a list of attribute values for attribute_name
#     Example for 'role': ( "admin", "user" )
#
#     """
#     attributes = dd.update_request_attributes(subject, action, object_name, tenant, attributes)
#     return attributes