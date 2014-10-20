"""
Policy information Point
Information gathering from the infrastructure
"""
from moon.tools.openstack_credentials import get_keystone_creds, get_nova_creds
import logging
from uuid import uuid4
from keystoneclient.openstack.common.apiclient.exceptions import Unauthorized, Forbidden, Conflict, NotFound

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

    def set_creds_for_tenant(self, tenant_name="admin", tenant_uuid=None):
        tenant = self.get_tenants(name=tenant_name, uuid=tenant_uuid).next()
        from keystoneclient.v3 import client as keystone_client
        kcreds = get_keystone_creds()
        #WORKAROUND: if in version 2.0, Keystone connection doesn't work
        kcreds["auth_url"] = kcreds["auth_url"].replace("2.0", "3")
        kcreds["tenant_name"] = tenant["name"]
        self.kclient = keystone_client.Client(**kcreds)
        from novaclient import client as nova_client
        ncreds = get_nova_creds()
        ncreds["project_id"] = tenant["name"]
        self.nclient = nova_client.Client("1.1", **ncreds)

    def unset_creds(self):
        self.kclient = None
        self.nclient = None

    def set_creds_from_token(self, token):
        """Get an authentication client from a token got from Moon Server

        :param token:
        :return:
        """
        #FIXME The connection must be done with the token given by the user
        #FIXME Actually, the connection comes from user/pass in moon.settings
        #FIXME This is a vulnerability
        # from keystoneclient.v3 import client as keystone_client
        # auth_url = getattr(settings, "OPENSTACK_KEYSTONE_URL")
        # self.kclient = keystone_client.Client(token=token.id, auth_url=auth_url)
        # from novaclient import client as nova_client
        # self.nclient = nova_client.Client("3", auth_token=token.id, auth_url=auth_url)
        self.set_creds_for_tenant()

    def get_subjects(self, tenant=None, user_uuid=None):
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
                s["project"] = ""
            s["enabled"] = user.enabled
            try:
                s["domain"] = user.domain_id
            except AttributeError:
                pass
            s["uuid"] = user.id
            if user_uuid and user_uuid == user.id:
                yield s
            elif not user_uuid:
                yield s

    def add_subject(self, user):
        for key in ('domain', 'enabled', 'name', 'project', 'password', 'description'):
            if key not in user.keys():
                if key in ('name', 'project', 'password'):
                    return None
                else:
                    user[key] = ""
        tenants = self.kclient.projects.list()
        try:
            my_tenant = [x for x in tenants if x.name == user["project"]][0]
        except IndexError:
            my_tenant = [x for x in tenants if x.id == user["project"]][0]
        my_user = self.kclient.users.create(
            name=user["name"],
            password=user["password"],
            tenant_id=my_tenant.id,
            description=user["description"],
            enabled=user["enabled"],
            domain=user["domain"])
        return my_user.id

    def del_subject(self, user_uuid):
        self.kclient.users.delete(user_uuid)

    def get_objects(self, tenant=None, object_uuid=None):
        s = dict()
        #TODO: need to send the token in parameter of all functions in PIP
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
            if object_uuid and object_uuid == o["uuid"]:
                yield o
            elif not object_uuid:
                yield o

    def add_object(self, name, image_name="Cirros3.2", flavor_name="m1.nano"):
        import time
        image = self.nclient.images.find(name=image_name)
        flavor = self.nclient.flavors.find(name=flavor_name)
        instance = self.nclient.servers.create(name=name, image=image, flavor=flavor)
        status = instance.status
        max_cpt = 0
        while status == "BUILD":
            time.sleep(5)
            instance = self.nclient.servers.get(instance.id)
            status = instance.status
            max_cpt += 1
            if max_cpt > 12:
                return
        return instance.id

    def del_object(self, uuid):
        instance = self.nclient.servers.find(id=uuid)
        instance.delete()
        cpt = 0
        import time
        while True:
            try:
                self.nclient.servers.find(id=uuid)
                time.sleep(1)
                cpt += 1
                if cpt > 10:
                    return
            except:
                return

    def get_roles(self, tenant_name="admin", project_uuid=None, user_uuid=None):
        try:
            if project_uuid:
                tenant = self.get_tenants(uuid=project_uuid).next()
            else:
                tenant = self.get_tenants(name=tenant_name).next()
        except StopIteration:
            pass
        else:
            for role in self.kclient.roles.list(project=tenant["uuid"], user=user_uuid):
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
                # if name and o["name"] != name:
                #     continue
                # if uuid and o["uuid"] != uuid:
                #     continue
                yield o

    def add_role(self, name, description=""):
        try:
            role = self.kclient.roles.create(name=name, description=description)
        except Conflict:
            role = filter(lambda x: x.name == name, self.kclient.roles.list())[0]
        return role.id

    def del_role(self, uuid):
        return self.kclient.roles.delete(uuid)

    def get_groups(self, tenant_name="admin", project_uuid=None, user_uuid=None):
        try:
            if project_uuid:
                tenant = self.get_tenants(uuid=project_uuid).next()
            else:
                tenant = self.get_tenants(name=tenant_name).next()
        except StopIteration:
            pass
        else:
            for group in self.kclient.groups.list(project_id=tenant["uuid"], user=user_uuid):
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
                # if name and g["name"] != name:
                #     continue
                # if uuid and g["uuid"] != uuid:
                #     continue
                yield g

    def add_group(self, name, description=""):
        return self.kclient.groups.create(name=name, description=description)

    def del_group(self, uuid):
        return self.kclient.groups.delete(uuid)

    def get_users_roles_assignment(self, tenant_name="admin", project_uuid=None, users=None, user_uuid=None):
        try:
            if project_uuid:
                tenant = self.get_tenants(uuid=project_uuid).next()
            else:
                tenant = self.get_tenants(name=tenant_name).next()
        except StopIteration:
            pass
        else:
            if not users:
                users = self.get_subjects(tenant["uuid"])
            for user in users:
                assignment = {}
                _uuid = str(uuid4()).replace("-", "")
                assignment["uuid"] = _uuid
                if user_uuid and user_uuid != user["uuid"]:
                    continue
                assignment["category"] = "role"
                assignment["subject"] = user["uuid"]
                assignment["description"] = "Role assignment for {}".format(user["name"])
                assignment["attributes"] = []
                roles = map(lambda x: x.id, self.kclient.roles.list(user=user["uuid"], project=tenant["uuid"]))
                if len(roles) > 0:
                    assignment["attributes"].extend(roles)
                yield assignment

    def add_users_roles_assignment(self, tenant_name="admin", project_uuid=None, user_uuid=None, role_uuid=None):
        #TODO
        try:
            if project_uuid:
                tenant = self.get_tenants(uuid=project_uuid).next()
            else:
                tenant = self.get_tenants(name=tenant_name).next()
        except StopIteration:
            pass
        else:
            # user = self.get_subjects(tenant=tenant["uuid"], user_uuid=user_uuid)
            # role = filter(
            #     lambda x: x["uuid"] == role_uuid,
            #     self.get_roles(project_uuid=tenant["uuid"], user_uuid=user_uuid)
            # )
            # self.kclient.roles.add(user=user["uuid"], project=tenant["uuid"], role=role["uuid"])
            self.kclient.roles.grant(role_uuid, user=user_uuid, project=tenant["uuid"])

    def del_users_roles_assignment(self, tenant_name="admin", project_uuid=None, user_uuid=None, role_uuid=None):
        #TODO: don't work, need additional authorization ?
        try:
            if project_uuid:
                tenant = self.get_tenants(uuid=project_uuid).next()
            else:
                tenant = self.get_tenants(name=tenant_name).next()
        except StopIteration:
            pass
        else:
            # user = self.get_subjects(tenant=tenant["uuid"], user_uuid=user_uuid)
            # role = self.get_roles(project_uuid=tenant["uuid"], user_uuid=user_uuid)
            self.kclient.roles.revoke(role_uuid, user=user_uuid, project=tenant["uuid"])

    def get_users_groups_assignment(self, tenant_name="admin", project_uuid=None, users=None, user_uuid=None):
        try:
            if project_uuid:
                tenant = self.get_tenants(uuid=project_uuid).next()
            else:
                tenant = self.get_tenants(name=tenant_name).next()
        except StopIteration:
            pass
        else:
            if not users:
                users = self.get_subjects(tenant["uuid"])
            for user in users:
                assignments = {}
                _uuid = str(uuid4()).replace("-", "")
                assignments["uuid"] = _uuid
                if user_uuid and user_uuid != user["uuid"]:
                    continue
                assignments["category"] = "group"
                assignments["subject"] = user["uuid"]
                assignments["description"] = "Group assignment for {}".format(user["name"])
                assignments["attributes"] = []
                groups = map(lambda x: x.id, self.kclient.groups.list(user=user["uuid"], project=tenant["uuid"]))
                if len(groups) > 0:
                    assignments["attributes"].extend(groups)
                yield assignments

    def get_tenants(self, name=None, uuid=None, pap=None):
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

    def add_tenant(self, tenant):
        """Add a new tenant

        :param tenant: dictionary describing the tenant
        :return: the id of the new tenant

        The dictionary must be:
        {
            "name": "...",
            "description": "...",
            "enabled": True,
            "domain": "Default"
        }
        """
        for key in ("name", "description", "enabled", "domain"):
            if key not in tenant.keys():
                return None
        tenant = self.kclient.projects.create(
            name=tenant["name"],
            domain=tenant["domain"],
            description=tenant["description"],
            enabled=tenant["enabled"]
        )
        return tenant.id

    def del_tenant(self, tenant_uuid):
        self.kclient.projects.delete(tenant_uuid)

    def get_images(self):
        images = list()
        for _img in self.nclient.images.list():
            i = dict()
            i["uuid"] = _img.id
            i["name"] = _img.name
            # print(_img.to_dict())
            images.append(i)
        return images

    def get_flavors(self):
        flavors = list()
        for _flavour in self.nclient.flavors.list():
            f = dict()
            f["uuid"] = _flavour.id
            f["name"] = _flavour.name
            # print(_flavour.to_dict())
            flavors.append(f)
        return flavors

pip = None


def get_pip(standalone=False, **kwargs):
    global pip
    if not pip:
        pip = PIP(standalone, **kwargs)
    return pip
