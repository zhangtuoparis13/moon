from intra_extension_manager import get_dispatcher as get_intra_dispatcher
from inter_extension_manager import get_dispatcher as get_inter_dispatcher
import logging
from moon import settings
import re

logger = logging.getLogger(__name__)


class AuthzManager:

    def __init__(self):
        self.intra_dispatcher = get_intra_dispatcher()
        self.inter_dispatcher = get_inter_dispatcher()
        self.intra_pdps = self.intra_dispatcher.extensions
        self.inter_pdps = self.inter_dispatcher.extensions
        self.tenants = self.inter_dispatcher.tenants
        self.BLOCK_UNKNOWN_TENANT = getattr(settings, "BLOCK_UNKNOWN_TENANT")

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
            "subject_tenant": subject_tenant,
            "object_type": object_type,
            "object_tenant": object_tenant
        }
        # rule_name = "None"
        find_extension = False
        find_rule = False
        find_object = False
        # print(subject, action, object_name, subject_tenant, object_type, object_tenant)
        if object_tenant == "None" and subject_tenant == "None":
            # TODO specific cases during authentication or when a user with no tenant ask for the list of tenants
            auth["auth"] = True
            auth["rule_name"] = "Default"
            logger.warning("object_tenant and subject_tenant are None together.")
        elif object_tenant == "None" or subject_tenant == object_tenant:
            # Intra Tenant
            for extension in self.intra_pdps.values():
                if subject_tenant != extension.tenant["uuid"]:
                    continue
                find_extension = True
                if not extension.has_object_attributes(name=object_type):
                    logger.warning("Unknown object {}".format(object_name))
                else:
                    find_object = True
                if not extension.has_subject(uuid=subject):
                    logger.warning("Subject {} unknown for tenant {}".format(subject, extension.tenant))
                    continue
                for rule in extension.get_rules():
                    # check if subject is in extension
                    # check if object is in extension
                    # check if subject has a assignment with s_attr (ie Role, Group, ...)
                    # check if object has a assignment with o_attr (ie Type, Security, Size, ...)
                    # check if action has a assignment with o_attr (ie Action)
                    #   and given action is equal to the rule value
                    if not extension.has_subject(uuid=subject):
                        continue
                    if not extension.has_object(uuid=object_name):
                        continue
                    find_rule = True
                    _auth = list()
                    for s_rule in rule["s_attr"]:
                        _auth.append(extension.has_assignment(
                            subject_uuid=subject,
                            category=s_rule["category"],
                            attribute_name=s_rule["value"]))
                    for o_rule in rule["o_attr"]:
                        if o_rule["category"] == "action":
                            has_assignment = extension.has_assignment(
                                object_uuid=object_name,
                                category=o_rule["category"],
                                attribute_uuid=action)
                            o_rule_value = o_rule["value"].replace(".", "\\.").replace("*", ".*")
                            if re.match(o_rule_value, action):
                                _auth.append(has_assignment)
                            else:
                                _auth.append(False)
                        else:
                            has_assignment = extension.has_assignment(
                                object_uuid=object_name,
                                category=o_rule["category"],
                                attribute_uuid=o_rule["value"])
                            _auth.append(has_assignment)
                    main_auth = reduce(lambda x, y: x and y, _auth)
                    if main_auth:
                        auth["auth"] = True
                        auth["rule_name"] = rule["name"]
                        auth["tenant_name"] = subject_tenant
                        break
        else:
            # Inter Tenant
            logger.warning("Inter Tenant authorization not developed!")
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
            for ext in get_inter_dispatcher().get():
                print(ext)
        if not find_rule and find_extension:
            # The request could be connected to a extension but no rule match
            auth["auth"] = "Out of scope"
            auth["message"] = "The request could be connected to a extension but no rule match."
        if not find_extension:
            # No extension match the request, the tenant cannot be managed
            if not self.BLOCK_UNKNOWN_TENANT:
                auth["auth"] = True
            else:
                auth["auth"] = False
            if object_tenant == "None" and subject_tenant == "None":
                auth["message"] = "No tenant given (special case)."
            else:
                auth["message"] = "No extension match the request, the tenant cannot be managed."
        return auth



manager = AuthzManager()


def get_manager():
    return manager