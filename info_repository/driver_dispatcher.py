import logging
from moon.gi import settings as gi_settings
from moon import settings
import importlib
from moon.info_repository import models
import os
import uuid
# from keystoneclient.v3.users import User
# from keystoneclient.v3.roles import Role

logger = logging.getLogger("moon.driver_dispatcher")

DATABASES = getattr(settings, "DATABASES")
if not 'user_db' in DATABASES or not 'ENGINE' in DATABASES['user_db']:
    raise(Exception("Unknown database engine {engine}".format(engine=DATABASES['user_db']['ENGINE'])))

drivername = DATABASES['user_db']['ENGINE']
driver = importlib.import_module(drivername)


class Users:
    """
    Class for all users
    """
    def __init__(self, kclient):
        self.kclient = kclient
        self.users = {}
        subjects = driver.get_elements(type="Subject")
        # attrs = filter(lambda x: not x.startswith("_"), dir(User))
        for subject in subjects:
            # __user = User()
            # for attr in attrs:
            #     setattr(__user, attr, eval("subject.{}".format(attr)))
            self.users[subject.uuid] = subject

    def create(self,
               name="",
               password="",
               domain="",
               project="",
               email="",
               description="",
               enabled=True):
        """
        Create the user in Moon database and Keystone database
        """
        kuser = self.kclient.users.create(
            name=name,
            password=password,
            domain=domain,
            project=project,
            email=email,
            description=description,
            enabled=enabled
        )
        muser = create_element(values={
            'name': name,
            'password': password,
            'uuid': kuser.id,
            'domain': domain,
            'project': project,
            'mail': email,
            'description': description,
            'enabled': enabled
        })
        logger.info("Add user {}".format(str(muser)))
        # TODO: check if Keystone creation was successful
        # driver.add_user_to_userdb(muser)
        self.users[kuser.id] = muser
        return muser

    def list_from_keystone(self, sort=True):
        """
        Return all users from the Keystone service.
        """
        if sort:
            users = sorted(self.kclient.users.list(), key=lambda _user: _user.name)
        else:
            users = self.kclient.users.list()
        return users

    def list(self, sort=True):
        """
        Return all users from the local database.
        """
        if sort:
            users = sorted(self.users.values(), key=lambda _user: _user.name)
        else:
            users = self.users.values()
        return users

    def get_user(self, uuid=None):
        """
        Return a specific user from the Keystone service.
        """
        user = ()
        # TODO: connect to moon DB
        for _user in self.kclient.users.list():
            if _user.id == uuid:
                user = _user
        user.project = user.default_project_id
        for _project in self.kclient.projects.list():
            if user.default_project_id == _project.id:
                user.project = _project.name
        user.domain = user.domain_id
        return user


true_values = ("true", "y", "yes", "oui", "on")


def create_element(type='Subject', values=dict()):
    if "uuid" not in values:
        values["uuid"] = str(uuid.uuid4()).replace("-", "")
    if "enabled" in values:
        if values["enabled"].lower() in true_values:
            values["enabled"] = 1
        else:
            values["enabled"] = 0
    return driver.add_element(table=type, elem=values)


def delete_element(table='Subject', values=dict()):
    return driver.delete_element(table=table, attributes=values)


def get_tables():
    """
    Return the list of all tables contained in the DB
    :returns: list of strings
    """
    return driver.get_tables()


def get_elements(type='Subject'):
    """Return all elements for a specific DB table

    :param type: (str) name of the table to search in (default: Subject)

    :returns: list of strings

    """
    return get_element(type=type, attributes={})


def get_element(type='Subject', attributes=dict()):
    """Return filtered elements for a specific DB table

    :param type: (str) name of the table to search in (default: Subject)
    :param attributes: (dict) attributes for filtering (default empty dict)
                       example of attributes {'uuid': "123456", 'tenant_uuid': "123456"}

    :returns: list of strings

    """
    return driver.get_element(attributes=attributes, type=type)


def get_attrs_list(type='Subject'):
    """Return the attribute list for an specific object (ie its columns)
    """
    return driver.get_attrs_list(type=type)


def get_db_diag(filename="db_diag.svg"):
    static_dir = getattr(gi_settings, 'STATICFILES_DIRS', "")[0]
    import pygraphviz as pgv
    graph = pgv.AGraph(directed=True, rankdir="LR")
    __dict = {}
    for table in get_tables():
        __dict[table.lower()] = {}
        label = "<f0> " + table + " |"
        attr_list =[]
        cpt = 1
        for attr in get_attrs_list(type=table):
            attr_list.append("<f{cpt}> {attr}".format(cpt=cpt, attr=attr))
            __dict[table.lower()][attr] = "f{}".format(cpt)
            cpt += 1
        label += "|".join(attr_list)
        graph.add_node(table, label=label, shape="record")
    for table in get_tables():
        if "Assignment" in table:
            for column in get_attrs_list(type=table):
                if column.split("_")[0] in __dict.keys():
                    node1 = "{}".format(table)
                    node2 = "{}".format(column.split("_")[0].title())
                    # node1 = "{}:{}".format(table, __dict[column.split("_")[0]][column.split("_")[1]])
                    # node2 = "{}:{}".format(column.split("_")[0], __dict[table.lower()][column])
                    graph.add_edge(node1, node2)
    graph.draw(os.path.join(static_dir, filename), format="svg", prog="dot")
    return filename


def delete_tables():
    build_class_from_dict(getattr(settings, "INITIAL_DB"))
    driver.delete_tables()


def add_user_from_keystone(obj=None):
    table = "Subject"
    values = dict()
    values['uuid'] = obj.id
    values['name'] = obj.name
    values['password'] = "<Unknown>"
    values['enabled'] = obj.enabled
    driver.add_element(table=table, elem=values)


def add_role_from_keystone(obj=None, tenant=None):
    table = "Role"
    values = dict()
    values['uuid'] = obj.id
    values['name'] = obj.name
    values['tenant_uuid'] = tenant.id
    values['enabled'] = True
    driver.add_element(table=table, elem=values)


def add_userroleassignment_from_keystone(user=None, role=None):
    table = "SubjectRoleAssignment"
    values = dict()
    values['user_uuid'] = user.id
    values['role_uuid'] = role.id
    driver.add_element(table=table, elem=values)


def add_element_from_keystone(user=None, role=None, tenant=None):
    """
    Add an object in a database table based on Keystone object
    """
    if user and role:
        add_userroleassignment_from_keystone(user=user, role=role)
    elif user and not role:
        add_user_from_keystone(obj=user)
    elif not user and role:
        add_role_from_keystone(obj=role, tenant=tenant)


def get_user_session():
    """
    Return the session associated with the User DB
    """
    return driver.UserSession()


def create_tables(cls=None):
    """
    Create all tables in database.
    """
    build_class_from_dict(cls)
    driver.create_tables()


# def add_user_to_userdb(user=None):
#     driver.add_user_to_userdb(user=user)
#
#
# def add_role_to_userdb(role=None, project=None):
#     driver.add_role_to_userdb(role=role, project=project)
#
#
# def add_userroleassignment_to_userdb(user=None, role=None):
#     driver.add_userroleassignment_to_userdb(user=user, role=role)


#def get_user(uuid=None):
def update_request_attributes(
        subject=None,
        action=None,
        object_name=None,
        tenant=None,
        attributes=None):
    """
    Get user information:
        - user attributes (name, description, ...)
        - roles in specific tenants
    Example:
        - User(name=John, description=...)
        - Tenant1, RoleAdmin, RoleUser
        - Tenant2, RoleUser
    Return a JSON Object:
        { 'user':
            {'name': "John", 'description': "a user..."},
          'tenants':
          (
            {
                'name': "tenant1",
                'description': "..."
                'attributes':
                {
                    'attribute_name': "attribute_value",
                    'role': ( "admin", "user" ),
                    'group': ( 'group1', 'group2' )
                }
            },
            {
                'name': "tenant2",
                'description': "..."
                'attributes':
                {
                    'attribute_name': "attribute_value",
                    'domain': ( "domain1", "domain2" )
                }
            },
          )
        }
    """
    # TODO: send a JSON Object ???
    attributes['s_attrs'] = driver.get_user(uuid=subject)
    # attributes['o_attrs'] = driver.get_user(uuid=subject)
    # attributes['a_attrs'] = driver.get_user(uuid=subject)
    return attributes


def build_class_from_dict(cls):
    models.build_class_from_dict(cls)
    driver.build_class_from_dict(cls)


def get_user(name=None, uuid=None):
    """
    Get a user with his name or UUID
    """
    return driver.get_element({'uuid': uuid}, type="Subject")


def get_role(uuid=None, name=None, project_uuid=None):
    """
    Get a role with his name or UUID on a specific project
    """
    return driver.get_element({'uuid':uuid, 'tenant_uuid':project_uuid}, type="Role")