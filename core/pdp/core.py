"""
Policy Decision Point
"""

from moon.intra_extension_manager import get_dispatcher as get_intra_dispatcher
from moon.inter_extension_manager import get_dispatcher as get_inter_dispatcher
from moon.core.pdp.inter_extension import get_inter_extentions
from moon.core.pdp.intra_extension import get_intra_extentions
import logging
from moon import settings
import re
import json
from uuid import uuid4

logger = logging.getLogger(__name__)


class AuthzManager:

    def __init__(self):
        self.intra_dispatcher = get_intra_dispatcher()
        self.inter_dispatcher = get_inter_dispatcher()
        self.intra_pdps = get_intra_extentions()
        self.inter_pdps = get_inter_extentions()
        self.tenants = get_inter_extentions().tenants
        self.BLOCK_UNKNOWN_TENANT = getattr(settings, "BLOCK_UNKNOWN_TENANT")
        self.__UNMANAGED_OBJECTS = getattr(settings, "UNMANAGED_OBJECTS", ("", "token", ))

    def get_tenant_for_object(self, object_uuid):
        return self.intra_dispatcher.get_object(uuid=object_uuid)[0]

    def __intra_tenant_authz(self, auth):
        for extension in self.intra_pdps.get():
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
            if not extension.has_subject(uuid=auth["subject"]):
                logger.warning("Subject {} unknown for tenant {}".format(auth["subject"], extension.get_tenant()))
                auth["auth"] = "Out of Scope"
                auth["message"] = "The request could be connected to a extension but no subject match."
                continue
            if not extension.has_object(uuid=auth["object_name"]):
                auth["auth"] = "Out of Scope"
                auth["message"] = "The request could be connected to a extension but no object match."
                #FIXME subject_tenant is false, we must found the true tenant for this object
                #FIXME this would be better done in nova_hook
                try:
                    obj = self.intra_pdps.get_object(uuid=auth["object_name"])[0]
                    auth["object_uuid"] = obj["uuid"]
                    auth["object_tenant"] = obj["tenant"]["uuid"]
                except IndexError:
                    continue
                break
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
                for s_rule in rule["s_attr"]:
                    _auth.append(extension.has_assignment(
                        subject_uuid=auth["subject"],
                        category=s_rule["category"],
                        attribute_uuid=[], #if not set, the attributes is set to ["admin_uuid"], I don't know why...
                        attribute_name=s_rule["value"]))
                    # if not _auth:
                    #     break
                for o_rule in rule["o_attr"]:
                    # print(auth["object_uuid"], o_rule["category"], o_rule["value"])
                    if o_rule["category"] == "action":
                        has_assignment = extension.has_assignment(
                            object_uuid=auth["object_uuid"],
                            category=o_rule["category"],
                            attribute_uuid=[],
                            attribute_name=auth["action"])
                        if type(o_rule["value"]) not in (list, tuple):
                            o_rule["value"] = [o_rule["value"], ]
                        o_rule_value = map(lambda x: x.replace(".", "\\.").replace("*", ".*"), o_rule["value"])
                        _auth_action = False
                        # the o_rule_value is a regex expression, so we search for all action_uuid corresponding
                        # to that expression
                        _possible_actions = extension.get_object_attributes(category="action")
                        possible_actions = []
                        for _o_rule_value in o_rule_value:
                            for _a in _possible_actions:
                                if re.match(_o_rule_value, _a["value"]):
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
                        has_assignment = extension.has_assignment(
                            object_uuid=auth["object_uuid"],
                            category=o_rule["category"],
                            attribute_name=[],
                            attribute_uuid=o_rule["value"])
                        _auth.append(has_assignment)
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
        for ext in self.inter_pdps.get():
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
        # tenant_name = "None"
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
        # rule_name = "None"
        # find_extension = False
        # find_rule = False
        # find_object = False
        # print(subject, action, object_name, subject_tenant, object_type, object_tenant)
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


class AdminManager:

    def __init__(self):
        # self.__conf_filename = getattr(settings, "INTERNAL_AUTHZ_CONF")
        # self.__conf = json.loads(open(self.__conf_filename).read())
        # self.__dispatcher = get_intra_dispatcher()
        # ext = self.__dispatcher.list(type="internalextension")
        # if not ext:
        #     self.__uuid = str(uuid4()).replace("-", "")
        #     self.name = self.__conf["name"]
        #     self.__metadata = self.__conf["configuration"]["metadata"]
        #     self.__description = self.__conf["description"]
        #     self.__tenant = self.__conf["tenant"]
        #     self.__model = self.__conf["model"]
        #     self.__protocol = self.__conf["configuration"]["protocol"]
        #     self.__objects = self.__conf["perimeter"]["objects"]
        #     self.__subjects = self.__conf["perimeter"]["subjects"]
        #     self.__rules = self.__conf["configuration"]["rules"]
        #     self.__s_attr = self.__conf["profiles"]["s_attr"]
        #     self.__o_attr = self.__conf["profiles"]["o_attr"]
        #     self.__s_attr_assign = self.__conf["profiles"]["s_attr_assign"]
        #     self.__o_attr_assign = self.__conf["profiles"]["o_attr_assign"]
        #     self.sync()
        # else:
        #     ext = ext[0]
        #     self.__uuid = ext["uuid"]
        #     self.name = ext["name"]
        #     self.__metadata = ext["configuration"]["metadata"]
        #     self.__description = ext["description"]
        #     self.__tenant = ext["tenant"]
        #     self.__model = ext["model"]
        #     self.__protocol = ext["configuration"]["protocol"]
        #     self.__objects = ext["perimeter"]["objects"]
        #     self.__subjects = ext["perimeter"]["subjects"]
        #     self.__rules = ext["configuration"]["rules"]
        #     self.__s_attr = ext["profiles"]["s_attr"]
        #     self.__o_attr = ext["profiles"]["o_attr"]
        #     self.__s_attr_assign = ext["profiles"]["s_attr_assign"]
        #     self.__o_attr_assign = ext["profiles"]["o_attr_assign"]
        pass

    def authz(self, user_uuid, object_name, tenant_name, mode):
        auth = {
            "auth": False,
            "rule_name": "None",
            "message": "",
            "subject": user_uuid,
            "action": mode,
            "object_name": object_name,
            "tenant_name": tenant_name,
            "extension_name": "Extension not found",
        }
        for extension in get_intra_extentions().get():
            return extension.authz(auth)
        return auth


manager = AuthzManager()

admin_manager = AdminManager()


def get_admin_manager():
    return admin_manager


def get_manager():
    return manager