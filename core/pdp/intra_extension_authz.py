from moon.core.pdp.extension import Extension


class AuthzExtension(Extension):
    def authz(self, sub, obj, act):
        pass

'''
class AuthzExtension(Extension):
    def authz(self, sub, obj, act):
        """Authz interface
        """
        pass

    def get_subjects(self):
        return set(self.__perimeter.subjects)
    #
    # @enforce("perimeter.subjects", "w")
    # def add_subject(self, name, description="", domain="Default", enabled=True, project=None, mail=""):
    #     return self.__extension.add_subjects(name, description, domain, enabled, project, mail)
    #
    # @enforce("perimeter.subjects", "w")
    # def del_subject(self, uuid):
    #     return self.__extension.del_subject(uuid)
    #
    # @enforce("perimeter.subjects", "w")
    # def set_subject(self, uuid, name="", description="", domain="Default", enabled=True, project=None, mail=""):
    #     return self.__extension.set_subject(self, uuid, name, description, domain, enabled, project, mail)
    #
    # @enforce("perimeter.objects")
    # def get_objects(self, uuid="", name=""):
    #     return self.__extension.get_objects(uuid, name)
    #
    # @enforce("perimeter.objects", "w")
    # def add_object(self, name, uuid="", description="", enabled=True, project=None):
    #     return self.__extension.add_objects(
    #         name=name,
    #         uuid=uuid,
    #         description=description,
    #         enabled=enabled,
    #         project=project)
    #
    # @enforce("perimeter.objects", "w")
    # def del_object(self, uuid):
    #     return self.__extension.del_object(uuid)
    #
    # @enforce("perimeter.objects", "w")
    # def set_object(self, uuid, name="", enabled=True, description="", project=None):
    #     return self.__extension.set_objects(
    #         uuid=uuid,
    #         name=name,
    #         enabled=enabled,
    #         description=description,
    #         project=project)
    #
    # @enforce("configuration.metadata") #TODO get_subject_categories
    # def get_subject_attribute_categories(self, name):
    #     """ Return all categories for subjects
    #
    #     :return:
    #     """
    #     return self.__extension.get_subject_attribute_categories(name)
    #
    # @enforce("configuration.metadata", "w")
    # def add_subject_attribute_categories(self, name):
    #     """ Return all categories for subjects
    #
    #     :return:
    #     """
    #     return self.__extension.add_subject_attribute_categories(name)
    #
    # @enforce("configuration.metadata", "w")
    # def del_subject_attribute_categories(self, name):
    #     """ Return all categories for subjects
    #
    #     :return:
    #     """
    #     return self.__extension.del_subject_attribute_categories(name)
    #
    # @enforce("configuration.metadata") #TODO get_object_categories
    # def get_object_attribute_categories(self):
    #     """ Return all categories for objects
    #
    #     :return:
    #     """
    #     return self.__extension.get_object_attribute_categories()
    #
    # @enforce("configuration.metadata", "w")
    # def add_object_attribute_categories(self, name):
    #     """ Return all categories for subjects
    #
    #     :return:
    #     """
    #     return self.__extension.add_object_attribute_categories(name)
    #
    # @enforce("configuration.metadata", "w")
    # def del_object_attribute_categories(self, name):
    #     """ Return all categories for subjects
    #
    #     :return:
    #     """
    #     return self.__extension.del_object_attribute_categories(name)
    #
    # @enforce("profiles.s_attr")  #TODO get_subject_category_values
    # def get_subject_attributes(self, uuid=None, value=None, category=None):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.get_subject_attributes(uuid=uuid, value=value, category=category)
    #
    # @enforce("profiles.s_attr", "w")
    # def add_subject_attributes(self, value, uuid=None, category=None, description=""):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.add_subject_attributes(
    #         value=value,
    #         uuid=uuid,
    #         category=category,
    #         description=description)
    #
    # @enforce("profiles.s_attr", "w")
    # def del_subject_attributes(self, uuid):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.del_subject_attributes(uuid)
    #
    # @enforce("profiles.s_attr", "w") #TODO delete
    # def set_subject_attributes(self, uuid, value="", category=None, description=""):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.set_subject_attributes(
    #         uuid=uuid,
    #         value=value,
    #         category=category,
    #         description=description)
    #
    # @enforce("profiles.o_attr")  #TODO get_object_category_values
    # def get_object_attributes(self, uuid=None, value=None, category=None):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.get_object_attributes(uuid=uuid, value=value, category=category)
    #
    # @enforce("profiles.o_attr", "w")
    # def add_object_attributes(self, value, uuid=None, category=None, description=""):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.add_object_attributes(
    #         value=value,
    #         uuid=uuid,
    #         category=category,
    #         description=description)
    #
    # @enforce("profiles.o_attr", "w")
    # def del_object_attributes(self, uuid):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.del_object_attributes(uuid)
    #
    # @enforce("profiles.o_attr", "w") #TODO delete
    # def set_object_attributes(self, uuid, value="", category=None, description=""):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.set_object_attributes(
    #         uuid=uuid,
    #         value=value,
    #         category=category,
    #         description=description)
    #
    # @enforce("profiles.s_attr_assign") #TODO get_subject_assignments(category_id)
    # def get_subject_attribute_assignments(self, uuid=None, subject_name=None, category=None):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.get_subject_attribute_assignments(
    #         uuid=uuid,
    #         subject_name=subject_name,
    #         category=category)
    #
    # @enforce("profiles.s_attr_assign", "w") #TODO add_subject_assignment(category_id, subject_id, category_value)
    # def add_subject_attribute_assignments(self, subject_name, category, uuid=None, attributes=None):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.add_subject_attribute_assignments(
    #         subject_name=subject_name,
    #         category=category,
    #         uuid=uuid,
    #         attributes=attributes)
    #
    # @enforce("profiles.s_attr_assign", "w") #TODO del_subject_assignment(category_id, subject_id, category_value)
    # def del_subject_attribute_assignments(self, uuid=None, subject_name=None, category=None):
    #     """
    #
    #     :param subject_name:
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.del_subject_attribute_assignments(
    #         uuid=uuid,
    #         subject_name=subject_name,
    #         category=category)
    #
    # @enforce("profiles.s_attr_assign", "w") #TODO delete
    # def set_subject_attribute_assignments(self, uuid=None, subject_name=None, category=None, attributes=None):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.set_subject_attribute_assignments(
    #         uuid=uuid,
    #         subject_name=subject_name,
    #         category=category,
    #         attributes=attributes)
    #
    # @enforce("profiles.o_attr_assign") #TODO get_object_assignments(category_id)
    # def get_object_attribute_assignments(self, uuid=None, object_name=None, category=None):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.get_object_attribute_assignments(
    #         uuid=uuid,
    #         object_name=object_name,
    #         category=category)
    #
    # @enforce("profiles.o_attr_assign", "w") #TODO add_object_assignment(category_id, object_id, category_value)
    # def add_object_attribute_assignments(self, uuid=None, object_name=None, category=None, attributes=None):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.add_object_attribute_assignments(
    #         uuid=uuid,
    #         object_name=object_name,
    #         category=category,
    #         attributes=attributes)
    #
    # @enforce("profiles.o_attr_assign", "w") #TODO del_object_assignment(category_id, object_id, category_value)
    # def del_object_attribute_assignments(self, uuid=None, object_name=None, category=None):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.del_object_attribute_assignments(
    #         uuid=uuid,
    #         object_name=object_name,
    #         category=category)
    #
    # @enforce("profiles.o_attr_assign", "w") #TODO  delete
    # def set_object_attribute_assignments(self, uuid=None, object_name=None, category=None, attributes=None):
    #     """
    #
    #     :return: a list of dict with value and category
    #     """
    #     return self.__extension.set_object_attribute_assignments(
    #         uuid=uuid,
    #         object_name=object_name,
    #         category=category,
    #         attributes=attributes)
    #
    # @enforce("rules")
    # def get_rules(self):
    #     """
    #
    #     :return:
    #     """
    #     return self.__extension.get_rules()
    #
    # @enforce("rules", "w")
    # def add_rule(self, name, subject_attrs, object_attrs, description=""):
    #     return self.__extension.add_rule(
    #         name=name,
    #         subject_attrs=subject_attrs,
    #         object_attrs=object_attrs,
    #         description=description)
    #
    # @enforce("rules", "w") #TODO  delete
    # def set_rule(self, uuid, name="", subject_attrs=None, object_attrs=None, description=""):
    #     return self.__extension.set_rule(
    #         uuid=uuid,
    #         name=name,
    #         subject_attrs=subject_attrs,
    #         object_attrs=object_attrs,
    #         description=description)
    #
    # @enforce("rules", "w")
    # def del_rule(self, uuid):
    #     return self.__extension.del_rule(uuid=uuid)

'''