"""
Policy Decision Point
"""
from moon.core.pip import core as pip
from moon.info_repository.driver_dispatcher import get_tables
# list of tenant name and corresponding pdp_i
# example:
#   {
#       'tenant1': pdp1,
#       'tenant2': pdp2,
#   }
# pdps = {}


class PDP:

    def __init__(self, user_uuid="", tenant_name=None, policy_plugin_pointer=None, attributes=None):
        self.user_uuid = user_uuid
        self.tenant_name = tenant_name
        self.__policy_plugin_pointer = policy_plugin_pointer
        get_tables()
        #self.__s_attrs = attributes['s_attrs']
        #self.__a_attrs = attributes['a_attrs']
        #self.__o_attrs = attributes['o_attrs']
        #self.__other_attrs = attributes['other_attrs']
        self.__attributes = attributes

    def authz(self, subject=None, action=None, object_name=None):
        self.__attributes = self.update_request_attributes(subject, action, object_name)
        return self.__policy_plugin_pointer.authz(
            subject=subject,
            action=action,
            object_name=object_name,
            attributes=self.__attributes
        )

    def update_request_attributes(self, subject=None, action=None, object_name=None):
        """
        Update user attributes list from attributes keys in Policy plugin
        and values in user_db
        """
        self.__attributes = pip.update_request_attributes(subject,
                                                          action,
                                                          object_name,
                                                          self.tenant_name,
                                                          self.__attributes)
        return self.__attributes

# def authz(
#         subject=None,
#         action=None,
#         object_name=None,
#         subject_tenant=None,
#         object_tenant=None):
#     """
#     Inter-tenant access control validation
#     Parameters:
#         subject: user who ask for resources
#         action:  manipulation on resources
#         object_name:  resources name
#         subject_tenant: tenant name of the subject
#         object_tenant: tenant name of the resources
#     Return: boolean
#     """
#     auth = False
#     if subject_tenant == object_tenant:
#         # intra tenant access control
#         # check pdp_i
#         auth = pdps[subject_tenant].authz(subject, action, object_name)
#     else:
#         # inter tenant access control
#         # check tenant_tree
#         # check pdp_i tenant1
#         # check pdp_i tenant2
#         pass
#     return auth


# def tenant_registry(tenant_uuid, tenant_name, policy_plugin_pointer, attributes):
#     pdp_i = PDP(tenant_uuid, tenant_name, policy_plugin_pointer, attributes)
#     pdps[tenant_name] = pdp_i