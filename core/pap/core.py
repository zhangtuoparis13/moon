"""
"""
import logging
from moon.info_repository.driver_dispatcher import Users, get_user, get_role
from moon.tenant_repository.driver_dispatcher import Tenants
# from moon.tenant_repository.driver_dispatcher import \
#     set_tenant_relationship, \
#     unset_tenant_relationship, \
#     get_tenant, \
#     get_tenants, \
#     Tenants

logger = logging.getLogger("moon.pap")


class PAP:
    """
    Policy Administration Point
    """

    def __init__(self, kclient=None):
        if not kclient:
            self.kclient = None
            # TODO: need authentication
        else:
            self.kclient = kclient
        self.users = Users(self.kclient)
        self.tenants = Tenants(self.kclient)

    # def get_user(self, name=None, uuid=None):
    #     return get_user(name=name, uuid=uuid)
    #
    # def get_role(self, name=None, uuid=None, project_uuid=None):
    #     return get_role(name, uuid, project_uuid)
    #
    # def set_tenant_relationship(self, tenant_up="", tenant_bottom=""):
    #     set_tenant_relationship(tenant_up=tenant_up, tenant_bottom=tenant_bottom)
    #
    # def unset_tenant_relationship(self, tenant_up="", tenant_bottom=""):
    #     unset_tenant_relationship(tenant_up=tenant_up, tenant_bottom=tenant_bottom)
    #
    # def get_project(self, uuid=None):
    #     return get_tenant(uuid=uuid)
    #
    # def get_projects(self):
    #     return get_tenants()

# class Users:
#
#     def __init__(self, kclient):
#         self.kclient = kclient
#
#     def create(self,
#                name="",
#                password="",
#                domain="",
#                project="",
#                email="",
#                description="",
#                enabled=True):
#         return self.kclient.create(name, password, domain, project, email, description, enabled)
#
#     def list(self, sort=True):
#         """
#         Return all users from the Keystone service.
#         """
#         if sort:
#             users = sorted(self.kclient.users.list(), key=lambda _user: _user.name)
#         else:
#             users = self.kclient.users.list()
#         return users
#
#     def get_user(self, identifier):
#         """
#         Return a specific user from the Keystone service.
#         """
#         user = ()
#         for _user in self.kclient.users.list():
#             if _user.id == identifier:
#                 user = _user
#         user.project = user.default_project_id
#         for _project in self.kclient.projects.list():
#             if user.default_project_id == _project.id:
#                 user.project = _project.name
#         user.domain = user.domain_id
#         return user
