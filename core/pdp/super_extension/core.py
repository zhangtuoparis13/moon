import os.path
import pkg_resources
from uuid import uuid4
from moon.core.pdp.extension import Extension
from moon.core.pdp import get_intra_extensions


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
        self.__intra_extensions = get_intra_extensions()
        self.__super_extension = Extension()

        _sample_path = 'core/pdp/super_extension/policy'
        _policy_abs_dir = pkg_resources.resource_filename('moon', _sample_path)
        self.__super_extension.load_from_json(_policy_abs_dir)

    def admin(self, sub, obj, act):
        return self.__super_extension.authz(sub, obj, act)

    def list_mappings(self):
        return tenant_intra_extension_mapping

    def create_mapping(self, tenant_uuid, intra_extension_uuid):
        for _mapping in tenant_intra_extension_mapping:
            if tenant_uuid == _mapping["tenant_uuid"]:
                if intra_extension_uuid in _mapping["intra_extension_uuids"]:
                    return "[SuperExtension Error] Create Mapping for Existing Mapping"
                else:
                    _mapping["intra_extension_uuids"].append(intra_extension_uuid)
                    return "[SuperExtension] Create Mapping for Existing Tenant: OK"

        _mapping = dict()
        _mapping["tenant_uuid"] = tenant_uuid
        _mapping["intra_extension_uuids"] = [intra_extension_uuid]
        tenant_intra_extension_mapping.append(_mapping)
        return "[SuperExtension] Create Mapping for No Existing Mapping: OK"

    def destroy_mapping(self, tenant_uuid, intra_extension_uuid):
        for _mapping in tenant_intra_extension_mapping:
            if tenant_uuid == _mapping["tenant_uuid"] and intra_extension_uuid in _mapping["intra_extension_uuids"]:
                if len(_mapping["intra_extension_uuids"]) >= 2:
                    _mapping["intra_extension_uuids"].remove(intra_extension_uuid)
                else:
                    tenant_intra_extension_mapping.remove(_mapping)
                return "[SuperExtension] Destroy Mapping: OK"
        return "[SuperExtension Error] Destroy Unknown Mapping"

    def delegate(self, delegator_uuid, privilege):
        self.__super_extension.add_subject(delegator_uuid)
        if privilege == "list":
            if self.__super_extension.add_subject_assignment("role", delegator_uuid, "super_user") \
                    == "[ERROR] Add Subject Assignment: Subject Assignment Exists":
                return "[SuperExtension ERROR] Delegate: Privilege Exists"
            else:
                return "[SuperExtension] Delegate: Add Super_User Privilege"
        elif privilege == "create" or privilege == "destroy":
            if self.__super_extension.add_subject_assignment("role", delegator_uuid, "super_admin") \
                    == "[ERROR] Add Subject Assignment: Subject Assignment Exists":
                return "[SuperExtension ERROR] Delegate: Privilege Exists"
            else:
                return "[SuperExtension] Delegate: Add Super_Admin Privilege"
        elif privilege == "delegate":
            if self.__super_extension.add_subject_assignment("role", delegator_uuid, "super_root") \
                    == "[ERROR] Add Subject Assignment: Subject Assignment Exists":
                return "[SuperExtension ERROR] Delegate: Privilege Exists"
            else:
                return "[SuperExtension] Delegate: Add Super_Root Privilege"
        else:
            return "[SuperExtension Error] Delegate Unknown Privilege"

super_extension = SuperExtension()


def get_super_extension():
    return super_extension


