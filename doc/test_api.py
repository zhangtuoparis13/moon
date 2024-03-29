from moon.tools.exceptions import AuthzException


class IntraExtension(object):

    def __init__(self):
        self.__uuid = ""
        self.__name = ""
        self.__tenant = dict()
        self.__subjects = []
        self.__objects = []
        self.__objectsAttributes = []
        self.__subjectsAttributes = []
        self.__objectsAssignments = []
        self.__subjectsAssignments = []
        self.__rules = []
        self.__metadata = {}
        self.__uuid = ""

    def get_uuid__(self):
        return self.__uuid

    def get_name__(self):
        return self.__name

    def get_tenant__(self):
        return self.__tenant

    def get_subjects(self, uuid="", name=""):
        return self.__subjects

    def add_subject(self, name, description="", domain="Default", enabled=True, project=None, mail=""):
        raise NotImplemented

    def del_subject(self, uuid):
        raise NotImplemented

    def set_subject(self, uuid, name="", description="", domain="Default", enabled=True, project=None, mail=""):
        raise NotImplemented

    def get_objects(self, uuid="", name=""):
        return self.__objects

    def add_objects(self, name, enabled=True, description="", tenant=None):
        raise NotImplemented

    def del_objects(self, uuid):
        raise NotImplemented

    def set_objects(self, uuid, name="", enabled=True, description="", tenant=None):
        raise NotImplemented

    def get_subject_attribute_categories(self, name=""):
        """ Return all categories for subjects

        :return:
        """
        return self.__metadata["s_attr"]

    def add_subject_attribute_categories(self, name):
        """ Return all categories for subjects

        :return:
        """
        raise NotImplemented

    def del_subject_attribute_categories(self, uuid):
        """ Return all categories for subjects

        :return:
        """
        raise NotImplemented

    def set_subject_attribute_categories(self, uuid, name):
        """ Return all categories for subjects

        :return:
        """
        raise NotImplemented

    def get_object_attribute_categories(self):
        """ Return all categories for objects

        :return:
        """
        return self.__metadata["o_attr"]

    def add_object_attribute_categories(self, name):
        """ Return all categories for subjects

        :return:
        """
        raise NotImplemented

    def del_object_attribute_categories(self, uuid):
        """ Return all categories for subjects

        :return:
        """
        raise NotImplemented

    def set_object_attribute_categories(self, uuid, name):
        """ Return all categories for subjects

        :return:
        """
        raise NotImplemented

    def get_subject_attributes(self, attribute_name, category=None):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def add_subject_attributes(self, attribute_name, category=None, description=""):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def del_subject_attributes(self, uuid):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def set_subject_attributes(self, uuid, attribute_name="", category=None, description=""):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def get_object_attributes(self, object_name, category=None):
        """

        :param object_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def add_object_attributes(self, attribute_name, category=None, description=""):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def del_object_attributes(self, uuid):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def set_object_attributes(self, uuid, attribute_name="", category=None, description=""):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def get_subject_attribute_assignments(self, subject_name=None, category=None):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def add_subject_attribute_assignments(self, subject_name=None, category=None, attributes=[]):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def del_subject_attribute_assignments(self, uuid, category=None):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def set_subject_attribute_assignments(self, uuid, subject_name=None, category=None, attributes=[]):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def get_object_attribute_assignments(self, object_name=None, category=None):
        """

        :param object_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def add_object_attribute_assignments(self, object_name=None, category=None, attributes=[]):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def del_object_attribute_assignments(self, uuid, category=None):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def set_object_attribute_assignments(self, uuid, object_name=None, category=None, attributes=[]):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    def get_rules(self):
        """

        :return:
        """
        return self.__rules

    def add_rule(self, name, subject_attrs, object_attrs, description=""):
        raise NotImplemented
        #TODO: check metadata to only add categories in self.__metadata

    def set_rule(self, uuid, name="", subject_attrs=[], object_attrs=[], description=""):
        raise NotImplemented
        #TODO: check metadata to only add categories in self.__metadata

    def del_rule(self, uuid):
        raise NotImplemented


class PublicAuthzInterface:

    def __init__(self, extension=None):
        self.__extension = extension
        print("Init of PublicAuthzInterface with uuid=" + self.__extension.get_uuid())
        self.__all__ = (self.authz, )

    def authz(self, request):
        raise NotImplemented


class PublicAdminInterface:

    def __init__(self, extension):
        self.__extension = extension
        self.__adminObjects = []
        self.__adminSubjects = []
        self.__adminObjectsAttributes = []
        self.__adminSubjectsAttributes = []
        self.__adminObjectsAssignments = []
        self.__adminSubjectsAssignments = []
        self.__adminRules = []
        self.__prolog_metadata = "/var/cache/prolog/metadata/{}".format(self.__extension.get_uuid())
        self.__prolog_data = """
attribute_category(subject,attribute_category...) # for each category
attribute_category(object,attribute_category...) # for each category
    example: attribute_category(user_uuid1, admin)
    example: attribute_category(vm_uuid1, vm_uuid1)
    example: attribute_category(vm_uuid1, action_uuid1)
rule_metadata(subject_attribute_category... , object_attribute_category) # for each rule
    example: rule_metadata(role,id,action)
???
subject_attributes(subject_category1..., value1...) # for each subject_attribute category
object_attributes(object_category1..., value1...) # for each object_attribute category
    example: subject_attributes(role,admin_uuid1)
    example: object_attributes(id,vm_uuid1)
    example: object_attributes(action,action_uuid1)
subject_attribute_assignments(subject..., attribute_value1...) # for each subject
object_attribute_assignments(object..., attribute_value1...) # for each object
    example: subject_attribute_assignments(user_uuid1,admin_uuid1)
    example: object_attribute_assignments(vm_uuid1,vm_uuid1)
    example: object_attribute_assignments(vm_uuid1,action_uuid1)
rule(
    subject_attribute_category1_value1, subject_attribute_category2_value1, ... subject_attribute_categoryn_value1,
    object_attribute_category1_value1, object_attribute_category2_value1, ... object_attribute_categoryn_value1
)
    example: rule (admin_uuid1, vm_uuid1, action_uuid1)


         """

    @enforce("perimeter.subjects")
    def get_subjects(self, uuid="", name=""):
        return self.__extension.get_subjects(uuid, name)

    @enforce("perimeter.subjects", "w")
    def add_subject(self, name, description="", domain="Default", enabled=True, project=None, mail=""):
        return self.__extension.add_subjects(name, description, domain, enabled, project, mail)

    @enforce("perimeter.subjects", "w")
    def del_subject(self, uuid):
        return self.__extension.del_subject(uuid)

    @enforce("perimeter.subjects", "w")
    def set_subject(self, uuid, name="", description="", domain="Default", enabled=True, project=None, mail=""):
        return self.__extension.set_subject(self, uuid, name, description, domain, enabled, project, mail)

    @enforce("perimeter.objects")
    def get_objects(self, uuid="", name=""):
        return self.__extension.get_objects(uuid, name)

    @enforce("perimeter.objects", "w")
    def add_objects(self, name, enabled=True, description="", tenant=None):
        raise NotImplemented

    @enforce("perimeter.objects", "w")
    def del_objects(self, uuid):
        raise NotImplemented

    @enforce("perimeter.objects", "w")
    def set_objects(self, uuid, name="", enabled=True, description="", tenant=None):
        raise NotImplemented

    @enforce("configuration.metadata")
    def get_subject_attribute_categories(self, name=""):
        """ Return all categories for subjects

        :return:
        """
        return self.__extension.get_metadata["s_attr"]

    @enforce("configuration.metadata", "w")
    def add_subject_attribute_categories(self, name):
        """ Return all categories for subjects

        :return:
        """
        raise NotImplemented

    @enforce("configuration.metadata", "w")
    def del_subject_attribute_categories(self, uuid):
        """ Return all categories for subjects

        :return:
        """
        raise NotImplemented

    @enforce("configuration.metadata", "w")
    def set_subject_attribute_categories(self, uuid, name):
        """ Return all categories for subjects

        :return:
        """
        raise NotImplemented

    @enforce("configuration.metadata")
    def get_object_attribute_categories(self):
        """ Return all categories for objects

        :return:
        """
        return self.__extension.get_metadata["o_attr"]

    @enforce("configuration.metadata", "w")
    def add_object_attribute_categories(self, name):
        """ Return all categories for subjects

        :return:
        """
        raise NotImplemented

    @enforce("configuration.metadata", "w")
    def del_object_attribute_categories(self, uuid):
        """ Return all categories for subjects

        :return:
        """
        raise NotImplemented

    @enforce("configuration.metadata", "w")
    def set_object_attribute_categories(self, uuid, name):
        """ Return all categories for subjects

        :return:
        """
        raise NotImplemented

    @enforce("profiles.s_attr")
    def get_subject_attributes(self, attribute_name, category=None):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        return self.__extension.get_get_subject_attributes(attribute_name=attribute_name, category=category)

    @enforce("profiles.s_attr", "w")
    def add_subject_attributes(self, attribute_name, category=None, description=""):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("profiles.s_attr", "w")
    def del_subject_attributes(self, uuid):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("profiles.s_attr", "w")
    def set_subject_attributes(self, uuid, attribute_name="", category=None, description=""):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("profiles.o_attr")
    def get_object_attributes(self, object_name, category=None):
        """

        :param object_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("profiles.o_attr", "w")
    def add_object_attributes(self, attribute_name, category=None, description=""):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("profiles.o_attr", "w")
    def del_object_attributes(self, uuid):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("profiles.o_attr", "w")
    def set_object_attributes(self, uuid, attribute_name="", category=None, description=""):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("profiles.s_attr_assign")
    def get_subject_attribute_assignments(self, subject_name=None, category=None):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("profiles.s_attr_assign", "w")
    def add_subject_attribute_assignments(self, subject_name=None, category=None, attributes=[]):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("profiles.s_attr_assign", "w")
    def del_subject_attribute_assignments(self, uuid, category=None):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("profiles.s_attr_assign", "w")
    def set_subject_attribute_assignments(self, uuid, subject_name=None, category=None, attributes=[]):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("profiles.o_attr_assign")
    def get_object_attribute_assignments(self, object_name=None, category=None):
        """

        :param object_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("profiles.o_attr_assign", "w")
    def add_object_attribute_assignments(self, object_name=None, category=None, attributes=[]):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("profiles.o_attr_assign", "w")
    def del_object_attribute_assignments(self, uuid, category=None):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("profiles.o_attr_assign", "w")
    def set_object_attribute_assignments(self, uuid, object_name=None, category=None, attributes=[]):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        raise NotImplemented

    @enforce("rules")
    def get_rules(self):
        """

        :return:
        """
        return self.__extension.get_get_rules()

    @enforce("rules", "w")
    def add_rule(self, name, subject_attrs, object_attrs, description=""):
        raise NotImplemented
        #TODO: check metadata to only add categories in self.__metadata

    @enforce("rules", "w")
    def set_rule(self, uuid, name="", subject_attrs=[], object_attrs=[], description=""):
        raise NotImplemented
        #TODO: check metadata to only add categories in self.__metadata

    @enforce("rules", "w")
    def del_rule(self, uuid):
        raise NotImplemented

    def adminAuthz(self, admin_object_name, action, user):
        raise NotImplemented


def enforce(param, mode="r"):
    def enforce_decorated(function):
        def wrapped(*args, **kwargs):
            interface = locals().get("args")[0]
            raw_extension = getattr(interface, "_PublicAdminInterface__extension")
            try:
                interface.adminAuthz()
            except AuthzException:
                pass
            result = function(*args, **kwargs)
            return result
        return wrapped
    return enforce_decorated


__PublicAuthzInterface = PublicAuthzInterface()
__PublicAdminInterface = PublicAdminInterface()


#Examples

def get_subjects():
    return __PublicAdminInterface.get_subjects()


def authz(request):
    return __PublicAuthzInterface.authz(request)