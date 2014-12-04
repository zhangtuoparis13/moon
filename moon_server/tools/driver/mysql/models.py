from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey #noqa
from sqlalchemy import Boolean #noqa
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.dialects.mysql import INTEGER as Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from moon_server import settings
# from moon.info_repository import models #noqa
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

UserSession = sessionmaker(expire_on_commit=False)
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


def get_tables():
    """
    Return all tables of the user DB.
    """
    return base_user_db.metadata.tables.keys()


template_key = """
class {name}(models.__list__['{name}'], base_user_db):
    \"\"\"
    {desc}
    \"\"\"
    __tablename__ = "{name}"
    __attrtype__ = "{attrtype}" """
#    id = Column(Integer(32), primary_key=True) """
template_value = "    {name} = Column({type}({parameters}){pkey})\n"
template_service = """\n    def __repr__(self):
        return "{attrkey}: {attrvalues}".format({attrdef})
"""
pkey = ", primary_key=True"

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
                    {'name': "uuid", "type": "String", "parameters": (32, )},
                    {'name': "name", "type": "String", "parameters": (254, )},
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
            _pkey = ""
            if "parameters" not in attr.keys():
                attr['parameters'] = list()
            parameters = []
            for param in attr['parameters']:
                if type(param) is str:
                    parameters.append("'{}'".format(param))
                else:
                    parameters.append(str(param))
            if attr["type"] == "ForeignKey":
                attr["type"] = "String(32), ForeignKey"
            if attr["name"] == "uuid":
                _pkey = pkey
                attr["type"] = "String"
            # else:
            #     _pkey = ""
            constructor += template_value.format(
                name=attr["name"],
                type=attr["type"],
                parameters=",".join(parameters),
                pkey=_pkey
            )
        # print(cls[key]['attributes'])
        constructor += template_service.format(
            attrkey=key,
            attrvalues=' '.join(map(lambda x: "{x}={{{x}}}".format(x=x['name']), cls[key]['attributes'])),
            attrdef=', '.join(map(lambda x: "{x}=self.{x}".format(x=x['name']), cls[key]['attributes'])),
        )
        constructor += "__list__['{name}'] = {name}".format(name=key)
    # print(constructor)
    # Warning: possible security hazard here!!!
    # TODO: check for integrity of cls
    exec constructor


def add_element(table=None, elem={}):
    logger.info("Add element: {} {}".format(table, elem))
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
        try:
            logger.debug("Updating {}/{}".format(table, elem["name"]))
        except KeyError:
            logger.debug("Updating {}/{}".format(table, elem))
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
    s.close()
    return obj


def get_elements(type="Subject"):
    """
    Return all elements of type "type"
    """
    # logger.info(__list__)
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
    s.close()
    return elements


def get_element(attributes=dict(), type="Subject"):
    """
    Return an element (subject, Role, ...) given its attributes
    """
    # TODO: check if type is a valid object (ie defined in settings or elsewhere)
    cls = eval("__list__['{name}']".format(name=type))
    s = get_user_session()
    query = s.query(cls).filter_by(**attributes)
    elements = []
    attrs = filter(lambda x: not x.startswith("_"), dir(cls))
    for instance in query:
        __mycls = cls()
        for attr in attrs:
            setattr(__mycls, attr, eval("instance.{}".format(attr)))
        elements.append(__mycls)
    s.close()
    return elements


def get_attrs_list(type='Subject'):
    """Return the attribute list for an specific object (ie its columns)
    """
    cls = eval("__list__['{name}']".format(name=type))
    return map(lambda x: str(x).split(".")[-1], cls.__table__.columns)


def delete_element(table="Subject", attributes=dict()):
    """Delete a specific element of the database.
    """
    cls = eval("__list__['{name}']".format(name=table))
    with engine_user_db.begin() as cnx:
        cnx.execute(cls.__table__.delete().where(cls.uuid == attributes["uuid"]))


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


def delete_tables():
    """ Delete all tables for cleaning purposes.
    """
    logger.warning("Drop all tables")
    base_user_db.metadata.drop_all(engine_user_db)
