"""
Policy Decision Point
"""

from moon.core.pdp.inter_extension import get_inter_extensions
import os
import imp
import logging
from moon import settings
import re
import json
from uuid import uuid4
from moon.core.pdp.authz import enforce
from moon.core.pdp.intra_extension import IntraExtension
from moon.intra_extension_manager import get_dispatcher
from moon.tools.exceptions import *
logger = logging.getLogger(__name__)


class PublicAuthzInterface:

    def __init__(self, intra_extensions, inter_extensions):
        self.__intra_extensions = intra_extensions
        self.__inter_extensions = inter_extensions
        self.__BLOCK_UNKNOWN_TENANT = getattr(settings, "BLOCK_UNKNOWN_TENANT")
        self.__UNMANAGED_OBJECTS = getattr(settings, "UNMANAGED_OBJECTS", ("", "token", ))

    def __is_subject_assignment(self,
                                extension,
                                subject_uuid,
                                category,
                                attribute_name=None,
                                attribute_uuid=None):
        subject = extension.get_subjects(uuid=subject_uuid).next()
        try:
            assign = extension.get_subject_attribute_assignments(subject_name=subject["uuid"], category=category).next()
            if attribute_uuid and attribute_uuid in assign["attributes"]:
                return True
            if attribute_name:
                for attribute in assign["attributes"]:
                    attr = extension.get_subject_attributes(uuid=attribute).next()
                    if attr["value"] == attribute_name:
                        return True
        except StopIteration:
            pass
        return False

    def __is_object_assignment(self,
                               extension,
                               object_uuid,
                               category,
                               attribute_name=None,
                               attribute_uuid=None):
        object = extension.get_objects(uuid=object_uuid).next()
        try:
            assign = extension.get_object_attribute_assignments(object_name=object["uuid"], category=category)
            for _assign in assign:
                for attribute in _assign["attributes"]:
                    try:
                        attr = extension.get_object_attributes(uuid=attribute).next()
                    except StopIteration:
                        continue
                    if attr["value"] == attribute_name or \
                            (type(attribute_name) in (list, tuple) and attr["value"] in attribute_name) or \
                            (type(attribute_name) in (str, unicode) and attr["value"] == attribute_name) or \
                            attr["uuid"] == attribute_uuid or \
                            (type(attribute_uuid) in (list, tuple) and attr["uuid"] in attribute_uuid) or \
                            (type(attribute_uuid) in (str, unicode) and attr["uuid"] == attribute_uuid):
                        return True
        except StopIteration:
            import traceback
            print(traceback.print_exc())
        return False

    def __intra_tenant_authz(self, auth):
        for extension in self.__intra_extensions:
            if auth["subject_tenant"] != extension.get_tenant()["uuid"]:
                if auth["auth"] != "Out of Scope":
                    auth["auth"] = "Out of Scope"
                    auth["message"] = "Subject tenant was not found in intra-tenant extensions " \
                                      "or Subject tenant cannot be managed."
                continue
            auth["extension_name"] = extension.get_uuid()
            auth["tenant_name"] = extension.get_tenant()["name"]
            # if not extension.has_object_attributes(name=auth["object_type"]):
            #     logger.warning("Unknown object {}".format(auth["object_name"]))
            # else:
            #     find_object = True
            try:
                extension.get_subjects(uuid=auth["subject"]).next()
            except StopIteration:
                logger.warning("Subject {} unknown for tenant {}".format(auth["subject"], extension.get_tenant()))
                auth["auth"] = "Out of Scope"
                auth["message"] = "The request could be connected to a extension but no subject match."
                continue
            try:
                obj = extension.get_objects(uuid=auth["object_name"]).next()
                auth["object_uuid"] = obj["uuid"]
            except StopIteration:
                auth["auth"] = "Out of Scope"
                auth["message"] = "The request could be connected to a extension but no object match."
                #FIXME subject_tenant is false, we must found the true tenant for this object
                #FIXME this would be better done in nova_hook
                for ext in self.__intra_extensions:
                    try:
                        obj = ext.get_objects(uuid=auth["object_name"]).next()
                    except StopIteration:
                        continue
                    auth["object_uuid"] = obj["uuid"]
                    auth["object_tenant"] = obj["project"]["uuid"]
                    break
                break
            # print(extension)
            # print(extension.get_rules())
            for rule in extension.get_rules():
                # check if subject is in extension
                # check if object is in extension
                # check if subject has a assignment with s_attr (ie Role, Group, ...)
                # check if object has a assignment with o_attr (ie Type, Security, Size, ...)
                # check if action has a assignment with o_attr (ie Action)
                #   and given action is equal to the rule value
                auth["auth"] = False
                auth["message"] = "The request could be connected to a extension but no rule match."
                _auth = list()
                # print("------------------------------")
                # print(auth)
                for s_rule in rule["s_rules"]:
                    # print("\t\033[34ms_rule\033[m " + str(s_rule))
                    _auth.append(self.__is_subject_assignment(
                        extension=extension,
                        subject_uuid=auth["subject"],
                        category=s_rule["category"],
                        attribute_uuid=s_rule["value"],
                        attribute_name=s_rule["value"]))
                    # if not _auth:
                    #     break
                    # print("\033[32m"+str(_auth)+"\033[m")
                for o_rule in rule["o_rules"]:
                    # print("\t\033[34mo_rule\033[m " + str(o_rule))
                    if o_rule["category"] == "action":
                        has_assignment = self.__is_object_assignment(
                            extension=extension,
                            object_uuid=auth["object_uuid"],
                            category=o_rule["category"],
                            attribute_name=auth["action"])
                        if type(o_rule["value"]) not in (list, tuple):
                            o_rule["value"] = [o_rule["value"], ]
                        o_rule_value = map(lambda x: x.replace(".", "\\.").replace("*", ".*"), o_rule["value"])
                        _auth_action = False
                        # the o_rule_value is a regex expression, so we search for all action_uuid corresponding
                        # to that expression
                        _possible_actions = list(extension.get_object_attributes(category="action"))
                        possible_actions = []
                        for _o_rule_value in o_rule_value:
                            for _a in _possible_actions:
                                if re.match(_o_rule_value, _a["uuid"]):
                                    possible_actions.append(_a["value"])
                        for _o_rule_value in possible_actions:
                            if re.match(_o_rule_value, auth["action"]):
                                _auth_action = True
                                break
                        if _auth_action:
                            _auth.append(has_assignment)
                        else:
                            _auth.append(False)
                    else:
                        has_assignment = self.__is_object_assignment(
                            extension=extension,
                            object_uuid=auth["object_uuid"],
                            category=o_rule["category"],
                            attribute_uuid=o_rule["value"],
                            attribute_name=o_rule["value"])
                        _auth.append(has_assignment)
                    # print("\033[32m"+str(_auth)+"\033[m")
                    # print(_auth)
                    # if not _auth:
                    #     continue
                    #TODO o_attr -> o_rule
                    #o_attr ou s_attr= {
                    # "uuid": "high-security",
                    # "category": "security",
                    # "value": "50",
                    # "type": "continue" or "discontinue" or "include"
                    # "description": "high security needed" },
                    # rule = {
                    #     "s_attr": [],
                    #     "o_attr": [],
                    #     "comparison": [
                    #         #TODO
                    #     ],
                    # }
                main_auth = reduce(lambda x, y: x and y, _auth)
                if main_auth:
                    auth["auth"] = True
                    auth["rule_name"] = rule["name"]
                    auth["tenant_name"] = auth["subject_tenant"]
                    auth["message"] = ""
                    break
                else:
                    auth["auth"] = False
            break
        return auth

    def __inter_tenant_authz(self, auth):
        """
        # for e in extension_list
        #     if intra-authorization(s1, o1, a1) == OK
        #         return OK
        #     elif intra-authorization(s1, o1, a1) == "out of scope"
        #         for (e', e'', vEnt) in extension_relation
        #             if (s1, vEnt) in e' and (vEnt, o1) in e''
        #                 if intra-authorization(s1, vEnt, a1) and intra-authorization(vEnt, o1, a1)
        #                     return 'OK'
        #                 else
        #                     return 'KO'
        #             else
        #                 return 'out of scope'
        #     else
        #         return KO
        """
        for ext in self.__inter_extensions:
            #Check if this extension has the good requesting_tenant and requested_tenant
            if auth["subject_tenant"] == ext.requesting_tenant and auth["object_tenant"] == ext.requested_tenant:
                # print("\033[45mCheck intra authorization for subject\033[m")
                subject_auth = dict(auth)
                subject_auth["object_type"] = "virtual_entity"
                subject_auth["object_name"] = ext.category
                subject_auth["object_uuid"] = ext.category
                subject_auth["object_tenant"] = subject_auth["subject_tenant"]
                subject_auth = self.__intra_tenant_authz(subject_auth)
                # print("---------------------------")
                # print(subject_auth)
                # print("---------------------------")
                # print("\033[45mCheck intra authorization for object\033[m")
                object_auth = dict(auth)
                object_auth["subject"] = ext.category
                object_auth["subject_tenant"] = object_auth["object_tenant"]
                object_auth = self.__intra_tenant_authz(object_auth)
                # print("---------------------------")
                # print(object_auth)
                # print("---------------------------")
                if object_auth["auth"] and subject_auth["auth"]:
                    auth["auth"] = True
                    auth["message"] = "Inter tenant authorisation"
                    auth["rule_name"] = subject_auth["rule_name"] + "->" + object_auth["rule_name"]
                break
            else:
                #Out of scope
                #TODO: set message in auth
                auth["message"] = "No inter tenant extension match the request."
        return auth

    def authz(
            self,
            subject=None,
            action=None,
            object_name=None,
            subject_tenant=None,
            object_type=None,
            object_tenant=None):
        """
        Intra/Inter-tenant access control validation
        Parameters:
            subject: user who ask for resources
            action:  manipulation on resources
            object_name:  resources name
            subject_tenant: tenant name of the subject
            object_tenant: tenant name of the resources
        Return: boolean, tenant_name #TODO must return a dict {"authz": True, "tenant_name": "admin", "message": "..."}
        """
        auth = {
            "auth": False,
            "tenant_name": "None",
            "rule_name": "None",
            "message": "",
            "subject": subject,
            "action": action,
            "object_name": object_name,
            "object_uuid": "",
            "subject_tenant": subject_tenant,
            "object_type": object_type,
            "object_tenant": object_tenant,
            "extension_name": "None"
        }
        if object_type in self.__UNMANAGED_OBJECTS:
            auth["auth"] = True
            auth["rule_name"] = "UNMANAGED_OBJECTS"
            auth["message"] = "The request is on an unmanaged object."
        elif object_tenant == "None" and subject_tenant == "None":
            # TODO specific cases during authentication or when a user with no tenant ask for the list of tenants
            auth["auth"] = True
            auth["rule_name"] = "Default"
            logger.warning("object_tenant and subject_tenant are None together.")
        elif object_tenant == "None" or subject_tenant == object_tenant:
            # Intra Tenant
            auth = self.__intra_tenant_authz(auth)
        # print(auth)
        if auth["auth"] == "Out of Scope":
            # Inter Tenant
            auth = self.__inter_tenant_authz(auth)
        return auth


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

    def get_uuid(self):
        return self.__extension.get_uuid()

    def get_name(self):
        return self.__extension.get_name()

    def get_tenant(self):
        return self.__extension.get_tenant()

    def get_subjects(self, intra_extension, user_uuid):
        intra_extension.admin_extension.enforce(user_uuid, "subjects", "r")
        return intra_extension.get_subjects()

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
    def add_object(self, name, uuid="", description="", enabled=True, project=None):
        return self.__extension.add_objects(
            name=name,
            uuid=uuid,
            description=description,
            enabled=enabled,
            project=project)

    @enforce("perimeter.objects", "w")
    def del_object(self, uuid):
        return self.__extension.del_object(uuid)

    @enforce("perimeter.objects", "w")
    def set_object(self, uuid, name="", enabled=True, description="", project=None):
        return self.__extension.set_objects(
            uuid=uuid,
            name=name,
            enabled=enabled,
            description=description,
            project=project)

    @enforce("configuration.metadata") #TODO get_subject_categories
    def get_subject_attribute_categories(self, name):
        """ Return all categories for subjects

        :return:
        """
        return self.__extension.get_subject_attribute_categories(name)

    @enforce("configuration.metadata", "w")
    def add_subject_attribute_categories(self, name):
        """ Return all categories for subjects

        :return:
        """
        return self.__extension.add_subject_attribute_categories(name)

    @enforce("configuration.metadata", "w")
    def del_subject_attribute_categories(self, name):
        """ Return all categories for subjects

        :return:
        """
        return self.__extension.del_subject_attribute_categories(name)

    @enforce("configuration.metadata") #TODO get_object_categories
    def get_object_attribute_categories(self):
        """ Return all categories for objects

        :return:
        """
        return self.__extension.get_object_attribute_categories()

    @enforce("configuration.metadata", "w")
    def add_object_attribute_categories(self, name):
        """ Return all categories for subjects

        :return:
        """
        return self.__extension.add_object_attribute_categories(name)

    @enforce("configuration.metadata", "w")
    def del_object_attribute_categories(self, name):
        """ Return all categories for subjects

        :return:
        """
        return self.__extension.del_object_attribute_categories(name)

    @enforce("profiles.s_attr")  #TODO get_subject_category_values
    def get_subject_attributes(self, uuid=None, value=None, category=None):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.get_subject_attributes(uuid=uuid, value=value, category=category)

    @enforce("profiles.s_attr", "w")
    def add_subject_attributes(self, value, uuid=None, category=None, description=""):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.add_subject_attributes(
            value=value,
            uuid=uuid,
            category=category,
            description=description)

    @enforce("profiles.s_attr", "w")
    def del_subject_attributes(self, uuid):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.del_subject_attributes(uuid)

    @enforce("profiles.s_attr", "w") #TODO delete
    def set_subject_attributes(self, uuid, value="", category=None, description=""):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.set_subject_attributes(
            uuid=uuid,
            value=value,
            category=category,
            description=description)

    @enforce("profiles.o_attr")  #TODO get_object_category_values
    def get_object_attributes(self, uuid=None, value=None, category=None):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.get_object_attributes(uuid=uuid, value=value, category=category)

    @enforce("profiles.o_attr", "w")
    def add_object_attributes(self, value, uuid=None, category=None, description=""):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.add_object_attributes(
            value=value,
            uuid=uuid,
            category=category,
            description=description)

    @enforce("profiles.o_attr", "w")
    def del_object_attributes(self, uuid):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.del_object_attributes(uuid)

    @enforce("profiles.o_attr", "w") #TODO delete
    def set_object_attributes(self, uuid, value="", category=None, description=""):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.set_object_attributes(
            uuid=uuid,
            value=value,
            category=category,
            description=description)

    @enforce("profiles.s_attr_assign") #TODO get_subject_assignments(category_id)
    def get_subject_attribute_assignments(self, uuid=None, subject_name=None, category=None):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.get_subject_attribute_assignments(
            uuid=uuid,
            subject_name=subject_name,
            category=category)

    @enforce("profiles.s_attr_assign", "w") #TODO add_subject_assignment(category_id, subject_id, category_value)
    def add_subject_attribute_assignments(self, subject_name, category, uuid=None, attributes=None):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.add_subject_attribute_assignments(
            subject_name=subject_name,
            category=category,
            uuid=uuid,
            attributes=attributes)

    @enforce("profiles.s_attr_assign", "w") #TODO del_subject_assignment(category_id, subject_id, category_value)
    def del_subject_attribute_assignments(self, uuid=None, subject_name=None, category=None):
        """

        :param subject_name:
        :return: a list of dict with value and category
        """
        return self.__extension.del_subject_attribute_assignments(
            uuid=uuid,
            subject_name=subject_name,
            category=category)

    @enforce("profiles.s_attr_assign", "w") #TODO delete
    def set_subject_attribute_assignments(self, uuid=None, subject_name=None, category=None, attributes=None):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.set_subject_attribute_assignments(
            uuid=uuid,
            subject_name=subject_name,
            category=category,
            attributes=attributes)

    @enforce("profiles.o_attr_assign") #TODO get_object_assignments(category_id)
    def get_object_attribute_assignments(self, uuid=None, object_name=None, category=None):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.get_object_attribute_assignments(
            uuid=uuid,
            object_name=object_name,
            category=category)

    @enforce("profiles.o_attr_assign", "w") #TODO add_object_assignment(category_id, object_id, category_value)
    def add_object_attribute_assignments(self, uuid=None, object_name=None, category=None, attributes=None):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.add_object_attribute_assignments(
            uuid=uuid,
            object_name=object_name,
            category=category,
            attributes=attributes)

    @enforce("profiles.o_attr_assign", "w") #TODO del_object_assignment(category_id, object_id, category_value)
    def del_object_attribute_assignments(self, uuid=None, object_name=None, category=None):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.del_object_attribute_assignments(
            uuid=uuid,
            object_name=object_name,
            category=category)

    @enforce("profiles.o_attr_assign", "w") #TODO  delete
    def set_object_attribute_assignments(self, uuid=None, object_name=None, category=None, attributes=None):
        """

        :return: a list of dict with value and category
        """
        return self.__extension.set_object_attribute_assignments(
            uuid=uuid,
            object_name=object_name,
            category=category,
            attributes=attributes)

    @enforce("rules")
    def get_rules(self):
        """

        :return:
        """
        return self.__extension.get_rules()

    @enforce("rules", "w")
    def add_rule(self, name, subject_attrs, object_attrs, description=""):
        return self.__extension.add_rule(
            name=name,
            subject_attrs=subject_attrs,
            object_attrs=object_attrs,
            description=description)

    @enforce("rules", "w") #TODO  delete
    def set_rule(self, uuid, name="", subject_attrs=None, object_attrs=None, description=""):
        return self.__extension.set_rule(
            uuid=uuid,
            name=name,
            subject_attrs=subject_attrs,
            object_attrs=object_attrs,
            description=description)

    @enforce("rules", "w")
    def del_rule(self, uuid):
        return self.__extension.del_rule(uuid=uuid)

    def requesting_vent_create(self, vent, subjects_list):
        self.__extension.requesting_vent_create(vent=vent, subjects_list=subjects_list)

    def requested_vent_create(self, vent, objects_list):
        self.__extension.requested_vent_create(vent=vent, objects_list=objects_list)

    # def authz(self, user_uuid, object_name, tenant_name, mode):
    def authz(self, auth):
        # auth = {
        #     "auth": False,
        #     "rule_name": "None",
        #     "message": "",
        #     "subject": user_uuid,
        #     "action": mode,
        #     "object_name": object_name,
        #     "tenant_name": tenant_name,
        #     "extension_name": "Extension not found",
        # }
        return self.__extension.authz(auth)

    def sync(self):
        self.__extension.sync()

    # @enforce(("tenant", "perimeter.subjects", "perimeter.objects"))
    def html(self):
        return self.__extension.html()

    def __repr__(self):
        return str(self.__extension)


class IntraExtensions:

    def __init__(self):
        #TODO create a MongoDB collection per extension
        self.dispatcher = get_dispatcher()
        # self.__PublicAdminInterface = PublicAdminInterface(extension=get_intra_extentions().get())

        self.__extensions = dict()
        self.__secured_extensions = dict()

        for ext in self.dispatcher.list(type="extension"):
            extension_filename = ext["configuration"]["protocol"].split(":")[0]
            extension_class = ext["configuration"]["protocol"].split(":")[-1]
            if not os.path.isfile(extension_filename) or not os.path.isfile(extension_filename):
                raise Exception("Cannot find an adequate protocol for extension {}".format(ext["uuid"]))
            requesting_module = imp.load_source("requesting_vent_create", extension_filename)
            __IntraExtension = eval("requesting_module.{}".format(extension_class))
            self.__extensions[ext["uuid"]] = __IntraExtension(
                name=ext["name"],
                uuid=ext["uuid"],
                subjects=ext["perimeter"]["subjects"],
                objects=ext["perimeter"]["objects"],
                metadata=ext["configuration"]["metadata"],
                rules=ext["configuration"]["rules"],
                profiles=ext["profiles"],
                description=ext["description"],
                tenant=ext["tenant"],
                model=ext["model"],
                protocol=ext["configuration"]["protocol"],
                administration=ext["administration"]
            )
            self.__secured_extensions[ext["uuid"]] = PublicAdminInterface(self.__extensions[ext["uuid"]])
        self.__PublicAuthzInterface = PublicAuthzInterface(
            intra_extensions=self.get(),
            inter_extensions=get_inter_extensions().get()
        )

    def values(self):
        return self.__secured_extensions.values()

    def keys(self):
        return self.__extensions.keys()

    def get(self, uuid=None, name=None, attributes=dict()):
        """
        :param uuid: uuid of the extension
        :param name: name of the extension
        :param attributes: other attributes to look for
        :return: a list of extensions
        """
        if not uuid and not name and not attributes:
            return self.__secured_extensions.values()
        elif uuid:
            return [self.__secured_extensions[uuid], ]
        elif name:
            for ext in self.__secured_extensions.values():
                if ext.name == name:
                    return [ext, ]
        else:
            uuids = map(lambda x: x["uuid"], tuple(self.dispatcher.get(attributes=attributes)))
            exts = []
            for uuid in uuids:
                exts.append(self.__secured_extensions[uuid])
            return exts

    def get_object(self, uuid=None, name=None):
        if not uuid and not name:
            return self.__secured_extensions
        for ext in self.__secured_extensions.values():
            for obj in ext.get_object():
                if uuid and obj["uuid"] == uuid:
                    return [obj]
                elif name and obj["name"] == name:
                    return [obj]
        return []

    def new_from_json(self, json_data):
        # all_tenants = map(lambda x: x.tenant["uuid"], self.extensions.values())
        # if json_data["tenant"]["uuid"] not in all_tenants:
        extension_filename = json_data["configuration"]["protocol"].split(":")[0]
        extension_class = json_data["configuration"]["protocol"].split(":")[-1]
        if not os.path.isfile(extension_filename) or not os.path.isfile(extension_filename):
            raise Exception("Cannot find an adequate protocol for extension {}".format(extension_filename))
        requesting_module = imp.load_source("requesting_vent_create", extension_filename)
        __IntraExtension = eval("requesting_module.{}".format(extension_class))
        administration = dict()
        administration["filename"] = json_data["configuration"]["administration"]
        adm_obj = None
        try:
            adm_obj = json.loads(open(administration["filename"]).read())
        except IOError:
            pass
        if adm_obj:
            administration["objects"] = adm_obj["perimeter"]["objects"]
            administration["attributes"] = adm_obj["profiles"]["o_attr"]
            administration["assignments"] = adm_obj["profiles"]["o_attr_assign"]
            administration["rules"] = adm_obj["configuration"]["rules"]
            admin_role = filter(lambda x: x["value"] == "admin", json_data["profiles"]["s_attr"])[0]
            default_admin_rule = {
                "name": "default_rule_for_admin_user",
                "s_attr": [
                    {"category": "role", "value": admin_role["uuid"]}
                ],
                "o_attr": [
                    {
                        "category": "id", "value": [
                            "id_subjects_list",
                            "id_objects_list",
                            "id_rules_list",
                            "id_s_attr_list",
                            "id_o_attr_list",
                            "id_s_attr_assign_list",
                            "id_o_attr_assign_list",
                            "id_tenant"
                        ]
                    },
                    {"category": "action", "value": ["action-read", "action-write"]}
                ],
                "description": "The admin has all authorisations by default"
            }
            administration["rules"].append(default_admin_rule)
        ext = __IntraExtension(
            name=json_data["name"],
            uuid=json_data["uuid"],
            subjects=[],
            objects=[],
            metadata=json_data["configuration"]["metadata"],
            rules=json_data["configuration"]["rules"],
            profiles=json_data["profiles"],
            description=json_data["description"],
            tenant=json_data["tenant"],
            model=json_data["model"],
            protocol=json_data["configuration"]["protocol"],
            administration=administration
        )
        ext.sync()
        self.__extensions[json_data["uuid"]] = ext
        self.__secured_extensions[json_data["uuid"]] = PublicAdminInterface(self.__extensions[ext.get_uuid()])
        #Adding subjects and objects after so we can tune afterward the creation process
        for sbj in json_data["perimeter"]["subjects"]:
            if "description" not in sbj:
                sbj["description"] = ""
            if "mail" not in sbj:
                sbj["mail"] = ""
            if "project" not in sbj:
                sbj["project"] = ""
            ext.add_subject(
                uuid=sbj["uuid"],
                name=sbj["name"],
                domain=sbj["domain"],
                enabled=sbj["enabled"],
                mail=sbj["mail"],
                project=sbj["project"],
                description=sbj["description"])
        for obj in json_data["perimeter"]["objects"]:
            if "description" not in obj:
                obj["description"] = ""
            ext.add_object(
                uuid=obj["uuid"],
                name=obj["name"],
                enabled=obj["enabled"],
                project=obj["tenant"],
                description=obj["description"])
        return self.__secured_extensions[json_data["uuid"]]

    def new(
            self,
            uuid=None,
            name="",
            subjects=None,
            objects=None,
            metadata=None,
            rules=None,
            profiles=None,
            description=""):
        """Create a new Intra-extension
        :param uuid: uuid of this extension (optional)
        :param name: name of this extension
        :param subjects: list of subjects example:
            [{
                "uuid": "user1_uuid",
                "name": "admin",
                "mail": "admin@localhost",
                "tenant_id": "0123456789",
                "description": "an administrator",
                "enabled": True
            },]
        :param objects: list of objects example:
            [{
                "uuid": "object1_uuid",
                "name": "vm1",
                "description": "the virtual machine number 1",
                "enabled": True
            },]
        :param metadata: list of authorized attributes for subject and object, example:
            {
                "subject": [
                    "role",
                    "group"
                ],
                "object": [
                    "type",
                    "security"
                ]
            }
        :param rules: list of rules, example:
            [{
                "name": "rule1",
                "s_attr": { "category": "role", "value": "subject_attribute_uuid1" },
                "o_attr": { "category": "type", "value": "object_attribute_uuid1" },
                "a_attr": { "category": "action", "value": "list" },
                "description": "..."
            },]
        :param profiles: list of profiles, example:
            {
                "s_attr": {
                    "s_attr_uuid1": {
                        "category": "role",
                        "value": "admin",
                        "description": "le role admin"
                    },
                    "s_uuid2": {
                        "category": "role",
                        "value": "dev"
                    },
                    "s_uuid3": {
                        "category": "group",
                        "value": "prog"
                    }
                },
                "o_attr": {
                    "o_attr_uuid1": {
                        "category": "type",
                        "value": "stockage",
                        "description": ""
                    },
                    "o_uuid2": {
                        "category": "size",
                        "value": "medium"
                    }
                },
                "s_attr_assign": {
                    "assign1_uuid": {
                        "subject": "user1_uuid",
                        "attributes": [ "s_uuid1", "s_uuid3" ]
                    },
                    "assign2_uuid": {
                        "subject": "user3_uuid",
                        "attributes": [ "s_uuid1", "s_uuid2", "s_uuid3" ]
                    }
                },
                "o_attr_assign": {
                    "assign3_uuid": {
                        "object": "object1_uuid",
                        "attributes": [ "o_uuid1", "o_uuid3" ]
                    },
                    "assign4_uuid": {
                        "object": "object3_uuid",
                        "attributes": [ "o_uuid1", "o_uuid2", "o_uuid3" ]
                    }
                }
            }
        :param description: string describing the new extension.
        :return the created UUID
        """
        filename = getattr(settings, "DEFAULT_EXTENSION_TABLE")
        json_data = json.loads(file(filename).read())
        all_tenants = map(lambda x: x.tenant["uuid"], self.__extensions.values())
        if uuid:
            json_data["uuid"] = uuid
        else:
            json_data["uuid"] = str(uuid4()).replace("-", "")
        if name:
            json_data["name"] = name
        if subjects:
            json_data["perimeter"]["subjects"] = subjects
        if objects:
            json_data["perimeter"]["objects"] = objects
        if metadata:
            json_data["configuration"]["metadata"] = metadata
        if rules:
            json_data["configuration"]["rules"] = rules
        if profiles:
            json_data["profiles"] = profiles
        if description:
            json_data["description"] = description
        json_data["tenant"] = {}
        json_data["tenant"]["uuid"] = str(uuid4()).replace("-", "")
        if json_data["tenant"]["uuid"] not in all_tenants:
            ext = IntraExtension(
                name=json_data["name"],
                uuid=json_data["uuid"],
                subjects=json_data["perimeter"]["subjects"],
                objects=json_data["perimeter"]["objects"],
                metadata=json_data["configuration"]["metadata"],
                rules=json_data["configuration"]["rules"],
                profiles=json_data["profiles"],
                description=json_data["description"],
                tenant=json_data["tenant"]
            )
            ext.sync()
            self.__extensions[json_data["uuid"]] = ext
            self.__secured_extensions[json_data["uuid"]] = PublicAdminInterface(self.__extensions[ext.get_uuid()])
            return ext
        else:
            return None

    def delete_attributes_from_vent(self, uuid):
        for ext in self.get():
            try:
                ext.del_subject(uuid=uuid)
            except SubjectNotFoundException:
                pass
            try:
                ext.del_object(uuid=uuid)
            except ObjectNotFoundException:
                pass

    def delete_rules(self, s_attrs=None, o_attrs=None):
        if type(s_attrs) not in (list, tuple):
            s_attrs = (s_attrs, )
        if type(o_attrs) not in (list, tuple):
            o_attrs = (o_attrs, )
        for ext in self.get():
            for rule in ext.get_rules():
                found = False
                for s_attr in s_attrs:
                    for s_rule in rule["s_rules"]:
                        if "role" == s_rule["category"]:
                            role_uuid = ext.get_subject_attributes(
                                value="virtual_entity_role_{}".format(s_attr),
                                category="role").next()["uuid"]
                            if role_uuid == s_rule["value"]:
                                found = True
                                break
                if not found:
                    for o_attr in o_attrs:
                        for o_rule in rule["o_rules"]:
                            if "id" == o_rule["category"] and o_attr == o_rule["value"]:
                                found = True
                                break
                if found:
                    ext.del_rule(uuid=rule["uuid"])

    def delete(self, uuid):
        self.__extensions.pop(uuid)
        self.__secured_extensions.pop(uuid)
        return self.dispatcher.delete(uuid=uuid)

    def delete_tables(self):
        logger.warning("Dropping Intra Extension Database")
        self.__extensions = dict()
        self.__secured_extensions = dict()
        return self.dispatcher.drop()

    def authz(self, subject, action, object_name, object_type, object_tenant, subject_tenant):
        return self.__PublicAuthzInterface.authz(
            subject=subject,
            action=action,
            object_name=object_name,
            object_type=object_type,
            object_tenant=object_tenant,
            subject_tenant=subject_tenant)


intra_extentions = IntraExtensions()


def get_intra_extensions():
    return intra_extentions

