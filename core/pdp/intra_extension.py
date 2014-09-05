from uuid import uuid4
import logging
try:
    from django.utils.safestring import mark_safe
except ImportError:
    mark_safe = str
from moon.intra_extension_manager import get_dispatcher
from moon.tools.exceptions import *
from moon.core.pdp.intra_extension_authz import AuthzExtension
from moon.core.pdp.intra_extension_admin import AdminExtension

logger = logging.getLogger(__name__)


class IntraExtension(object):
    def __init__(self):
        self.__intra_extension_authz = AuthzExtension()
        self.__intra_extension_admin = AdminExtension()

    def authz(self, sub, obj, act):
        return self.__intra_extension_authz.authz(sub, obj, act)

    def admin(self, sub, obj, act):
        return self.__intra_extension_admin.authz(sub, obj, act)


'''
class AdminExtension(Extension):
    def authz(self, user_uuid, object_uuid, action):
        """Authz interface
        """
        # auth = {
        #     "auth": False,
        #     "rule_name": "None",
        #     "message": "",
        #     "subject": user_uuid,
        #     "action": "action-write" if mode == "w" else "action-read",
        #     "object_name": obj,
        #     "tenant_name": tenant["name"],
        #     "extension_name": ext.get_name(),
        # }
        # if "objects" not in self.__administration:
        #     auth["message"] = "No administration protocol for extension"
        #     auth["auth"] = True
        #     return auth
        # if self.__tenant["name"] != auth["tenant_name"]:
        #     auth["message"] = "Tenant not found."
        #     return auth
        # if auth["subject"] not in map(lambda x: x["uuid"], self.__subjects):
        #     auth["message"] = "User not found."
        #     return auth
        # if auth["object_name"] not in map(lambda x: x["name"], self.__administration["objects"]):
        #     auth["message"] = "Object not found."
        #     return auth
        # for obj in self.__administration["objects"]:
        #     if obj["name"] == auth["object_name"]:
        #         auth["object_uuid"] = obj["uuid"]
        #         break
        # for rule in self.__administration["rules"]:
        #     _auth = False
        #     for s_rule in rule["s_attr"]:
        #         data = self.__subjectsAssignments
        #         attribute = s_rule["value"]
        #         for sbj in data:
        #             if type(attribute) not in (list, tuple):
        #                 attribute = [attribute, ]
        #             for att in attribute:
        #                 if auth["subject"] == sbj["subject"] and att in sbj["attributes"]:
        #                     _auth = True
        #                     break
        #     if not _auth:
        #         auth["message"] = "Rules on subject don't match."
        #         continue
        #     for o_rule in rule["o_attr"]:
        #             if o_rule["category"] == "action":
        #                 _auth = self.__has_admin_assignment(
        #                     object_uuid=auth["object_uuid"],
        #                     attribute_uuid=auth["action"])
        #                 if not _auth:
        #                     auth["message"] = "Rules on action assignments don't match."
        #                     break
        #                 if auth["action"] not in o_rule["value"]:
        #                     auth["message"] = "Rules on action don't match."
        #                     break
        #             else:
        #                 _auth = self.__has_admin_assignment(
        #                     object_uuid=auth["object_uuid"],
        #                     attribute_uuid=o_rule["value"])
        #                 if not _auth:
        #                     auth["message"] = "Rules on object don't match."
        #                     print(auth["object_uuid"], o_rule["value"])
        #                     break
        #     else:
        #         auth["message"] = ""
        #         auth["auth"] = True
        #         break
        # # auth = ext.authz(auth=auth)
        # # print("\033[32min wrapped\033[m")
        # # try:
        # #     auth = ext.authz(auth=auth)
        # #     print(auth)
        # #     print("\033[32m----------------------------------------\033[m")
        # # except:
        # #     import sys
        # #     print("\033[31mException\033[m", sys.exc_info())
        # # print("\t-> {subject} {action} {object_name} {auth}: {message}".format(**auth))
        # if auth["auth"] is not True:
        #     print("\033[31mCalling {} for {}/{} on {}/{}\033[m".format(
        #         function.__name__,
        #         tenant["name"],
        #         user_uuid,
        #         obj,
        #         mode))
        #     raise AdminException(auth["message"])
        pass


class AuthzExtension(Extension):
    def authz(self):
        """Authz interface
        """
        pass

    def get_subjects(self):
        return set(self.__perimeter.subjects)

    def add_subject(self, subject_id):
        self.__perimeter.subjects.add(subject_id)

    def del_subject(self, subject_id):
        self.__perimeter.subjects.remove(subject_id)
        #TODO need to check if the subject is not in other tables like assignment

    def get_objects(self):
        return set(self.__perimeter.objects)

    def add_object(self, object_id):
        self.__perimeter.objects.add(object_id)

    def del_object(self, object_id):
        return self.__perimeter.objects.remove(object_id)

    def get_subject_categories(self):
        return set(self.__metadata.subject_categories)

    def add_subject_category(self, category_id):
        self.__metadata.subject_categories.add(category_id)

    def del_subject_category(self, category_id):
        self.__metadata.subject_categories.remove(category_id)

    def get_object_categories(self):
        return set(self.__metadata.object_categories)

    def add_object_category(self, category_id):
        self.__metadata.object_categories.add(category_id)

    def del_object_category(self, category_id):
        self.__metadata.object_categories.remove(category_id)

    def get_meta_rules(self):
        return set(self.__metadata.meta_rules)

    def add_meta_rules(self, rule):
        #TODO to be defined
        self.__metadata.meta_rules.add(rule)

    def del_meta_rules(self, rule_id):
        #TODO to be defined
        self.__metadata.meta_rules.remove(rule_id)

    def get_subject_category_values(self, category_id):
        return set(self.__configuration.subject_category_values[category_id])

    def add_subject_category_values(self, category_id, category_value):
        self.__configuration.subject_category_values[category_id].add(category_value)

    def del_subject_category_values(self, category_id, category_value):
        self.__configuration.subject_category_values[category_id].remove(category_value)
        #TODO need to check if the value is not in other tables like assignment

    def get_object_category_values(self, category_id):
        return set(self.__configuration.object_category_values[category_id])

    def add_object_category_values(self, category_id, category_value):
        self.__configuration.object_category_values[category_id].add(category_value)

    def del_object_category_values(self, category_id, category_value):
        self.__configuration.object_category_values[category_id].remove(category_value)
        #TODO need to check if the value is not in other tables like assignment

    def get_subject_assignments(self, category_id):
        return dict(self.__assignment.subject_category_assignments[category_id])

    def add_subject_assignment(self, category_id, subject_id, category_value):
        self.__assignment.subject_category_assignments[category_id][subject_id].add(category_value)

    def del_subject_assignment(self, category_id, subject_id, category_value):
        self.__assignment.subject_category_assignments[category_id][subject_id].remove(category_value)

    def get_object_assignments(self, category_id):
        return dict(self.__assignment.object_category_assignments[category_id])

    def add_object_assignment(self, category_id, object_id, category_value):
        self.__assignment.object_category_assignments[category_id][object_id].add(category_value)

    def del_object_assignment(self, category_id, object_id, category_value):
        self.__assignment.object_category_assignments[category_id][object_id].remove(category_value)

    def get_rules(self):
        return list(self.__configuration.rules)

    def add_rule(self, name, subject_attrs, object_attrs, description=""):
        self.__configuration.rules.append({
            "uuid": str(uuid4()),
            "name": name,
            "subject_attrs": subject_attrs,
            "object_attrs": object_attrs,
            "description": description
        })

    def del_rule(self, rule_id):
        for rule in self.__configuration.rules:
            if rule["uuid"] == rule_id:
                self.__configuration.rules.remove(rule)


class IntraExtension(object):

>>>>>>> dev
    def __init__(
            self,
            name="",
            uuid=None,
            subjects=None,
            objects=None,
            metadata=None,
            rules=None,
            profiles=None,
            description="",
            tenant=None,
            model="RBAC",
            protocol=None,
            administration=None):
        self.__name = name
<<<<<<< HEAD
        self.__uuid = tenant["uuid"]
        # if not uuid:
        #     self.__uuid = str(uuid4()).replace("-", "")
        # else:
        #     self.__uuid = str(uuid).replace("-", "")
=======
        if not uuid:
            self.__uuid = tenant["uuid"]
        else:
            self.__uuid = uuid
>>>>>>> dev
        # self.__subjects = subjects
        # self.__objects = objects
        # self.__metadata = metadata
        # self.__rules = rules
        # self.__objectsAttributes = profiles["o_attr"]
        # self.__subjectsAttributes = profiles["s_attr"]
        # self.__objectsAssignments = profiles["o_attr_assign"]
        # self.__subjectsAssignments = profiles["s_attr_assign"]
<<<<<<< HEAD
        # self.__description = description
        # self.__tenant = tenant
        # self.__model = model
        # self.__protocol = protocol
        # self.__administration = administration
=======
        self.__description = description
        # self.__tenant = tenant
        self.__model = model
        self.__protocol = protocol
        self.__administration = administration
>>>>>>> dev
        self.__dispatcher = get_dispatcher()
        self.authz_extension = AuthzExtension()
        self.admin_extension = AdminExtension()

    def get_uuid(self):
        return self.__uuid

    def get_name(self):
        return self.__name

<<<<<<< HEAD
    def get_tenant(self):
        return self.__tenant

    def get_subjects(self, uuid="", name=""):
        """Return all or a specific subject

        :param uuid: uuid of the subject
        :param name: name of the subject
        :return: a list of dictionary or a dictionary matching a subject
        """
        for sbj in self.__subjects:
            if not sbj["enabled"]:
                continue
            if sbj["uuid"] == uuid or sbj["name"] == name:
                yield sbj
            if not uuid and not name:
                yield sbj

    def add_subject(self, name, uuid="", description="", domain="Default", enabled=True, project=None, mail=""):
        """Add a subject

        :param name: (str) name of the subject
        :param uuid: (str) uuid for this subject (uuid is created if none or empty)
        :param description: (str) description
        :param domain: (str) domain of belonging
        :param enabled: (boolean) true if user is enabled in the system
        :param project: (str) main tenant of the subject
        :param mail: (str) mail address of the subject
        :return: (dict) a dictionary matching the new subject
        """
        try:
            self.get_subjects(name=name).next()
            raise DuplicateSubjectException("Subject {} already exists".format(name))
        except StopIteration:
            pass
        sbj = dict()
        if uuid:
            sbj["uuid"] = uuid
        else:
            sbj["uuid"] = str(uuid4()).replace("-", "")
        sbj["name"] = name
        sbj["description"] = description
        sbj["domain"] = domain
        sbj["enabled"] = enabled
        sbj["project"] = project
        sbj["mail"] = mail
        self.__subjects.append(sbj)
        self.sync()

    def del_subject(self, uuid):
        """Delete a subject

        :param uuid: (str) uuid of the subject
        :return: None
        """
        for sbj in self.__subjects:
            if sbj["uuid"] == uuid:
                self.__subjects.remove(sbj)
                self.sync()
                return
        raise SubjectNotFoundException("Subject {} not found".format(uuid))

    def set_subject(self, uuid, name="", description="", domain="", enabled=True, project=None, mail=""):
        """ Modify a subject

        :param uuid: (str) uuid of the subject
        :param name: (str) name of the subject
        :param description: (str) description
        :param domain: (str) domain
        :param enabled: (boolean) true if user is enabled in the system
        :param project: (str) main tenant of the subject
        :param mail: (str) mail address of the subject
        :return: (dict) a dictionary matching the updated subject
        """
        for sbj in self.__subjects:
            if sbj["uuid"] == uuid:
                if name:
                    sbj["name"] = name
                if description:
                    sbj["description"] = description
                if domain:
                    sbj["domain"] = domain
                if enabled:
                    sbj["enabled"] = enabled
                if project:
                    sbj["project"] = project
                if mail:
                    sbj["mail"] = mail
                self.sync()
                return
        raise SubjectNotFoundException("Subject {} not found".format(uuid))

    def get_objects(self, uuid="", name=""):
        """Return all or a specific object

        :param uuid: uuid of the object
        :param name: name of the object
        :return: a list of dictionary or a dictionary matching an object
        """
        for obj in self.__objects:
            if not obj["enabled"]:
                continue
            if obj["uuid"] == uuid or obj["name"] == name:
                yield obj
            if not uuid and not name:
                yield obj

    def add_object(self, name, uuid="", enabled=True, description="", project=None):
        """Add an object

        :param uuid: (str) uuid of the object
        :param name: (str) name of the object
        :param description: (str) description
        :param enabled: (boolean) true if user is enabled in the system
        :param project: (str) main tenant of the subject
        :return: (dict) a dictionary matching the updated object
        """
        try:
            self.get_objects(name=name).next()
            raise DuplicateObjectException("Object {} already exists".format(name))
        except StopIteration:
            pass
        obj = dict()
        if uuid:
            obj["uuid"] = uuid
        else:
            obj["uuid"] = str(uuid4()).replace("-", "")
        obj["name"] = name
        obj["description"] = description
        obj["enabled"] = enabled
        obj["project"] = project
        self.__objects.append(obj)
        self.sync()

    def del_object(self, uuid):
        """Delete an object

        :param uuid: (str) uuid of the object
        :return: None
        """
        for obj in self.__objects:
            if obj["uuid"] == uuid:
                self.__objects.remove(obj)
                self.sync()
                return
        raise ObjectNotFoundException("Object {} not found".format(uuid))

    def set_object(self, uuid, name="", enabled=True, description="", project=None):
        """ Modify an object

        :param uuid: (str) uuid of the object
        :param name: (str) name of the object
        :param description: (str) description
        :param enabled: (boolean) true if user is enabled in the system
        :param project: (str) main tenant of the subject
        :return: (dict) a dictionary matching the updated user
        """
        for sbj in self.__subjects:
            if sbj["uuid"] == uuid:
                if name:
                    sbj["name"] = name
                if description:
                    sbj["description"] = description
                if enabled:
                    sbj["enabled"] = enabled
                if project:
                    sbj["project"] = project
                self.sync()
                return
        raise ObjectNotFoundException("Object {} not found".format(uuid))

    def get_subject_attribute_categories(self):
        """ Return all categories for subjects

        :return: (list) list of all subject categories available in this extension
        """
        return self.__metadata["subject"]

    def add_subject_attribute_categories(self, name):
        """ Return all categories for subjects

        :return: (str) the name of the new category
        """
        self.__metadata["subject"].append(name)
        return name

    def del_subject_attribute_categories(self, name):
        """ delete one category in subject metadata

        :param name: (str) name of the category to delete
        :return: None
        """
        self.__metadata["subject"].remove(name)

    def get_object_attribute_categories(self):
        """ Return all categories for objects

        :return: (list) list of all object categories available in this extension
        """
        return self.__metadata["object"]

    def add_object_attribute_categories(self, name):
        """Add an object category

        :param name: (str) name of the category
        :return: (str) name of the category
        """
        self.__metadata["object"].append(name)
        return name

    def del_object_attribute_categories(self, name):
        """ delete one category in object metadata

        :param name: (str) name of the category to delete
        :return: None
        """
        self.__metadata["object"].remove(name)

    def get_subject_attributes(self, uuid=None, value=None, category=None):
        """Return all or one specific subject attributes

        :param uuid: (str) uuid of the searched attribute
        :param value: (str) value of the searched attribute
        :param category: (str) category of the searched attribute
        :return: a list of dict with value and category
        """
        for attr in self.__subjectsAttributes:
            if category and attr["category"] != category:
                continue
            if uuid and attr["uuid"] == uuid:
                yield attr
            if value and type(attr["value"]) in (list, tuple) and value in attr["value"]:
                yield attr
            if value and type(attr["value"]) in (str, unicode) and value == attr["value"]:
                yield attr
            if not uuid and not value:
                yield attr

    def add_subject_attributes(self, value, category, uuid=None, description=""):
        """Add a new subject attributes

        :param value: (str or list) name(s) of the new attribute
        :param uuid: (str) uuid (computed if none or empty)
        :param category: (str) category value for that attributes
        :param description: (str) description
        :return: (dict) a dict of the new attributes
        """
        if category not in self.get_subject_attribute_categories():
            return None
        try:
            self.get_subject_attributes(value=value, category=category).next()
            raise DuplicateSubjectAttributeException("Subject attribute {} already exists".format(value))
        except StopIteration:
            pass
        attr = dict()
        if uuid:
            attr["uuid"] = uuid
        else:
            attr["uuid"] = str(uuid4()).replace("-", "")
        attr["value"] = value
        attr["category"] = category
        attr["description"] = description
        self.__subjectsAttributes.append(attr)
        self.sync()
        return attr

    def del_subject_attributes(self, uuid):
        """Delete a subject attribute

        :param uuid: (str) uuid of the attribute to delete
        :return: None
        """
        for attr in self.__subjectsAttributes:
            if attr["uuid"] == uuid:
                self.__subjectsAttributes.remove(attr)
                self.sync()
                return
        raise SubjectAttributeNotFoundException("Subject attribute {} not found".format(uuid))

    def set_subject_attributes(self, uuid, value=None, category=None, description=""):
        """Modify a subject attributes

        :param uuid: (str) uuid of the attribute
        :param value: (str or list) value
        :param category: (str) category
        :param description: (str) description
        :return: (dict) a dict of the updated attributes
        """
        for attr in self.__subjectsAttributes:
            if attr["uuid"] == uuid:
                if value:
                    attr["value"] = value
                if category:
                    attr["category"] = category
                if description:
                    attr["description"] = description
                self.sync()
                return attr
        raise SubjectAttributeNotFoundException("Subject attribute {} not found".format(uuid))

    def get_object_attributes(self, uuid=None, value=None, category=None):
        """Return all or one specific object attributes

        :param uuid: (str) uuid of the searched attribute
        :param value: (str) value of the searched attribute
        :param category: (str) category of the searched attribute
        :return: a list of dict with value and category
        """
        for attr in self.__objectsAttributes:
            if category and attr["category"] != category:
                continue
            if uuid and attr["uuid"] == uuid:
                yield attr
            if value and type(attr["value"]) in (list, tuple) and value in attr["value"]:
                yield attr
            if value and type(attr["value"]) in (str, unicode) and value == attr["value"]:
                yield attr
            if not uuid and not value:
                yield attr

    def add_object_attributes(self, value, category, uuid=None, description=""):
        """Add a new object attributes

        :param value: (str or list) name(s) of the new attribute
        :param uuid: (str) uuid (computed if none or empty)
        :param category: (str) category value for that attributes
        :param description: (str) description
        :return: (dict) a dict of the new attributes
        """
        if category not in self.get_object_attribute_categories():
            return None
        try:
            self.get_object_attributes(value=value, category=category).next()
            raise DuplicateObjectAttributeException("Object attribute {} not found".format(uuid))
        except StopIteration:
            pass
        attr = dict()
        if uuid:
            attr["uuid"] = uuid
        else:
            attr["uuid"] = str(uuid4()).replace("-", "")
        attr["value"] = value
        attr["category"] = category
        attr["description"] = description
        self.__objectsAttributes.append(attr)
        self.sync()
        return attr

    def del_object_attributes(self, uuid):
        """Delete an object attribute

        :param uuid: (str) uuid of the attribute to delete
        :return: None
        """
        for attr in self.__subjectsAttributes:
            if attr["uuid"] == uuid:
                self.__subjectsAttributes.remove(attr)
                self.sync()
                return
        raise SubjectAttributeNotFoundException("Subject attribute {} not found".format(uuid))

    def set_object_attributes(self, uuid, value="", category=None, description=""):
        """Modify an object attribute

        :param uuid: (str) uuid of the attribute
        :param value: (str or list) value
        :param category: (str) category
        :param description: (str) description
        :return: (dict) a dict of the updated attributes
        """
        for attr in self.__objectsAttributes:
            if attr["uuid"] == uuid:
                if value:
                    attr["value"] = value
                if category:
                    attr["category"] = category
                if description:
                    attr["description"] = description
                self.sync()
                return attr
        raise ObjectAttributeNotFoundException("Subject attribute {} not found".format(uuid))

    def get_subject_attribute_assignments(self, uuid=None, subject_name=None, category=None):
        """Return all or one specific object attributes assignment

        :param uuid: (str) uuid of the searched assignment
        :param subject_name: (str) value of the searched assignment
        :param category: (str) filter the returned attributes with this category
        :return: a list of dict containing assignments
        """
        for attr in self.__subjectsAssignments:
            if (uuid and attr["uuid"] == uuid) or\
                    (subject_name and
                        category and
                        type(attr["subject"]) in (list, tuple) and
                        subject_name in attr["subject"] and
                        category == attr["category"]) or\
                    (subject_name and
                        category and
                        type(attr["subject"]) in (str, unicode) and
                        subject_name == attr["subject"] and
                        category == attr["category"]):
                yield attr
            elif not uuid and not subject_name and not category:
                yield attr

    def add_subject_attribute_assignments(self, subject_name, category, uuid=None, attributes=None):
        """Add a new object attributes

        :param subject_name: (str or list) name(s) of the new attribute
        :param uuid: (str) uuid (computed if none or empty)
        :param category: (str) the attributes in this assignment must have this category
        :param attributes: (str or list) list of assigned attributes
                            if a duplicate assignments is detected, attributes will be added
        :return: (dict) a dict of the new assignment
        """
        try:
            assign = self.get_subject_attribute_assignments(subject_name=subject_name, category=category).next()
        except StopIteration:
            attr = dict()
            if uuid:
                attr["uuid"] = uuid
            else:
                attr["uuid"] = str(uuid4()).replace("-", "")
            attr["subject"] = subject_name
            attr["category"] = category
            attr["attributes"] = []
            if type(attributes) not in (list, tuple):
                attributes = (attributes,)
            for _attr in attributes:
                if category and self.get_subject_attributes(uuid=_attr).next()["category"] == category:
                    if type(_attr) is dict and "uuid" in _attr:
                        _attr = _attr["uuid"]
                    attr["attributes"].append(_attr)
                else:
                    logger.warning("Attribute {} is not part of category {}".format(_attr, category))
                    #must never pass here (in theory...)
            attr["attributes"] = attributes
            self.__subjectsAssignments.append(attr)
            self.sync()
            return attr
        else:
            attributes = assign["attributes"]
            if attributes not in (list, tuple):
                attributes = (attributes,)
            for _attr in attributes:
                if category and self.get_subject_attributes(uuid=_attr).next()["category"] == category:
                    if _attr not in assign["attributes"]:
                        if type(_attr) is dict and "uuid" in _attr:
                            _attr = _attr["uuid"]
                        assign["attributes"].append(_attr)
                else:
                    logger.warning("Attribute {} is not part of category {}".format(_attr, category))
                    #must never pass here (in theory...)
            self.sync()
            return assign

    def del_subject_attribute_assignments(self, uuid=None, subject_name=None, category=None):
        """Delete a subject attribute assignment

        :param uuid: (str) uuid of the attribute to delete
        :param subject_name: (str) subject to delete (category and subject_name must be set together)
        :param category: (str) category to delete (category and subject_name must be set together)
        :return: None
        """
        for attr in self.__subjectsAttributes:
            if (attr["uuid"] == uuid) or\
                    (subject_name and category and attr["subject"] == subject_name and attr["category"] == category):
                self.__subjectsAttributes.remove(attr)
                self.sync()
                return
        raise SubjectAssignmentNotFoundException("Subject assignment {}/{} not found".format(uuid, subject_name))

    def set_subject_attribute_assignments(self, uuid=None, subject_name=None, category=None, attributes=None):
        """Modify a subject assignment

        :param uuid: (str) uuid of the attribute
        :param subject_name: (str) value
        :param category: (str) category
        :param attributes: (list) list of new attributes (warning previous attributes will be erased)
        :return: (dict) a dict of the updated assignment
        """
        for attr in self.__subjectsAssignments:
            if (attr["uuid"] == uuid) or\
                    (attr["subject"] == subject_name and attr["category"] == category):
                if subject_name:
                    attr["subject"] = subject_name
                if category:
                    attr["category"] = category
                if attributes:
                    attr["attributes"] = attributes
                self.sync()
                return attr
        raise SubjectAssignmentNotFoundException("Subject assignment {}/{} not found".format(uuid, subject_name))

    def get_object_attribute_assignments(self, uuid=None, object_name=None, category=None):
        """Return all object attributes assignment for a specific object

        :param uuid: (str) uuid of the searched assignment
        :param object_name: (str) value of the searched assignment
        :param category: (str) filter the returned attributes with this category
        :return: a list of dict containing assignments
        """
        for attr in self.__objectsAssignments:
            if (uuid and attr["uuid"] == uuid) or\
                    (object_name and
                        category and
                        type(attr["object"]) in (list, tuple) and
                        object_name in attr["object"] and
                        category == attr["category"]) or\
                    (object_name and
                        category and
                        type(attr["object"]) in (str, unicode) and
                        object_name == attr["object"] and
                        category == attr["category"]):
                yield attr

    def add_object_attribute_assignments(self, uuid=None, object_name=None, category=None, attributes=None):
        """Add a new object attributes

        :param object_name: (str or list) name(s) of the new attribute
        :param uuid: (str) uuid (computed if none or empty)
        :param category: (str) the attributes in this assignment must have this category
        :param attributes: (str or list) list of assigned attributes
                            if a duplicate assignments is detected, attributes will be added
        :return: (dict) a dict of the new assignment
        """
        try:
            assign = self.get_object_attribute_assignments(object_name=object_name, category=category).next()
        except StopIteration:
            attr = dict()
            if uuid:
                attr["uuid"] = uuid
            else:
                attr["uuid"] = str(uuid4()).replace("-", "")
            attr["object"] = object_name
            attr["category"] = category
            attr["attributes"] = []
            if type(attributes) not in (list, tuple):
                attributes = (attributes,)
            for _attr in attributes:
                if category and self.get_object_attributes(uuid=_attr).next()["category"] == category:
                    if type(_attr) is dict and "uuid" in _attr:
                        _attr = _attr["uuid"]
                    attr["attributes"].append(_attr)
                else:
                    logger.warning("Attribute {} is not part of category {}".format(_attr, category))
                    #must never pas here (in theory...)
            self.__objectsAssignments.append(attr)
            self.sync()
            return attr
        else:
            attributes = assign["attributes"]
            if type(attributes) not in (list, tuple):
                attributes = (attributes,)
            for _attr in attributes:
                if category and self.get_object_attributes(uuid=_attr).next()["category"] == category:
                    if _attr not in assign["attributes"]:
                        if type(_attr) is dict and "uuid" in _attr:
                            _attr = _attr["uuid"]
                        assign["attributes"].append(_attr)
                else:
                    logger.warning("Attribute {} is not part of category {}".format(_attr, category))
                    #must never pass here (in theory...)
            self.sync()
            return assign

    def del_object_attribute_assignments(self, uuid=None, object_name=None, category=None):
        """Delete an object attribute assignment

        :param uuid: (str) uuid of the attribute to delete
        :param object_name: (str) object to delete (category and object_name must be set together)
        :param category: (str) category to delete (category and object_name must be set together)
        :return: None
        """
        for attr in self.__objectsAttributes:
            if (attr["uuid"] == uuid) or\
                    (object_name and category and attr["object"] == object_name and attr["category"] == category):
                self.__subjectsAttributes.remove(attr)
                self.sync()
                return
        raise ObjectAssignmentNotFoundException("Object assignment {}/{} not found".format(uuid, object_name))

    def set_object_attribute_assignments(self, uuid=None, object_name=None, category=None, attributes=None):
        """Modify an object assignment

        :param uuid: (str) uuid of the attribute
        :param object_name: (str) value
        :param category: (str) category
        :param attributes: (list) list of new attributes (warning previous attributes will be erased)
        :return: (dict) a dict of the updated assignment
        """
        for attr in self.__subjectsAssignments:
            if (attr["uuid"] == uuid) or\
                    (attr["object"] == object_name and attr["category"] == category):
                if object_name:
                    attr["object"] = object_name
                if category:
                    attr["category"] = category
                if attributes:
                    attr["attributes"] = attributes
                self.sync()
                return attr
        raise ObjectAssignmentNotFoundException("Object assignment {}/{} not found".format(uuid, object_name))

    def get_rules(self):
        """ Return all the rules

        :return: a list of dict
        """
        return self.__rules

    def add_rule(self, name, subject_attrs, object_attrs, description=""):
        """Add a new rule in this extension
        :param name: (str) name of the rule
        :param subject_attrs: (list) list of subject attributes to be added
        :param object_attrs: (list) list of object attributes to be added
        :param description: (str) short description of the rule
        :return: (dict) a dict of the new rule

        The new rule must be formed like this:
        {
            "name": "the name of the rule",
            "description": "a short description",
            "s_rule": [
                {u'category': u'role', u'value': u'admin'},
            ],
            "o_rule": [
                {u'category': u'type', u'value': u'server'},
                {u'category': u'action', u'value': u'get.os-start'},
            ],
        }
        """
        rule = dict()
        rule["uuid"] = str(uuid4()).replace("-", "")
        rule["name"] = name
        rule["description"] = description
        rule["s_rules"] = list()
        rule["o_rules"] = list()
        s_cat = self.get_subject_attribute_categories()
        o_cat = self.get_object_attribute_categories()
        for s_attr in subject_attrs:
            if s_attr["category"] in s_cat:
                rule["s_rules"].append(s_attr)
        for o_attr in object_attrs:
            if o_attr["category"] in o_cat:
                rule["o_rules"].append(o_attr)
        self.__rules.append(rule)
        self.sync()
        return rule

    def set_rule(self, uuid, name="", subject_attrs=None, object_attrs=None, description=""):
        """Modify a specific rule

        :param uuid: (str) uuid of the rule to be changed
        :param name: (str) name of the rule
        :param subject_attrs: (list) list of subject attributes to be added
        :param object_attrs: (list) list of object attributes to be added
        :param description: (str) short description of the rule
        :return: (dict) a dict of the new rule
        """
        for rule in self.__rules:
            if rule["uuid"] == uuid:
                if name:
                    rule["name"] = name
                if description:
                    rule["description"] = description
                if subject_attrs:
                    rule["s_rules"] = list()
                    s_cat = self.get_subject_attribute_categories()
                    for s_attr in subject_attrs:
                        if s_attr["category"] in s_cat:
                            rule["s_rules"].append(s_attr)
                if object_attrs:
                    rule["o_rules"] = list()
                    o_cat = self.get_object_attribute_categories()
                    for o_attr in object_attrs:
                        if o_attr["category"] in o_cat:
                            rule["o_rules"].append(o_attr)
                self.sync()
                return rule
        raise RuleNotFoundException("rule {} not found".format(uuid))

    def del_rule(self, uuid):
        """Delete a rule

        :param uuid: (str) uuid to delete
        :return: None
        """
        for rule in self.__rules:
            if rule["uuid"] == uuid:
                self.__rules.remove(rule)
                return
        raise RuleNotFoundException("rule {} not found".format(uuid))

    def __has_admin_assignment(
            self,
            object_uuid=None,
            attribute_uuid=None
        ):
        if object_uuid == "*":
            return True
        data = self.__administration["assignments"]
        for obj in data:
            if type(attribute_uuid) not in (list, tuple):
                attribute_uuid = [attribute_uuid, ]
            for att in attribute_uuid:
                if object_uuid == obj["object"] and att in obj["attributes"]:
                    return True
        return False

    def authz(self, auth):
        if "objects" not in self.__administration:
            auth["message"] = "No administration protocol for extension"
            auth["auth"] = True
            return auth
        if self.__tenant["name"] != auth["tenant_name"]:
            auth["message"] = "Tenant not found."
            return auth
        if auth["subject"] not in map(lambda x: x["uuid"], self.__subjects):
            auth["message"] = "User not found."
            return auth
        if auth["object_name"] not in map(lambda x: x["name"], self.__administration["objects"]):
            auth["message"] = "Object not found."
            return auth
        for obj in self.__administration["objects"]:
            if obj["name"] == auth["object_name"]:
                auth["object_uuid"] = obj["uuid"]
                break
        for rule in self.__administration["rules"]:
            _auth = False
            for s_rule in rule["s_attr"]:
                data = self.__subjectsAssignments
                attribute = s_rule["value"]
                for sbj in data:
                    if type(attribute) not in (list, tuple):
                        attribute = [attribute, ]
                    for att in attribute:
                        if auth["subject"] == sbj["subject"] and att in sbj["attributes"]:
                            _auth = True
                            break
            if not _auth:
                auth["message"] = "Rules on subject don't match."
                continue
            for o_rule in rule["o_attr"]:
                    if o_rule["category"] == "action":
                        _auth = self.__has_admin_assignment(
                            object_uuid=auth["object_uuid"],
                            attribute_uuid=auth["action"])
                        if not _auth:
                            auth["message"] = "Rules on action assignments don't match."
                            break
                        if auth["action"] not in o_rule["value"]:
                            auth["message"] = "Rules on action don't match."
                            break
                    else:
                        _auth = self.__has_admin_assignment(
                            object_uuid=auth["object_uuid"],
                            attribute_uuid=o_rule["value"])
                        if not _auth:
                            auth["message"] = "Rules on object don't match."
                            print(auth["object_uuid"], o_rule["value"])
                            break
            else:
                auth["message"] = ""
                auth["auth"] = True
                break
        return auth

    def sync(self):
        profiles = dict()
        profiles["o_attr"] = self.__objectsAttributes
        profiles["s_attr"] = self.__subjectsAttributes
        profiles["o_attr_assign"] = self.__objectsAssignments
        profiles["s_attr_assign"] = self.__subjectsAssignments
        self.__dispatcher.new_extension(
            uuid=self.__uuid,
            name=self.__name,
            subjects=self.__subjects,
            objects=self.__objects,
            metadata=self.__metadata,
            rules=self.__rules,
            profiles=profiles,
            description=self.__description,
            tenant=self.__tenant,
=======
    def sync(self):
        profiles = dict()
        profiles["o_attr"] = self.authz_extension.get_object_categories()
        profiles["s_attr"] = self.authz_extension.get_subject_categories()
        profiles["s_attr_assign"] = dict()
        for cat in self.authz_extension.get_subject_categories():
            profiles["s_attr_assign"][cat] = self.authz_extension.get_subject_assignments(cat)
        profiles["o_attr_assign"] = dict()
        for cat in self.authz_extension.get_object_categories():
            profiles["o_attr_assign"][cat] = self.authz_extension.get_object_assignments(cat)
        metadata = dict()
        metadata["subject_category"] = dict()
        for cat in self.authz_extension.get_subject_categories():
            metadata["subject_category"][cat] = self.authz_extension.get_subject_category_values(cat)
        metadata["object_category"] = dict()
        for cat in self.authz_extension.get_object_categories():
            metadata["object_category"][cat] = self.authz_extension.get_object_category_values(cat)
        metadata["meta_rules"] = self.authz_extension.get_meta_rules()
        self.__dispatcher.new_extension(
            uuid=self.__uuid,
            name=self.__name,
            subjects=self.authz_extension.get_subjects(),
            objects=self.authz_extension.get_objects(),
            metadata=metadata,
            rules=self.authz_extension.get_rules(),
            profiles=profiles,
            description=self.__description,
>>>>>>> dev
            model=self.__model,
            type="extension",
            protocol=self.__protocol,
            administration=self.__administration
        )

<<<<<<< HEAD
    # @enforce(("tenant", "perimeter.subjects", "perimeter.objects"))
    def html(self):
        return mark_safe("""<b>Extension</b> {} for <b>tenant {}</b><br/><br/>
        <b>Subjects:</b> <ul>{}</ul><br>
        <b>Objects:</b> <ul>{}</ul>
        """.format(
            self.__name,
            self.__tenant["name"],
            "".join(map(lambda x: "<li>"+x["name"]+"</li>", self.__subjects)),
            "".join(map(lambda x: "<li>"+x["name"]+"</li>", self.__objects)),
        ))
=======
    # def get_tenant(self):
    #     return self.__tenant

    # def get_subjects(self, uuid="", name=""):
    #     """Return all or a specific subject
    #
    #     :param uuid: uuid of the subject
    #     :param name: name of the subject
    #     :return: a list of dictionary or a dictionary matching a subject
    #     """
    #     for sbj in self.__subjects:
    #         if not sbj["enabled"]:
    #             continue
    #         if sbj["uuid"] == uuid or sbj["name"] == name:
    #             yield sbj
    #         if not uuid and not name:
    #             yield sbj
    #
    # def add_subject(self, name, uuid="", description="", domain="Default", enabled=True, project=None, mail=""):
    #     """Add a subject
    #
    #     :param name: (str) name of the subject
    #     :param uuid: (str) uuid for this subject (uuid is created if none or empty)
    #     :param description: (str) description
    #     :param domain: (str) domain of belonging
    #     :param enabled: (boolean) true if user is enabled in the system
    #     :param project: (str) main tenant of the subject
    #     :param mail: (str) mail address of the subject
    #     :return: (dict) a dictionary matching the new subject
    #     """
    #     try:
    #         self.get_subjects(name=name).next()
    #         raise DuplicateSubjectException("Subject {} already exists".format(name))
    #     except StopIteration:
    #         pass
    #     sbj = dict()
    #     if uuid:
    #         sbj["uuid"] = uuid
    #     else:
    #         sbj["uuid"] = str(uuid4()).replace("-", "")
    #     sbj["name"] = name
    #     sbj["description"] = description
    #     sbj["domain"] = domain
    #     sbj["enabled"] = enabled
    #     sbj["project"] = project
    #     sbj["mail"] = mail
    #     self.__subjects.append(sbj)
    #     self.sync()
    #
    # def del_subject(self, uuid):
    #     """Delete a subject
    #
    #     :param uuid: (str) uuid of the subject
    #     :return: None
    #     """
    #     for sbj in self.__subjects:
    #         if sbj["uuid"] == uuid:
    #             self.__subjects.remove(sbj)
    #             self.sync()
    #             return
    #     raise SubjectNotFoundException("Subject {} not found".format(uuid))
    #
    # def set_subject(self, uuid, name="", description="", domain="", enabled=True, project=None, mail=""):
    #     """ Modify a subject
    #
    #     :param uuid: (str) uuid of the subject
    #     :param name: (str) name of the subject
    #     :param description: (str) description
    #     :param domain: (str) domain
    #     :param enabled: (boolean) true if user is enabled in the system
    #     :param project: (str) main tenant of the subject
    #     :param mail: (str) mail address of the subject
    #     :return: (dict) a dictionary matching the updated subject
    #     """
    #     for sbj in self.__subjects:
    #         if sbj["uuid"] == uuid:
    #             if name:
    #                 sbj["name"] = name
    #             if description:
    #                 sbj["description"] = description
    #             if domain:
    #                 sbj["domain"] = domain
    #             if enabled:
    #                 sbj["enabled"] = enabled
    #             if project:
    #                 sbj["project"] = project
    #             if mail:
    #                 sbj["mail"] = mail
    #             self.sync()
    #             return
    #     raise SubjectNotFoundException("Subject {} not found".format(uuid))
    #
    # def get_objects(self, uuid="", name=""):
    #     """Return all or a specific object
    #
    #     :param uuid: uuid of the object
    #     :param name: name of the object
    #     :return: a list of dictionary or a dictionary matching an object
    #     """
    #     for obj in self.__objects:
    #         if not obj["enabled"]:
    #             continue
    #         if obj["uuid"] == uuid or obj["name"] == name:
    #             yield obj
    #         if not uuid and not name:
    #             yield obj
    #
    # def add_object(self, name, uuid="", enabled=True, description="", project=None):
    #     """Add an object
    #
    #     :param uuid: (str) uuid of the object
    #     :param name: (str) name of the object
    #     :param description: (str) description
    #     :param enabled: (boolean) true if user is enabled in the system
    #     :param project: (str) main tenant of the subject
    #     :return: (dict) a dictionary matching the updated object
    #     """
    #     try:
    #         self.get_objects(name=name).next()
    #         raise DuplicateObjectException("Object {} already exists".format(name))
    #     except StopIteration:
    #         pass
    #     obj = dict()
    #     if uuid:
    #         obj["uuid"] = uuid
    #     else:
    #         obj["uuid"] = str(uuid4()).replace("-", "")
    #     obj["name"] = name
    #     obj["description"] = description
    #     obj["enabled"] = enabled
    #     obj["project"] = project
    #     self.__objects.append(obj)
    #     self.sync()
    #
    # def del_object(self, uuid):
    #     """Delete an object
    #
    #     :param uuid: (str) uuid of the object
    #     :return: None
    #     """
    #     for obj in self.__objects:
    #         if obj["uuid"] == uuid:
    #             self.__objects.remove(obj)
    #             self.sync()
    #             return
    #     raise ObjectNotFoundException("Object {} not found".format(uuid))
    #
    # def set_object(self, uuid, name="", enabled=True, description="", project=None):
    #     """ Modify an object
    #
    #     :param uuid: (str) uuid of the object
    #     :param name: (str) name of the object
    #     :param description: (str) description
    #     :param enabled: (boolean) true if user is enabled in the system
    #     :param project: (str) main tenant of the subject
    #     :return: (dict) a dictionary matching the updated user
    #     """
    #     for sbj in self.__subjects:
    #         if sbj["uuid"] == uuid:
    #             if name:
    #                 sbj["name"] = name
    #             if description:
    #                 sbj["description"] = description
    #             if enabled:
    #                 sbj["enabled"] = enabled
    #             if project:
    #                 sbj["project"] = project
    #             self.sync()
    #             return
    #     raise ObjectNotFoundException("Object {} not found".format(uuid))
    #
    # def get_subject_attribute_categories(self):
    #     """ Return all categories for subjects
    #
    #     :return: (list) list of all subject categories available in this extension
    #     """
    #     return self.__metadata["subject"]
    #
    # def add_subject_attribute_categories(self, name):
    #     """ Return all categories for subjects
    #
    #     :return: (str) the name of the new category
    #     """
    #     self.__metadata["subject"].append(name)
    #     return name
    #
    # def del_subject_attribute_categories(self, name):
    #     """ delete one category in subject metadata
    #
    #     :param name: (str) name of the category to delete
    #     :return: None
    #     """
    #     self.__metadata["subject"].remove(name)
    #
    # def get_object_attribute_categories(self):
    #     """ Return all categories for objects
    #
    #     :return: (list) list of all object categories available in this extension
    #     """
    #     return self.__metadata["object"]
    #
    # def add_object_attribute_categories(self, name):
    #     """Add an object category
    #
    #     :param name: (str) name of the category
    #     :return: (str) name of the category
    #     """
    #     self.__metadata["object"].append(name)
    #     return name
    #
    # def del_object_attribute_categories(self, name):
    #     """ delete one category in object metadata
    #
    #     :param name: (str) name of the category to delete
    #     :return: None
    #     """
    #     self.__metadata["object"].remove(name)
    #
    # def get_subject_attributes(self, uuid=None, value=None, category=None):
    #     """Return all or one specific subject attributes
    #
    #     :param uuid: (str) uuid of the searched attribute
    #     :param value: (str) value of the searched attribute
    #     :param category: (str) category of the searched attribute
    #     :return: a list of dict with value and category
    #     """
    #     for attr in self.__subjectsAttributes:
    #         if category and attr["category"] != category:
    #             continue
    #         if uuid and attr["uuid"] == uuid:
    #             yield attr
    #         if value and type(attr["value"]) in (list, tuple) and value in attr["value"]:
    #             yield attr
    #         if value and type(attr["value"]) in (str, unicode) and value == attr["value"]:
    #             yield attr
    #         if not uuid and not value:
    #             yield attr
    #
    # def add_subject_attributes(self, value, category, uuid=None, description=""):
    #     """Add a new subject attributes
    #
    #     :param value: (str or list) name(s) of the new attribute
    #     :param uuid: (str) uuid (computed if none or empty)
    #     :param category: (str) category value for that attributes
    #     :param description: (str) description
    #     :return: (dict) a dict of the new attributes
    #     """
    #     if category not in self.get_subject_attribute_categories():
    #         return None
    #     try:
    #         self.get_subject_attributes(value=value, category=category).next()
    #         raise DuplicateSubjectAttributeException("Subject attribute {} already exists".format(value))
    #     except StopIteration:
    #         pass
    #     attr = dict()
    #     if uuid:
    #         attr["uuid"] = uuid
    #     else:
    #         attr["uuid"] = str(uuid4()).replace("-", "")
    #     attr["value"] = value
    #     attr["category"] = category
    #     attr["description"] = description
    #     self.__subjectsAttributes.append(attr)
    #     self.sync()
    #     return attr
    #
    # def del_subject_attributes(self, uuid):
    #     """Delete a subject attribute
    #
    #     :param uuid: (str) uuid of the attribute to delete
    #     :return: None
    #     """
    #     for attr in self.__subjectsAttributes:
    #         if attr["uuid"] == uuid:
    #             self.__subjectsAttributes.remove(attr)
    #             self.sync()
    #             return
    #     raise SubjectAttributeNotFoundException("Subject attribute {} not found".format(uuid))
    #
    # def set_subject_attributes(self, uuid, value=None, category=None, description=""):
    #     """Modify a subject attributes
    #
    #     :param uuid: (str) uuid of the attribute
    #     :param value: (str or list) value
    #     :param category: (str) category
    #     :param description: (str) description
    #     :return: (dict) a dict of the updated attributes
    #     """
    #     for attr in self.__subjectsAttributes:
    #         if attr["uuid"] == uuid:
    #             if value:
    #                 attr["value"] = value
    #             if category:
    #                 attr["category"] = category
    #             if description:
    #                 attr["description"] = description
    #             self.sync()
    #             return attr
    #     raise SubjectAttributeNotFoundException("Subject attribute {} not found".format(uuid))
    #
    # def get_object_attributes(self, uuid=None, value=None, category=None):
    #     """Return all or one specific object attributes
    #
    #     :param uuid: (str) uuid of the searched attribute
    #     :param value: (str) value of the searched attribute
    #     :param category: (str) category of the searched attribute
    #     :return: a list of dict with value and category
    #     """
    #     for attr in self.__objectsAttributes:
    #         if category and attr["category"] != category:
    #             continue
    #         if uuid and attr["uuid"] == uuid:
    #             yield attr
    #         if value and type(attr["value"]) in (list, tuple) and value in attr["value"]:
    #             yield attr
    #         if value and type(attr["value"]) in (str, unicode) and value == attr["value"]:
    #             yield attr
    #         if not uuid and not value:
    #             yield attr
    #
    # def add_object_attributes(self, value, category, uuid=None, description=""):
    #     """Add a new object attributes
    #
    #     :param value: (str or list) name(s) of the new attribute
    #     :param uuid: (str) uuid (computed if none or empty)
    #     :param category: (str) category value for that attributes
    #     :param description: (str) description
    #     :return: (dict) a dict of the new attributes
    #     """
    #     if category not in self.get_object_attribute_categories():
    #         return None
    #     try:
    #         self.get_object_attributes(value=value, category=category).next()
    #         raise DuplicateObjectAttributeException("Object attribute {} not found".format(uuid))
    #     except StopIteration:
    #         pass
    #     attr = dict()
    #     if uuid:
    #         attr["uuid"] = uuid
    #     else:
    #         attr["uuid"] = str(uuid4()).replace("-", "")
    #     attr["value"] = value
    #     attr["category"] = category
    #     attr["description"] = description
    #     self.__objectsAttributes.append(attr)
    #     self.sync()
    #     return attr
    #
    # def del_object_attributes(self, uuid):
    #     """Delete an object attribute
    #
    #     :param uuid: (str) uuid of the attribute to delete
    #     :return: None
    #     """
    #     for attr in self.__subjectsAttributes:
    #         if attr["uuid"] == uuid:
    #             self.__subjectsAttributes.remove(attr)
    #             self.sync()
    #             return
    #     raise SubjectAttributeNotFoundException("Subject attribute {} not found".format(uuid))
    #
    # def set_object_attributes(self, uuid, value="", category=None, description=""):
    #     """Modify an object attribute
    #
    #     :param uuid: (str) uuid of the attribute
    #     :param value: (str or list) value
    #     :param category: (str) category
    #     :param description: (str) description
    #     :return: (dict) a dict of the updated attributes
    #     """
    #     for attr in self.__objectsAttributes:
    #         if attr["uuid"] == uuid:
    #             if value:
    #                 attr["value"] = value
    #             if category:
    #                 attr["category"] = category
    #             if description:
    #                 attr["description"] = description
    #             self.sync()
    #             return attr
    #     raise ObjectAttributeNotFoundException("Subject attribute {} not found".format(uuid))
    #
    # def get_subject_attribute_assignments(self, uuid=None, subject_name=None, category=None):
    #     """Return all or one specific object attributes assignment
    #
    #     :param uuid: (str) uuid of the searched assignment
    #     :param subject_name: (str) value of the searched assignment
    #     :param category: (str) filter the returned attributes with this category
    #     :return: a list of dict containing assignments
    #     """
    #     for attr in self.__subjectsAssignments:
    #         if (uuid and attr["uuid"] == uuid) or\
    #                 (subject_name and
    #                     category and
    #                     type(attr["subject"]) in (list, tuple) and
    #                     subject_name in attr["subject"] and
    #                     category == attr["category"]) or\
    #                 (subject_name and
    #                     category and
    #                     type(attr["subject"]) in (str, unicode) and
    #                     subject_name == attr["subject"] and
    #                     category == attr["category"]):
    #             yield attr
    #         elif not uuid and not subject_name and not category:
    #             yield attr
    #
    # def add_subject_attribute_assignments(self, subject_name, category, uuid=None, attributes=None):
    #     """Add a new object attributes
    #
    #     :param subject_name: (str or list) name(s) of the new attribute
    #     :param uuid: (str) uuid (computed if none or empty)
    #     :param category: (str) the attributes in this assignment must have this category
    #     :param attributes: (str or list) list of assigned attributes
    #                         if a duplicate assignments is detected, attributes will be added
    #     :return: (dict) a dict of the new assignment
    #     """
    #     try:
    #         assign = self.get_subject_attribute_assignments(subject_name=subject_name, category=category).next()
    #     except StopIteration:
    #         attr = dict()
    #         if uuid:
    #             attr["uuid"] = uuid
    #         else:
    #             attr["uuid"] = str(uuid4()).replace("-", "")
    #         attr["subject"] = subject_name
    #         attr["category"] = category
    #         attr["attributes"] = []
    #         if type(attributes) not in (list, tuple):
    #             attributes = (attributes,)
    #         for _attr in attributes:
    #             if category and self.get_subject_attributes(uuid=_attr).next()["category"] == category:
    #                 if type(_attr) is dict and "uuid" in _attr:
    #                     _attr = _attr["uuid"]
    #                 attr["attributes"].append(_attr)
    #             else:
    #                 logger.warning("Attribute {} is not part of category {}".format(_attr, category))
    #                 #must never pass here (in theory...)
    #         attr["attributes"] = attributes
    #         self.__subjectsAssignments.append(attr)
    #         self.sync()
    #         return attr
    #     else:
    #         attributes = assign["attributes"]
    #         if attributes not in (list, tuple):
    #             attributes = (attributes,)
    #         for _attr in attributes:
    #             if category and self.get_subject_attributes(uuid=_attr).next()["category"] == category:
    #                 if _attr not in assign["attributes"]:
    #                     if type(_attr) is dict and "uuid" in _attr:
    #                         _attr = _attr["uuid"]
    #                     assign["attributes"].append(_attr)
    #             else:
    #                 logger.warning("Attribute {} is not part of category {}".format(_attr, category))
    #                 #must never pass here (in theory...)
    #         self.sync()
    #         return assign
    #
    # def del_subject_attribute_assignments(self, uuid=None, subject_name=None, category=None):
    #     """Delete a subject attribute assignment
    #
    #     :param uuid: (str) uuid of the attribute to delete
    #     :param subject_name: (str) subject to delete (category and subject_name must be set together)
    #     :param category: (str) category to delete (category and subject_name must be set together)
    #     :return: None
    #     """
    #     for attr in self.__subjectsAttributes:
    #         if (attr["uuid"] == uuid) or\
    #                 (subject_name and category and attr["subject"] == subject_name and attr["category"] == category):
    #             self.__subjectsAttributes.remove(attr)
    #             self.sync()
    #             return
    #     raise SubjectAssignmentNotFoundException("Subject assignment {}/{} not found".format(uuid, subject_name))
    #
    # def set_subject_attribute_assignments(self, uuid=None, subject_name=None, category=None, attributes=None):
    #     """Modify a subject assignment
    #
    #     :param uuid: (str) uuid of the attribute
    #     :param subject_name: (str) value
    #     :param category: (str) category
    #     :param attributes: (list) list of new attributes (warning previous attributes will be erased)
    #     :return: (dict) a dict of the updated assignment
    #     """
    #     for attr in self.__subjectsAssignments:
    #         if (attr["uuid"] == uuid) or\
    #                 (attr["subject"] == subject_name and attr["category"] == category):
    #             if subject_name:
    #                 attr["subject"] = subject_name
    #             if category:
    #                 attr["category"] = category
    #             if attributes:
    #                 attr["attributes"] = attributes
    #             self.sync()
    #             return attr
    #     raise SubjectAssignmentNotFoundException("Subject assignment {}/{} not found".format(uuid, subject_name))
    #
    # def get_object_attribute_assignments(self, uuid=None, object_name=None, category=None):
    #     """Return all object attributes assignment for a specific object
    #
    #     :param uuid: (str) uuid of the searched assignment
    #     :param object_name: (str) value of the searched assignment
    #     :param category: (str) filter the returned attributes with this category
    #     :return: a list of dict containing assignments
    #     """
    #     for attr in self.__objectsAssignments:
    #         if (uuid and attr["uuid"] == uuid) or\
    #                 (object_name and
    #                     category and
    #                     type(attr["object"]) in (list, tuple) and
    #                     object_name in attr["object"] and
    #                     category == attr["category"]) or\
    #                 (object_name and
    #                     category and
    #                     type(attr["object"]) in (str, unicode) and
    #                     object_name == attr["object"] and
    #                     category == attr["category"]):
    #             yield attr
    #
    # def add_object_attribute_assignments(self, uuid=None, object_name=None, category=None, attributes=None):
    #     """Add a new object attributes
    #
    #     :param object_name: (str or list) name(s) of the new attribute
    #     :param uuid: (str) uuid (computed if none or empty)
    #     :param category: (str) the attributes in this assignment must have this category
    #     :param attributes: (str or list) list of assigned attributes
    #                         if a duplicate assignments is detected, attributes will be added
    #     :return: (dict) a dict of the new assignment
    #     """
    #     try:
    #         assign = self.get_object_attribute_assignments(object_name=object_name, category=category).next()
    #     except StopIteration:
    #         attr = dict()
    #         if uuid:
    #             attr["uuid"] = uuid
    #         else:
    #             attr["uuid"] = str(uuid4()).replace("-", "")
    #         attr["object"] = object_name
    #         attr["category"] = category
    #         attr["attributes"] = []
    #         if type(attributes) not in (list, tuple):
    #             attributes = (attributes,)
    #         for _attr in attributes:
    #             if category and self.get_object_attributes(uuid=_attr).next()["category"] == category:
    #                 if type(_attr) is dict and "uuid" in _attr:
    #                     _attr = _attr["uuid"]
    #                 attr["attributes"].append(_attr)
    #             else:
    #                 logger.warning("Attribute {} is not part of category {}".format(_attr, category))
    #                 #must never pas here (in theory...)
    #         self.__objectsAssignments.append(attr)
    #         self.sync()
    #         return attr
    #     else:
    #         attributes = assign["attributes"]
    #         if type(attributes) not in (list, tuple):
    #             attributes = (attributes,)
    #         for _attr in attributes:
    #             if category and self.get_object_attributes(uuid=_attr).next()["category"] == category:
    #                 if _attr not in assign["attributes"]:
    #                     if type(_attr) is dict and "uuid" in _attr:
    #                         _attr = _attr["uuid"]
    #                     assign["attributes"].append(_attr)
    #             else:
    #                 logger.warning("Attribute {} is not part of category {}".format(_attr, category))
    #                 #must never pass here (in theory...)
    #         self.sync()
    #         return assign
    #
    # def del_object_attribute_assignments(self, uuid=None, object_name=None, category=None):
    #     """Delete an object attribute assignment
    #
    #     :param uuid: (str) uuid of the attribute to delete
    #     :param object_name: (str) object to delete (category and object_name must be set together)
    #     :param category: (str) category to delete (category and object_name must be set together)
    #     :return: None
    #     """
    #     for attr in self.__objectsAttributes:
    #         if (attr["uuid"] == uuid) or\
    #                 (object_name and category and attr["object"] == object_name and attr["category"] == category):
    #             self.__subjectsAttributes.remove(attr)
    #             self.sync()
    #             return
    #     raise ObjectAssignmentNotFoundException("Object assignment {}/{} not found".format(uuid, object_name))
    #
    # def set_object_attribute_assignments(self, uuid=None, object_name=None, category=None, attributes=None):
    #     """Modify an object assignment
    #
    #     :param uuid: (str) uuid of the attribute
    #     :param object_name: (str) value
    #     :param category: (str) category
    #     :param attributes: (list) list of new attributes (warning previous attributes will be erased)
    #     :return: (dict) a dict of the updated assignment
    #     """
    #     for attr in self.__subjectsAssignments:
    #         if (attr["uuid"] == uuid) or\
    #                 (attr["object"] == object_name and attr["category"] == category):
    #             if object_name:
    #                 attr["object"] = object_name
    #             if category:
    #                 attr["category"] = category
    #             if attributes:
    #                 attr["attributes"] = attributes
    #             self.sync()
    #             return attr
    #     raise ObjectAssignmentNotFoundException("Object assignment {}/{} not found".format(uuid, object_name))
    #
    # def get_rules(self):
    #     """ Return all the rules
    #
    #     :return: a list of dict
    #     """
    #     return self.__rules
    #
    # def add_rule(self, name, subject_attrs, object_attrs, description=""):
    #     """Add a new rule in this extension
    #     :param name: (str) name of the rule
    #     :param subject_attrs: (list) list of subject attributes to be added
    #     :param object_attrs: (list) list of object attributes to be added
    #     :param description: (str) short description of the rule
    #     :return: (dict) a dict of the new rule
    #
    #     The new rule must be formed like this:
    #     {
    #         "name": "the name of the rule",
    #         "description": "a short description",
    #         "s_rule": [
    #             {u'category': u'role', u'value': u'admin'},
    #         ],
    #         "o_rule": [
    #             {u'category': u'type', u'value': u'server'},
    #             {u'category': u'action', u'value': u'get.os-start'},
    #         ],
    #     }
    #     """
    #     rule = dict()
    #     rule["uuid"] = str(uuid4()).replace("-", "")
    #     rule["name"] = name
    #     rule["description"] = description
    #     rule["s_rules"] = list()
    #     rule["o_rules"] = list()
    #     s_cat = self.get_subject_attribute_categories()
    #     o_cat = self.get_object_attribute_categories()
    #     for s_attr in subject_attrs:
    #         if s_attr["category"] in s_cat:
    #             rule["s_rules"].append(s_attr)
    #     for o_attr in object_attrs:
    #         if o_attr["category"] in o_cat:
    #             rule["o_rules"].append(o_attr)
    #     self.__rules.append(rule)
    #     self.sync()
    #     return rule
    #
    # def set_rule(self, uuid, name="", subject_attrs=None, object_attrs=None, description=""):
    #     """Modify a specific rule
    #
    #     :param uuid: (str) uuid of the rule to be changed
    #     :param name: (str) name of the rule
    #     :param subject_attrs: (list) list of subject attributes to be added
    #     :param object_attrs: (list) list of object attributes to be added
    #     :param description: (str) short description of the rule
    #     :return: (dict) a dict of the new rule
    #     """
    #     for rule in self.__rules:
    #         if rule["uuid"] == uuid:
    #             if name:
    #                 rule["name"] = name
    #             if description:
    #                 rule["description"] = description
    #             if subject_attrs:
    #                 rule["s_rules"] = list()
    #                 s_cat = self.get_subject_attribute_categories()
    #                 for s_attr in subject_attrs:
    #                     if s_attr["category"] in s_cat:
    #                         rule["s_rules"].append(s_attr)
    #             if object_attrs:
    #                 rule["o_rules"] = list()
    #                 o_cat = self.get_object_attribute_categories()
    #                 for o_attr in object_attrs:
    #                     if o_attr["category"] in o_cat:
    #                         rule["o_rules"].append(o_attr)
    #             self.sync()
    #             return rule
    #     raise RuleNotFoundException("rule {} not found".format(uuid))
    #
    # def del_rule(self, uuid):
    #     """Delete a rule
    #
    #     :param uuid: (str) uuid to delete
    #     :return: None
    #     """
    #     for rule in self.__rules:
    #         if rule["uuid"] == uuid:
    #             self.__rules.remove(rule)
    #             return
    #     raise RuleNotFoundException("rule {} not found".format(uuid))
    #
    # def __has_admin_assignment(
    #         self,
    #         object_uuid=None,
    #         attribute_uuid=None
    #     ):
    #     if object_uuid == "*":
    #         return True
    #     data = self.__administration["assignments"]
    #     for obj in data:
    #         if type(attribute_uuid) not in (list, tuple):
    #             attribute_uuid = [attribute_uuid, ]
    #         for att in attribute_uuid:
    #             if object_uuid == obj["object"] and att in obj["attributes"]:
    #                 return True
    #     return False
    #
    # def authz(self, auth):
    #     if "objects" not in self.__administration:
    #         auth["message"] = "No administration protocol for extension"
    #         auth["auth"] = True
    #         return auth
    #     if self.__tenant["name"] != auth["tenant_name"]:
    #         auth["message"] = "Tenant not found."
    #         return auth
    #     if auth["subject"] not in map(lambda x: x["uuid"], self.__subjects):
    #         auth["message"] = "User not found."
    #         return auth
    #     if auth["object_name"] not in map(lambda x: x["name"], self.__administration["objects"]):
    #         auth["message"] = "Object not found."
    #         return auth
    #     for obj in self.__administration["objects"]:
    #         if obj["name"] == auth["object_name"]:
    #             auth["object_uuid"] = obj["uuid"]
    #             break
    #     for rule in self.__administration["rules"]:
    #         _auth = False
    #         for s_rule in rule["s_attr"]:
    #             data = self.__subjectsAssignments
    #             attribute = s_rule["value"]
    #             for sbj in data:
    #                 if type(attribute) not in (list, tuple):
    #                     attribute = [attribute, ]
    #                 for att in attribute:
    #                     if auth["subject"] == sbj["subject"] and att in sbj["attributes"]:
    #                         _auth = True
    #                         break
    #         if not _auth:
    #             auth["message"] = "Rules on subject don't match."
    #             continue
    #         for o_rule in rule["o_attr"]:
    #                 if o_rule["category"] == "action":
    #                     _auth = self.__has_admin_assignment(
    #                         object_uuid=auth["object_uuid"],
    #                         attribute_uuid=auth["action"])
    #                     if not _auth:
    #                         auth["message"] = "Rules on action assignments don't match."
    #                         break
    #                     if auth["action"] not in o_rule["value"]:
    #                         auth["message"] = "Rules on action don't match."
    #                         break
    #                 else:
    #                     _auth = self.__has_admin_assignment(
    #                         object_uuid=auth["object_uuid"],
    #                         attribute_uuid=o_rule["value"])
    #                     if not _auth:
    #                         auth["message"] = "Rules on object don't match."
    #                         print(auth["object_uuid"], o_rule["value"])
    #                         break
    #         else:
    #             auth["message"] = ""
    #             auth["auth"] = True
    #             break
    #     return auth

    # def html(self):
    #     return mark_safe("""<b>Extension</b> {} for <b>tenant {}</b><br/><br/>
    #     <b>Subjects:</b> <ul>{}</ul><br>
    #     <b>Objects:</b> <ul>{}</ul>
    #     """.format(
    #         self.__name,
    #         self.__tenant["name"],
    #         "".join(map(lambda x: "<li>"+x["name"]+"</li>", self.__subjects)),
    #         "".join(map(lambda x: "<li>"+x["name"]+"</li>", self.__objects)),
    #     ))
>>>>>>> dev

    def __repr__(self):
        return """Extension {} ({})
        Subjects: {}
        Objects: {}
        """.format(
            self.__name,
            self.__uuid,
            map(lambda x: x["name"], self.authz_extension.get_subjects()),
            map(lambda x: x["name"], self.authz_extension.get_objects()),
        )
'''

