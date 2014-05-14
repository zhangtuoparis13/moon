from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Sequence #noqa
from sqlalchemy import Boolean #noqa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from moon import settings
from moon.info_repository import models #noqa
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

engine_user_db = create_engine(
    engine_url,
    echo=False
)

base_user_db = declarative_base()

UserSession = sessionmaker()
UserSession.configure(bind=engine_user_db)


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


template_key = """
class {name}(models.__list__['{name}'], base_user_db):
    \"\"\"
    {desc}
    \"\"\"
    __tablename__ = "{name}"
    __attrtype__ = "{attrtype}"
    id = Column(Integer, primary_key=True) """
template_value = "    {name} = Column({type}({length}))\n"
template_service = """\n    def __repr__(self):
        return "{attrkey}: {attrvalues}".format({attrdef})
"""

__list__ = {}


def build_class_from_dict(cls={}):
    """
    Build classes from a dictionary and execute them
    param: dict cls: the dictionary source
    example of dictionary:
        {
        # Subject attributes
          'Subject': {
            'attributes': (
                    {'name': "uuid", "type": "String", "length": 32},
                    {'name': "name", "type": "String", "length": 254},
                    ),
            'type': "AttrKey",
            'description': "A user in the system.",
        },
    """
    constructor = ""
    for key in cls.keys():
        logger.info("Initializing class {}".format(key))
        constructor += "{tk}\n".format(
            tk=template_key.format(
                name=key,
                attrtype=cls[key]['type'],
                desc=cls[key]['description']
            )
        )
        for attr in cls[key]['attributes']:
            if "length" not in attr.keys():
                attr['length'] = 32
            constructor += template_value.format(
                name=attr["name"],
                type=attr["type"],
                length=attr['length']
            )
        # print(cls[key]['attributes'])
        constructor += template_service.format(
            attrkey=key,
            attrvalues=' '.join(map(lambda x: "{x}={{{x}}}".format(x=x['name']), cls[key]['attributes'])),
            attrdef=', '.join(map(lambda x: "{x}=self.{x}".format(x=x['name']), cls[key]['attributes'])),
        )
        constructor += "__list__['{name}'] = {name}".format(name=key)
    print(constructor)
    # Warning: possible security hazard here!!!
    # TODO: check for integrity of cls
    exec constructor


def add_element(table=None, elem={}):
    query = ""
    obj = None
    q = None
    s = get_user_session()
    cls = eval("__list__['{}']".format(table))
    # logger.info("Adding element in {} ({})".format(table, elem))
    if "uuid" in elem:
        q = s.query(cls).filter_by(uuid=elem["uuid"])
    elif "name" in elem:
        q = s.query(cls).filter_by(name=elem["name"])
    else:
        # we are in a assignment table so we must find x_uuid and y_uuid
        uuid_keys = filter(lambda x: "uuid" in x, elem.keys())
        param = dict()
        for key in uuid_keys:
            param[key] = elem[key]
        q = s.query(cls).filter_by(**param)
    if q.count() > 0:
        record = q.first()
        logger.debug("Updating {}".format(elem["name"]))
        for key in elem.keys():
            # Warning security hazard
            # TODO: check for integrity of elem and key
            if type(elem[key]) == str or type(elem[key]) == unicode:
                exec "record.{key} = '{value}'".format(key=key, value=elem[key])
            else:
                exec "record.{key} = {value}".format(key=key, value=elem[key])
    else:
        param = ", ".join(map(lambda x: "{x}=elem['{x}']".format(x=x), elem.keys()))
        logger.debug("param before add = {}".format(param))
            # Warning security hazard
            # TODO: check for integrity of table and param
        obj = eval("__list__['{name}']({param})".format(name=table, param=param))
        s.add(obj)
    s.commit()
    return obj


def get_elements(type="Subject"):
    """
    Return all elements of type "type"
    """
    logger.info(__list__)
    cls = eval("__list__['{name}']".format(name=type))
    s = get_user_session()
    query = s.query(cls)
    elements = []
    attrs = filter(lambda x: not x.startswith("_"), dir(cls))
    for instance in query:
        __mycls = cls()
        for attr in attrs:
            setattr(__mycls, attr, eval("instance.{}".format(attr)))
        elements.append(__mycls)
    return elements


def get_element(uuids={}, type="Subject"):
    """
    Return an element (subject, Role, ...) given its UUID
    """
    # TODO: check if type is a valid object (ie defined in settings or elsewhere)
    logger.info(__list__)
    cls = eval("__list__['{name}']".format(name=type))
    s = get_user_session()
    q = s.query(cls).filter_by(**uuids)
    record = q.first()
    # TODO: we have to deals with multiple results
    return record


def check_assignment(uuids={}, type="SubjectRoleAssignment"):
    """
    Return True if UUID listed in 'uuids' match in table 'type'
    """
    # TODO: check if type is a valid object (ie defined in settings or elsewhere)
    cls = eval(type)
    s = get_user_session()
    # TODO: check if uuids are correct in a security point of vue
    q = s.query(cls).filter_by(**uuids)
    record = q.first()
    # TODO: we have to deals with multiple results
    return record



# class Subject(models.Subject, base_user_db):
#     """
#     Database Model for a User
#     """
#     __tablename__ = 'user'
#     id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
#     name = Column(String(50))
#     uuid = Column(String(32))
#     password = Column(String(50))
#     email = Column(String(100))
#     description = Column(String(250))
#     enabled = Column(Boolean)
#
#     def __repr__(self):
#         return "Subject: {user} ({uuid}) {email} {description} {enabled}".format(
#             user=self.name,
#             uuid=self.uuid,
#             email=self.email,
#             description=self.description,
#             enabled=self.enabled
#         )
#
#
# class Role(models.Role, base_user_db):
#     """
#     Database Model for a Role
#     """
#     __tablename__ = 'role'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     uuid = Column(String(32))
#     tenant_uuid = Column(String(32))
#     description = Column(String(250))
#     enabled = Column(Boolean)
#
#     def __repr__(self):
#         return "Role: {role} ({uuid}) {tenant_uuid} {description} {enabled}".format(
#             role=self.name,
#             uuid=self.uuid,
#             tenant_uuid=self.tenant_uuid,
#             description=self.description,
#             enabled=self.enabled
#         )
#
#
# class UserRoleAssignment(models.UserRoleAssignment, base_user_db):
#     """
#     Database Model for relations between User and Role
#     """
#     __tablename__ = 'user_role_assignment'
#     id = Column(Integer, primary_key=True)
#     user_uuid = Column(String(32))
#     role_uuid = Column(String(32))
#
#     def __repr__(self):
#         return "{user_uuid}, {role_uuid}".format(
#             user_uuid=self.user_uuid,
#             role_uuid=self.role_uuid,
#         )


# def add_user_to_userdb(user):
#     """
#     Add a user in User DB from a Keystone User
#     """
#     s = get_user_session()
#     try:
#         email = user.email
#     except TypeError:
#         email = ""
#     except AttributeError:
#         email = ""
#     u = Subject(
#         name=user.name,
#         password="<Unknown>",
#         uuid=user.id,
#         email=email,
#         enabled=user.enabled
#     )
#     q = s.query(Subject).filter_by(uuid=user.id)
#     if q.count() > 0:
#         record = q.first()
#         logger.debug("Updating {}".format(user.name))
#         record.name = user.name
#         record.email = email
#         record.enabled = user.enabled
#     else:
#         logger.debug("Adding {}".format(user.name))
#         s.add(u)
#     s.commit()
#
#
# def add_role_to_userdb(role, project):
#     """
#     Add a role in User DB from a Keystone Role
#     """
#     s = get_user_session()
#     r = Role(
#         name=role.name,
#         uuid=role.id,
#         tenant_uuid=project.id,
#         # description=role.description,
#         # enabled=role.enabled
#     )
#     q = s.query(Role).filter_by(uuid=role.id, tenant_uuid=project.id)
#     if q.count() > 0:
#         record = q.first()
#         # logger.info("Updating {}/{}".format(role.name, project.id))
#         record.name = role.name
#     else:
#         # logger.info("Adding {}/{}".format(role.name, project.id))
#         s.add(r)
#     s.commit()
#
#
# def add_userroleassignment_to_userdb(user, role):
#     """
#     Add a user role assignment in User DB from Keystone information
#     """
#     s = get_user_session()
#     # logger.info("Adding role {role} to user {user} to User DB".format(
#     #     role=role.name,
#     #     user=user.name,
#     # ))
#     r = UserRoleAssignment(
#         role_uuid=role.id,
#         user_uuid=user.id,
#     )
#     q = s.query(UserRoleAssignment).filter_by(
#         role_uuid=role.id,
#         user_uuid=user.id,
#     )
#     if q.count() == 0:
#         # logger.info("Count = 0")
#         s.add(r)
#         s.commit()

# def get_user(uuid=None, name=None):
#     """
#     Get a user with his name or UUID
#     """
#     s = get_user_session()
#     q = None
#     if uuid:
#         q = s.query(Subject).filter_by(uuid=uuid)
#     else:
#         q = s.query(Subject).filter_by(name=name)
#     record = q.first()
#     # TODO: we have to deals with multiple results
#     return record
#
#
# def get_role(uuid=None, name=None, project_uuid=None):
#     """
#     Get a role with his name or UUID on a specific project
#     """
#     s = get_user_session()
#     q = None
#     if uuid:
#         q = s.query(Role).filter_by(uuid=uuid, project_uuid=project_uuid)
#     else:
#         q = s.query(Role).filter_by(name=name, project_uuid=project_uuid)
#     record = q.first()
#     # TODO: we have to deals with multiple results
#     return record

