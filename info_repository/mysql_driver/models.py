from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy import Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from moon import settings
from moon.info_repository import models
import logging

logger = logging.getLogger('moon.mysql_driver')

DataBases = getattr(settings, "DATABASES")
if len(DataBases['user_db']['HOST']) == 0:
    DataBases['user_db']['HOST'] = "127.0.0.1"
if len(DataBases['user_db']['PORT']) == 0:
    DataBases['user_db']['PORT'] = "3306"

drivername = DataBases['user_db']['ENGINE']
engine_url = 'mysql://{user}:{password}@{host}:{port}/{table}'.format(
    user=DataBases['user_db']['USER'],
    password=DataBases['user_db']['PASSWORD'],
    host=DataBases['user_db']['HOST'],
    port=DataBases['user_db']['PORT'],
    table=DataBases['user_db']['NAME']
)
# TODO: set config from somewhere else
engine_user_db = create_engine(
    engine_url,
    echo=False
)
# engine_tenant_db = create_engine(
#     'mysql+mysqldb://moonuser:P4ssw0rd@localhost:3306/tenant_db?charset=utf8&use_unicode=0',
#     echo=False
# )
base_user_db = declarative_base()
# base_tenant_db = declarative_base()

UserSession = sessionmaker()
UserSession.configure(bind=engine_user_db)
# TenantSession = sessionmaker(bind=base_tenant_db)
# myUserSession = UserSession()


def get_user_session():
    """
    Return a session associated with the User DB
    """
    return UserSession()


def create_tables():
    """
    Create all tables in database.
    """
    logger.info("Creating DB tables")
    base_user_db.metadata.create_all(engine_user_db)
    # base_tenant_db.metadata.create_all(engine_tenant_db)


class User(models.User, base_user_db):
    """
    Database Model for a User
    """
    __tablename__ = 'user'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    uuid = Column(String(32))
    password = Column(String(50))
    email = Column(String(100))
    description = Column(String(250))
    enabled = Column(Boolean)

    def __repr__(self):
        return "User: {user} ({uuid}) {email} {description} {enabled}".format(
            user=self.name,
            uuid=self.uuid,
            email=self.email,
            description=self.description,
            enabled=self.enabled
        )


class Role(models.Role, base_user_db):
    """
    Database Model for a Role
    """
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    uuid = Column(String(32))
    tenant_uuid = Column(String(32))
    description = Column(String(250))
    enabled = Column(Boolean)

    def __repr__(self):
        return "Role: {role} ({uuid}) {tenant_uuid} {description} {enabled}".format(
            role=self.name,
            uuid=self.uuid,
            tenant_uuid=self.tenant_uuid,
            description=self.description,
            enabled=self.enabled
        )


class UserRoleAssignment(models.UserRoleAssignment, base_user_db):
    """
    Database Model for relations between User and Role
    """
    __tablename__ = 'user_role_assignment'
    id = Column(Integer, primary_key=True)
    user_uuid = Column(String(32))
    role_uuid = Column(String(32))

    def __repr__(self):
        return "{user_uuid}, {role_uuid}".format(
            user_uuid=self.user_uuid,
            role_uuid=self.role_uuid,
        )


def add_user_to_userdb(user):
    """
    Add a user in User DB from a Keystone User
    """
    s = get_user_session()
    try:
        email = user.email
    except TypeError:
        email = ""
    except AttributeError:
        email = ""
    u = User(
        name=user.name,
        password="<Unknown>",
        uuid=user.id,
        email=email,
        enabled=user.enabled
    )
    q = s.query(User).filter_by(uuid=user.id)
    if q.count() > 0:
        record = q.first()
        logger.debug("Updating {}".format(user.name))
        record.name = user.name
        record.email = email
        record.enabled = user.enabled
    else:
        logger.debug("Adding {}".format(user.name))
        s.add(u)
    s.commit()


def add_role_to_userdb(role, project):
    """
    Add a role in User DB from a Keystone Role
    """
    s = get_user_session()
    r = Role(
        name=role.name,
        uuid=role.id,
        tenant_uuid=project.id,
        # description=role.description,
        # enabled=role.enabled
    )
    q = s.query(Role).filter_by(uuid=role.id, tenant_uuid=project.id)
    if q.count() > 0:
        record = q.first()
        # logger.info("Updating {}/{}".format(role.name, project.id))
        record.name = role.name
    else:
        # logger.info("Adding {}/{}".format(role.name, project.id))
        s.add(r)
    s.commit()


def add_userroleassignment_to_userdb(user, role):
    """
    Add a user role assignment in User DB from Keystone information
    """
    s = get_user_session()
    # logger.info("Adding role {role} to user {user} to User DB".format(
    #     role=role.name,
    #     user=user.name,
    # ))
    r = UserRoleAssignment(
        role_uuid=role.id,
        user_uuid=user.id,
    )
    q = s.query(UserRoleAssignment).filter_by(
        role_uuid=role.id,
        user_uuid=user.id,
    )
    if q.count() == 0:
        # logger.info("Count = 0")
        s.add(r)
        s.commit()


def get_user(uuid=None, name=None):
    """
    Get a user with his name or UUID
    """
    s = get_user_session()
    q = None
    if uuid:
        q = s.query(User).filter_by(uuid=uuid)
    else:
        q = s.query(User).filter_by(name=name)
    record = q.first()
    # TODO: we have to deals with multiple results
    return record


def get_role(uuid=None, name=None, project_uuid=None):
    """
    Get a role with his name or UUID on a specific project
    """
    s = get_user_session()
    q = None
    if uuid:
        q = s.query(Role).filter_by(uuid=uuid, project_uuid=project_uuid)
    else:
        q = s.query(Role).filter_by(name=name, project_uuid=project_uuid)
    record = q.first()
    # TODO: we have to deals with multiple results
    return record

