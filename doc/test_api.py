class BasicInterface(object):

    def __init__(self):
        self.__subjects = []
        self.__objects = []
        self.__objectsAttributes = []
        self.__subjectsAttributes = []
        self.__objectsAssignments = []
        self.__subjectsAssignments = []
        self.__rules = []
        self.__metadata = {}
        self.__uuid = ""

    def __get_subjects(self):
        return self.__subjects

    def __get_objects(self):
        return self.__objects

    def __get_subject_attribute_categories(self):
        """ Return all categories for subjects

        :return:
        """
        return self.__metadata["s_attr"]

    def __get_object_attribute_categories(self):
        """ Return all categories for objects

        :return:
        """
        return self.__metadata["o_attr"]

    def __get_subject_attributes(self, subject_name, category=None):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        pass

    def __get_object_attributes(self, object_name, category=None):
        """

        :param object_name:
        :return: a list of dict with value and category
        """
        pass

    def __get_subject_attribute_assignments(self, subject_name=None, category=None):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        pass

    def __get_object_attribute_assignments(self, object_name=None, category=None):
        """

        :param object_name:
        :return: a list of dict with value and category
        """
        pass

    def __get_rules(self):
        """

        :return:
        """
        pass


class PublicAuthzInterface(BasicInterface):

    def __init__(self):
        super(PublicAuthzInterface, self).__init__()

    def authz(self, request):
        s = self.__subjects


class PublicAdminInterface(BasicInterface):

    def __init__(self):
        super(PublicAdminInterface, self).__init__()
        self.__adminObjects = []
        self.__adminSubjects = []
        self.__adminObjectsAttributes = []
        self.__adminSubjectsAttributes = []
        self.__adminObjectsAssignments = []
        self.__adminSubjectsAssignments = []
        self.__adminRules = []
        self.__prolog_metadata = "/var/cache/prolog/metadata/{}".format(self.__uuid)
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

    @enforce("")
    def get_subjects(self):
        return self.__subjects

    @enforce("")
    def get_objects(self):
        return self.__objects

    @enforce("")
    def get_subject_attribute_categories(self):
        """ Return all categories for subjects

        :return:
        """
        return self.__metadata["s_attr"]

    @enforce("")
    def get_object_attribute_categories(self):
        """ Return all categories for objects

        :return:
        """
        return self.__metadata["o_attr"]

    @enforce("")
    def get_subject_attributes(self, subject_name, category=None):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        return self.__get_subject_attributes(subject_name=subject_name, category=category)

    @enforce("")
    def get_object_attributes(self, object_name, category=None):
        """

        :param object_name:
        :return: a list of dict with value and category
        """
        pass

    @enforce("")
    def get_subject_attribute_assignments(self, subject_name=None, category=None):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        pass

    @enforce("object_assignment")
    def get_object_attribute_assignments(self, object_name=None, category=None):
        """

        :param object_name:
        :return: a list of dict with value and category
        """
        pass

    @enforce("rules")
    def get_rules(self):
        """

        :return:
        """
        pass

    #TODO add, del, mod

    @enforce("rules", "w")
    def add_rule(self, name, subject_attrs, object_attrs, desription=""):
        pass
        #TODO: check metadata to only add categories in self.__metadata

    @enforce("rules", "w")
    def mod_rule(self, uuid, name="", subject_attrs=[], object_attrs=[], desription=""):
        pass
        #TODO: check metadata to only add categories in self.__metadata

    @enforce("rules", "w")
    def del_rule(self, uuid):
        pass

    def adminAuthz(self, admin_object_name, action, user):
        pass


def enforce(param, mode="r"):
    def enforce_decorated(function):
        def wrapped(*args, **kwargs):
            interface = locals().get("args")[0]
            s = super(PublicAdminInterface, interface).__get_subjects(interface)
            try:
                interface.adminAuthz()
            except MyException:
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