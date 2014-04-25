# from sqlalchemy import create_engine
# from sqlalchemy import Column, Integer, String
# from sqlalchemy import Boolean
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from gi import settings
import logging

logger = logging.getLogger('moon.info_repository')


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
    domain = "Default"
    project = ""

    def __repr__(self):
        return "User: {domain}/{user} ({uuid}) {email} {description} {enabled}".format(
            user=self.name,
            uuid=self.uuid,
            email=self.email,
            description=self.description,
            enabled=self.enabled,
            domain=self.domain
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

