"""
Policy Decision Point
"""
# from moon.core.pip import core as pip
# from moon.info_repository.driver_dispatcher import get_tables


# class IntraPDP:
#
#     def __init__(self, user_uuid="", tenant_name=None, policy_plugin_pointer=None, attributes=None):
#         self.user_uuid = user_uuid
#         self.tenant_name = tenant_name
#         self.__policy_plugin_pointer = policy_plugin_pointer
#         self.enabled = True
#         self.description = self.__policy_plugin_pointer.get_description()
#         self.__attributes = attributes
#
#     def get_rules(self):
#         return self.__policy_plugin_pointer.rules
#
#     def get_metadata(self):
#         return self.__policy_plugin_pointer.attributes
#
#     def authz(self, subject=None, action=None, object_name=None):
#         """
#         parameter subject, object, action
#         return OK=True, KO=False, OS=None
#         """
#         # self.__attributes = self.update_request_attributes(subject, action, object_name)
#         return self.__policy_plugin_pointer.authz(
#             subject=subject,
#             action=action,
#             object_name=object_name,
#             attributes=self.__attributes
#         )
#
#     # def update_request_attributes(self, subject=None, action=None, object_name=None):
#     #     """
#     #     Update user attributes list from attributes keys in Policy plugin
#     #     and values in user_db
#     #     """
#     #     self.__attributes = pip.update_request_attributes(subject,
#     #                                                       action,
#     #                                                       object_name,
#     #                                                       self.tenant_name,
#     #                                                       self.__attributes)
#     #     return self.__attributes
#
#
# class InterPDP:
#     pass