# from sqlalchemy import create_engine
# from sqlalchemy import Column, Integer, String
# from sqlalchemy import Boolean
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from gi import settings
import logging

logger = logging.getLogger('moon.user_repository')


class User:
    """
    Model for a User
    """
    __tablename__ = 'user'
    uuid = ""
    name = ""
    password = ""
    email = ""
    description = ""
    enabled = ""

    def __repr__(self):
        return "User: {user} ({uuid}) {email} {description} {enabled}".format(
            user=self.name,
            uuid=self.uuid,
            email=self.email,
            description=self.description,
            enabled=self.enabled
        )


class Role:
    """
    Database Model for a Role
    """
    __tablename__ = 'role'
    uuid = ""
    name = ""
    tenant_uuid = ""
    description = ""
    enabled = ""

    def __repr__(self):
        return "Role: {role} ({uuid}) {tenant_uuid} {description} {enabled}".format(
            role=self.name,
            uuid=self.uuid,
            tenant_uuid=self.tenant_uuid,
            description=self.description,
            enabled=self.enabled
        )


class UserRoleAssignment:
    """
    Database Model for relations between User and Role
    """
    __tablename__ = 'user_role_assignment'
    uuid = ""
    user_uuid = ""
    role_uuid = ""

    def __repr__(self):
        return "{user_uuid} -> {role_uuid}".format(
            user_uuid=self.user_uuid,
            role_uuid=self.role_uuid,
        )


# class Tenant(base_tenant_db):
#     """
#     Database Model for a Tenant / Project
#     """
#     __tablename__ = 'tenant'
#     uuid = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     description = Column(String(250))
#     enabled = Column(Boolean)
#
#     def __repr__(self):
#         return "Tenant: {name} ({uuid}) {description} {enabled}".format(
#             name=self.name,
#             uuid=self.uuid,
#             description=self.description,
#             enabled=self.enabled
#         )
#
#
# class TenantTree(base_tenant_db):
#     """
#     Database Model for the relations between every Tenant
#     """
#     __tablename__ = 'tenant_tree'
#     uuid = Column(Integer, primary_key=True)
#     parent_tenant_uuid = Column(String(32))
#     child_tenant_uuid = Column(String(32))
#     type = Column(String(32))
#
#     def __repr__(self):
#         return "TenantRelation: {parent_tenant_uuid} -> {child_tenant_uuid} (type: {type})".format(
#             parent_tenant_uuid=self.parent_tenant_uuid,
#             child_tenant_uuid=self.child_tenant_uuid,
#             type=self.type
#         )


# def create_tables():
#     """
#     Create all tables in database.
#     """
#     logger.debug("Creating DB tables")
#     base_user_db.metadata.create_all(engine_user_db)
#     base_tenant_db.metadata.create_all(engine_tenant_db)


# def get_user_session():
#     """
#     Return the session associated with the User DB
#     """
#     return UserSession()
#

# def get_tenant_session():
#     """
#     Return the session associated with the Tenant DB
#     """
#     return TenantSession()

#
# def __add_user_to_userdb(user):
#     """
#     Add a user in User DB from a Keystone User
#     """
#     s = get_user_session()
#     logger.debug("Adding user {user} to User DB".format(user=user.name))
#     u = User(
#         name=user.name,
#         password=user.password,
#         uuid=user.uuid,
#         email=user.email,
#         description=user.description,
#         enabled=user.enabled
#     )
#     s.add(u)
#
#
# def __add_role_to_userdb(role):
#     """
#     Add a role in User DB from a Keystone Role
#     """
#     s = get_user_session()
#     logger.debug("Adding role {role} to User DB".format(role=role.name))
#     r = User(
#         name=role.name,
#         uuid=role.uuid,
#         description=role.description,
#         enabled=role.enabled
#     )
#     s.add(r)
#
#
# def __add_userroleassignment_to_userdb(user, role):
#     """
#     Add a user role assignment in User DB from Keystone information
#     """
#     s = get_user_session()
#     logger.debug("Adding role {role} to user {user} to User DB".format(role=role.name, user=user.name))
#     r = UserRoleAssignment(
#         role_uuid=role.uuid,
#         user_uuid=user.uuid
#     )
#     s.add(r)


# def populate_dbs(username="admin", password=None, domain="Default"):
#     """
#     Populated for the first time the User DB with the content of the Keystone DB.
#     """
#     logger.info("Populate Database with information from Keystone server")
#     if not password:
#         import getpass
#         password = getpass.getpass("Keystone password for {user} on [{url}]:".format(
#             user=username,
#             url=getattr(settings, 'OPENSTACK_KEYSTONE_URL', "")
#         ))
#     from keystoneclient.v3 import client
#     logger.debug(getattr(settings, 'OPENSTACK_KEYSTONE_URL', ""))
#     c = client.Client(
#         username=username,
#         password=password,
#         user_domain_name=domain,
#         region_name="regionOne",
#         #endpoint=getattr(settings, 'OPENSTACK_KEYSTONE_URL', ""),
#         # insecure=True,
#         # cacert=None,
#         auth_url=getattr(settings, 'OPENSTACK_KEYSTONE_URL', ""),
#         # debug=settings.DEBUG
#     )
#     logger.debug(c.services.list())
#     logger.debug(dir(c))
#     for u in c.users.list():
#         __add_user_to_userdb(u)
#
#
# def sync_user_db():
#     """
#     Synchronise when needed from the remote Keystone DB to the local User DB.
#     """
#     # TODO: define arguments and add synchronisation.
#     pass