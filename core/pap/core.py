"""
"""
import logging
from moon.user_repository.driver_dispatcher import Users, get_user, get_role
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

    def get_user(self, name=None, uuid=None):
        return get_user(name, uuid)

    def get_role(self, name=None, uuid=None, project_uuid=None):
        return get_role(name, uuid, project_uuid)

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
