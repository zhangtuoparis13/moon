"""
Policy information Point
Information gathering from the infrastructure
"""
from moon.tools.openstack_credentials import get_keystone_creds, get_nova_creds
import logging
from uuid import uuid4
from keystoneclient.openstack.common.apiclient.exceptions import Unauthorized, Forbidden
from moon import settings

logger = logging.getLogger("moon.pip")


class PIP:

    def __init__(self, standalone=False, kclient=None, **kwargs):
        self.kclient = kclient
        self.nclient = None
        self.kwargs = kwargs
        self.Unauthorized = Unauthorized
        self.Forbidden = Forbidden
        if not standalone and not kclient:
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

    def unset_creds(self):
        self.kclient = None
        self.nclient = None

    def set_creds_from_token(self, token):
        """Get an authentication client from a token got from Moon Server

        :param token:
        :return:
        """
        from keystoneclient.v3 import client as keystone_client
        auth_url = getattr(settings, "OPENSTACK_KEYSTONE_URL")
        self.kclient = keystone_client.Client(token=token.id, auth_url=auth_url)
        from novaclient import client as nova_client
        self.nclient = nova_client.Client("3", auth_token=token.id, auth_url=auth_url)

    def get_subjects(self, tenant=None):
        if type(tenant) is dict:
            tenant = tenant["uuid"]
        for user in self.kclient.users.list(project_id=tenant):
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
            o["uuid"] = server.id.replace("-", "")
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

    def get_roles(self, tenant=None, uuid=None, name=None):
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
            if name and o["name"] != name:
                continue
            if uuid and o["uuid"] != uuid:
                continue
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
            assignment["category"] = "role"
            assignment["subject"] = user["uuid"]
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
            assignments["category"] = "group"
            assignments["object"] = user["uuid"]
            assignments["description"] = "Group assignment for {}".format(user["name"])
            assignments["attributes"] = []
            groups = map(lambda x: x.id, self.kclient.groups.list(user=user["uuid"], project=tenant_uuid))
            if len(groups) > 0:
                assignments["attributes"].extend(groups)
            yield assignments

    def get_tenants(self, name, uuid=None, pap=None):
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
            if pap and pap.get_intra_extensions(tenant_uuid=t["uuid"]):
                t["managed"] = True
            else:
                t["managed"] = False
            if name and name != t["name"]:
                continue
            if uuid and uuid != t["uuid"]:
                continue
            yield t

    def create_roles(self, name, description=""):
        return self.kclient.roles.create(name=name, description=description)

    def delete_roles(self, uuid):
        return self.kclient.roles.delete(uuid)


pip = None


def get_pip(standalone=False, **kwargs):
    global pip
    if not pip:
        pip = PIP(standalone, **kwargs)
    return pip
