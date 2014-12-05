import pkg_resources
from uuid import uuid4
from moon_server.core.pdp.extension import Extension
# from moon_server.core.pdp import get_intra_extensions


tenant_intra_extension_mapping = [
    {
        "tenant_uuid": "admin",
        "intra_extension_uuids": ["super_extension"]
    }
]


class SuperExtension:
    def __init__(self):
        self.__uuid = str(uuid4())
        self.__tenant_uuid = ""
        # self.__intra_extensions = get_intra_extensions()
        self.__super_extension = Extension()
        _policy_abs_dir = '/etc/moon/super_extension/policy'
        import os
        if os.path.isdir('core/pdp/super_extension/policy'):
            _sample_path = 'core/pdp/super_extension/policy'
            _policy_abs_dir = pkg_resources.resource_filename('moon_server', _sample_path)
        self.__super_extension.load_from_json(_policy_abs_dir)

    def admin(self, sub, obj, act):
        return self.__super_extension.authz(sub, obj, act)

    def delegate(self, delegating_uuid, delegated_uuid, privilege):  # TODO later
        pass
        # self.__super_extension.add_subject(delegated_uuid)
        # # if genre == "mapping":
        # if privilege == "list":
        #     if self.__super_extension.add_subject_assignment("role", delegator_uuid, "super_user") \
        #             == "[ERROR] Add Subject Assignment: Subject Assignment Exists":
        #         return "[SuperExtension ERROR] Mapping Delegate: Privilege Exists"
        #     else:
        #         return "[SuperExtension] Delegate: Add Super_User Privilege"
        # elif privilege == "create" or privilege == "destroy":
        #     if self.__super_extension.add_subject_assignment("role", delegator_uuid, "super_admin") \
        #             == "[ERROR] Add Subject Assignment: Subject Assignment Exists":
        #         return "[SuperExtension ERROR] Mapping Delegate: Privilege Exists"
        #     else:
        #         return "[SuperExtension] Delegate: Add Super_Admin Privilege"
        # elif privilege == "delegate":
        #     if self.__super_extension.add_subject_assignment("role", delegator_uuid, "super_root") \
        #             == "[ERROR] Add Subject Assignment: Subject Assignment Exists":
        #         return "[SuperExtension ERROR] Mapping Delegate: Privilege Exists"
        #     else:
        #         return "[SuperExtension] Delegate: Add Super_Root Privilege"
        # else:
        #     return "[SuperExtension Error] Mapping Delegate Unknown Privilege"
        # elif genre == "collaboration":
        #     if privilege == "list":
        #         if self.__super_extension.add_subject_assignment("role", delegator_uuid, "inter_extension_user") \
        #                 == "[ERROR] Add Subject Assignment: Subject Assignment Exists":
        #             return "[SuperExtension ERROR] Collaboration Delegate: Privilege Exists"
        #         else:
        #             return "[SuperExtension] Delegate: Add Inter_Extension_User Privilege"
        #     elif privilege == "create" or privilege == "destroy":
        #         if self.__super_extension.add_subject_assignment("role", delegator_uuid, "inter_extension_admin") \
        #                 == "[ERROR] Add Subject Assignment: Subject Assignment Exists":
        #             return "[SuperExtension ERROR] Collaboration Delegate: Privilege Exists"
        #         else:
        #             return "[SuperExtension] Delegate: Add Inter_Extension_Admin Privilege"
        #     elif privilege == "delegate":
        #         if self.__super_extension.add_subject_assignment("role", delegator_uuid, "inter_extension_root") \
        #                 == "[ERROR] Add Subject Assignment: Subject Assignment Exists":
        #             return "[SuperExtension ERROR] Collaboration Delegate: Privilege Exists"
        #         else:
        #             return "[SuperExtension] Delegate: Add Inter_Extension_Root Privilege"
        #     else:
        #         return "[SuperExtension Error] Collaboration Delegate Unknown Privilege"
        # else:
        #     return "[SuperExtension Error] Collaboration Delegate Unknown Genre"

super_extension = SuperExtension()


def get_super_extension():
    return super_extension


