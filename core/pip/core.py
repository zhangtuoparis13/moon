"""
Policy information Point
Information gathering from the infrastructure
"""
# from moon.info_repository import driver_dispatcher as dd
from moon import settings
# from moon.intra_extension_manager import get_dispatcher as get_intra_dd
# from moon.inter_extension_manager import get_dispatcher as get_inter_dd
from moon.core.pdp.inter_extension import get_inter_extentions
from moon.core.pdp.intra_extension import get_intra_extentions
from moon.tools.openstack_credentials import get_keystone_creds, get_nova_creds
import logging
from uuid import uuid4
import json
from keystoneclient.openstack.common.apiclient.exceptions import Unauthorized, Forbidden

logger = logging.getLogger("moon.pip")


class PIP:

    def __init__(self, standalone=False):
        self.kclient = None
        self.nclient = None
        if not standalone:
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
            o["tenant"] = tenant
            yield o

    def get_roles(self, tenant=None):
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
            _uuid = str(uuid4()).replace("-", "")
            assignment["uuid"] = _uuid
            assignment["object"] = user["uuid"]
            assignment["description"] = "Role assignment for {}".format(user["name"])
            assignment["attributes"] = []
            roles = map(lambda x: x.id, self.kclient.roles.list(user=user["uuid"], project=tenant_uuid))
            if len(roles) > 0:
                assignment["attributes"].extend(roles)
            yield assignment

    def get_users_groups_assignment(self, tenant_uuid, users=None):
        if not users:
            users = self.get_subjects(tenant_uuid)
        for user in users:
            assignments = {}
            _uuid = str(uuid4()).replace("-", "")
            assignments["uuid"] = _uuid
            assignments["object"] = user["uuid"]
            assignments["description"] = "Group assignment for {}".format(user["name"])
            assignments["attributes"] = []
            groups = map(lambda x: x.id, self.kclient.groups.list(user=user["uuid"], project=tenant_uuid))
            if len(groups) > 0:
                assignments["attributes"].extend(groups)
            yield assignments

    def get_tenants(self):
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

    def new_intra_extension(self, tenant, test_only=False, json_data=None):
        # TODO: delete o_attr "type" and add an attribute with value the UUID of VM
        existing_extension = get_intra_extentions().get(attributes={"tenant.uuid": tenant["uuid"]})
        if not json_data:
            filename = getattr(settings, "DEFAULT_EXTENSION_TABLE")
            #TODO: deals with errors in json file
            json_data = json.loads(file(filename).read())
        if existing_extension:
            json_data["uuid"] = existing_extension[0].uuid
        else:
            json_data["uuid"] = str(uuid4()).replace("-", "")
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
        #HYPOTHESIS: objects are only virtual servers, so linking all objects to type server
        o_attr_assign = json_data["profiles"]["o_attr_assign"]
        for obj in json_data["perimeter"]["objects"]:
            link = {}
            link["uuid"] = str(uuid4())
            link["object"] = obj["uuid"]
            #Add default actions
            link["attributes"] = ["type-vm", "action-get", "action-post", "action-delete", "action-post.os-start"]
            o_attr_assign.append(link)
        json_data["profiles"]["o_attr_assign"] = o_attr_assign
        if "rules" not in json_data["configuration"].keys():
            json_data["configuration"]["rules"] = []
        if len(attributes) > 0:
            logger.warning("All attributes have not been parsed in configuration.metadata.subject {}".format(attributes))
        if not test_only:
            get_intra_extentions().new_from_json(json_data=json_data)

    def sync_db_with_keystone(self):
        logs = ""
        # #synchronize all intra extensions
        self.set_creds_for_tenant()
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
            logs += "Syncing {}".format(tenant["name"])
            get_inter_extentions().add_tenant(
                name=tenant["name"],
                description=tenant["description"],
                enabled=tenant["enabled"],
                domain=tenant["domain"],
                uuid=tenant["uuid"]
            )
            try:
                self.new_intra_extension(tenant=tenant)
                logs += " OK\n"
            except Forbidden:
                logger.warning("Cannot list users in tenant {}".format(tenant["name"]))
                logs += " KO\n"
                continue
        # #synchronize all inter extensions
        # for subject in self.get_subjects(client):
        #     get_intra_dd().add_user(subject)
        # for role in self.get_roles(client):
        #     get_intra_dd().add_role(role)
        return logs

    @staticmethod
    def delete_tables():
        get_intra_extentions().delete_tables()
        get_inter_extentions().delete_tables()


pip = None


def get_pip(standalone=False):
    global pip
    if not pip:
        pip = PIP(standalone)
    return pip
