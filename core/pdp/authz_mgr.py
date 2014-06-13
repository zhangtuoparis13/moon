from intra_extension_manager import get_dispatcher as get_intra_dispatcher
from inter_extension_manager import get_dispatcher as get_inter_dispatcher
import logging

logger = logging.getLogger(__name__)


class AuthzManager:

    def __init__(self):
        self.intra_dispatcher = get_intra_dispatcher()
        self.inter_dispatcher = get_inter_dispatcher()
        self.intra_pdps = self.intra_dispatcher.extensions
        self.inter_pdps = self.inter_dispatcher.extensions
        self.tenants = self.inter_dispatcher.tenants

    # def __check_policy(self, subject, action, object_name, tenant_name=""):
    #     auth = False
    #     tenant_name = tenant_name.replace("*", ".*")
    #     policy_found = False
    #     for key in self.intra_pdps.keys():
    #         if re.match(key, tenant_name):
    #             auth = self.intra_pdps[key].authz(subject, action, object_name)
    #             policy_found = True
    #             break
    #     if not policy_found:
    #         logger.warning("No policy found for tenant {}".format(tenant_name))
    #     return auth

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
            "message": ""
        }
        # rule_name = "None"
        find_rule = False
        if object_tenant == "None" and subject_tenant == "None":
            # TODO specific cases during authentication or when a user with no tenant ask for the list of tenants
            auth["auth"] = True
            logger.warning("object_tenant and subject_tenant are None together.")
        elif object_tenant == "None" or subject_tenant == object_tenant:
            # Intra Tenant
            for extension in self.intra_pdps.values():
                if subject_tenant != extension.tenant["uuid"]:
                    continue
                find_rule = True
                if not extension.has_object_attributes(name=object_type):
                    logger.warning("Unknown object {}".format(object_name))
                else:
                    if not extension.has_subject(uuid=subject):
                        logger.warning("Subject {} unknown for tenant {}".format(subject, extension.tenant))
                        continue
                for rule in extension.get_rules():
                    # check if subject has a assignment with s_attr (ie Role, Group, ...)
                    # check if object has a assignment with o_attr (ie Type, Security, Size, ...)
                    # check if action has a assignment with a_attr (ie Action)
                    # print("rule {} has assignment {} {} {}".format(
                    #     rule["name"],
                    #     extension.has_assignment(
                    #             subject_uuid=subject,
                    #             category=rule["s_attr"]["category"],
                    #             attribute_name=rule["s_attr"]["value"]),
                    #     extension.has_assignment(
                    #             object_name=object_name,
                    #             category=rule["o_attr"]["category"],
                    #             attribute_name=rule["o_attr"]["value"]),
                    #     extension.has_assignment(
                    #             object_name=action,
                    #             category=rule["a_attr"]["category"],
                    #             attribute_name=rule["a_attr"]["value"])
                    # ))
                    if extension.has_assignment(
                            subject_uuid=subject,
                            category=rule["s_attr"]["category"],
                            attribute_name=rule["s_attr"]["value"]) \
                        and extension.has_assignment(
                            object_name=object_name,
                            category=rule["o_attr"]["category"],
                            attribute_name=rule["o_attr"]["value"]) \
                        and extension.has_assignment(
                            object_name=action,
                            category=rule["a_attr"]["category"],
                            attribute_name=rule["a_attr"]["value"]):
                        auth["auth"] = True
                        auth["rule_name"] = rule["name"]
                        auth["tenant_name"] = subject_tenant
                        break
        else:
            # Inter Tenant
            logger.warning("Inter Tenant authorization not developed!")
        if not auth["auth"] and not find_rule:
            logger.warning("No rule matches the request")
        return auth



manager = AuthzManager()


def get_manager():
    return manager