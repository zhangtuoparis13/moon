"""
Policy Decision Point
"""

import logging
import os
from moon.core.pdp.inter_extension import InterExtension
logger = logging.getLogger(__name__)
import pkg_resources
from moon.core.pdp.intra_extension import IntraExtension
from moon.tools.sync_db import IntraExtensionsSyncer


class TenantIntraExtensionMapping:
    def __init__(self):
        self.tenant_intra_extension_mapping = [
            {
                "tenant_uuid": "admin",
                "intra_extension_uuids": ["super_extension"]
            }
        ]

    def list_mappings(self):
        return self.tenant_intra_extension_mapping

    def create_mapping(self, tenant_uuid, intra_extension_uuid):
        for _mapping in self.tenant_intra_extension_mapping:
            if tenant_uuid == _mapping["tenant_uuid"]:
                if intra_extension_uuid in _mapping["intra_extension_uuids"]:
                    return "[SuperExtension Error] Create Mapping for Existing Mapping"
                else:
                    _mapping["intra_extension_uuids"].append(intra_extension_uuid)
                    return "[SuperExtension] Create Mapping for Existing Tenant: OK"

        _mapping = dict()
        _mapping["tenant_uuid"] = tenant_uuid
        _mapping["intra_extension_uuids"] = [intra_extension_uuid]
        self.tenant_intra_extension_mapping.append(_mapping)
        return "[SuperExtension] Create Mapping for No Existing Mapping: OK"

    def destroy_mapping(self, tenant_uuid, intra_extension_uuid):
        for _mapping in self.tenant_intra_extension_mapping:
            if tenant_uuid == _mapping["tenant_uuid"] and intra_extension_uuid in _mapping["intra_extension_uuids"]:
                if len(_mapping["intra_extension_uuids"]) >= 2:
                    _mapping["intra_extension_uuids"].remove(intra_extension_uuid)
                else:
                    self.tenant_intra_extension_mapping.remove(_mapping)
                return "[SuperExtension] Destroy Mapping: OK"
        return "[SuperExtension Error] Destroy Unknown Mapping"


class IntraExtensions:
    def __init__(self):
        self.__installed_intra_extensions = dict()
        self.__syncer = IntraExtensionsSyncer()

    def authz(self, sub, obj, act):
        for _intra_extension in self.__installed_intra_extensions.values():
            if _intra_extension.authz(sub, obj, act) == 'OK':
                return 'OK'
        return 'KO'

    def admin(self, sub, obj, act):
        for _intra_extension in self.__installed_intra_extensions.values():
            if _intra_extension.admin(sub, obj, act) == 'OK':
                return 'OK'
        return 'KO'

    def get_installed_intra_extensions(self):
        return self.__installed_intra_extensions

    def install_intra_extension_from_json(self, extension_setting_dir):
        extension_setting_abs_dir = extension_setting_dir
        if not os.path.isdir(extension_setting_dir):
            extension_setting_abs_dir = pkg_resources.resource_filename("moon", extension_setting_dir)
        _intra_extension = IntraExtension()
        _intra_extension.load_from_json(extension_setting_abs_dir)
        self.__installed_intra_extensions[_intra_extension.get_uuid()] = _intra_extension
        return _intra_extension.get_uuid()

    def install_intra_extension_from_db(self):  # TODO test
        intra_extension = IntraExtension()
        intra_extension.load_from_db()
        self.__installed_intra_extensions[intra_extension.get_uuid()] = intra_extension

    def delete_intra_extension(self, intra_extensin_uuid):
        self.__installed_intra_extensions.pop(intra_extensin_uuid)

    def get_intra_extensions_from_db(self):  # TODO test
        return self.__syncer.get_intra_extensions_from_db()

    def backup_intra_extensions_to_db(self):  # TODO test
        for _intra_extension in self.__installed_intra_extensions:
            self.__installed_intra_extensions[_intra_extension].backup_intra_extension_to_db()

    def install_intra_extensions_from_db(self):  # TODO test
        _intra_extension_dict = self.__syncer.get_intra_extensions_from_db()
        for _intra_extension_uuid in _intra_extension_dict:
            if _intra_extension_uuid not in self.__installed_intra_extensions:
                _intra_extension = IntraExtension()
                _intra_extension.set_data(_intra_extension_dict[_intra_extension_uuid])
                self.__installed_intra_extensions[_intra_extension_uuid] = _intra_extension

    def __getitem__(self, key):
        if key in self.__installed_intra_extensions:
            return self.__installed_intra_extensions[key]
        else:
            return None

    def __setitem__(self, key, item):
        self.__installed_intra_extensions[key] = item

    def values(self):
        return self.__installed_intra_extensions

    def keys(self):
        return set(self.__installed_intra_extensions.keys())


class InterExtensions:
    def __init__(self, installed_intra_extensions):
        self.__installed_intra_extensions = installed_intra_extensions
        self.__installed_inter_extensions = dict()

    def authz(self, requesting_intra_extension_uuid, requested_intra_extension_uuid, sub, obj, act):
        for _installed_inter_extension in self.__installed_inter_extensions.values():
            if _installed_inter_extension.check_requesters(requesting_intra_extension_uuid, requested_intra_extension_uuid):
                if _installed_inter_extension.authz(sub, obj, act) == 'OK':
                    return 'OK'
        return "KO"

    def admin(self, requesting_intra_extension_uuid, requested_intra_extension_uuid, sub, obj, act):
        for _installed_inter_extension in self.__installed_inter_extensions.values():
            if _installed_inter_extension.check_requesters(requesting_intra_extension_uuid, requested_intra_extension_uuid):
                if _installed_inter_extension.admin(sub, obj, act) == 'OK':
                    return 'OK'
        return "KO"

    def create_collaboration(self, requesting_intra_extension_uuid, requested_intra_extension_uuid,
                             genre, sub_list, obj_list, act):  # TODO test
        for _installed_inter_extension_uuid, _installed_inter_extension in self.__installed_inter_extensions:
            if _installed_inter_extension.check_requesters(requesting_intra_extension_uuid,
                                                           requested_intra_extension_uuid):
                _vent_uuid = _installed_inter_extension.create_collaboration(genre, sub_list, obj_list, act)
                if _vent_uuid is "[InterExtension Error] Create Collaboration: vEnt Exists":
                    return "[InterExtension] Create Collaboration: vEnt Exists"
                else:
                    return _installed_inter_extension_uuid, _vent_uuid

        _new_inter_extension = InterExtension(self.__installed_intra_extensions[requesting_intra_extension_uuid],
                                              self.__installed_intra_extensions[requested_intra_extension_uuid])
        _inter_extension_uuid = _new_inter_extension.get_uuid()
        self.__installed_inter_extensions[_inter_extension_uuid] = _new_inter_extension
        _vent_uuid = _new_inter_extension.create_collaboration(genre, sub_list, obj_list, act)
        return _inter_extension_uuid, _vent_uuid

    def destroy_collaboration(self, genre, inter_extension_uuid, vent_uuid):
        if self.__installed_inter_extensions[inter_extension_uuid].destroy_collaboration(genre, vent_uuid) \
                == "[InterExtension] Destroy Collaboration: OK":
            self.__installed_inter_extensions.pop(inter_extension_uuid)
            return "[InterExtensions] Destroy Collaboration: OK"
        else:
            return "[InterExtensions Error] Destroy Collaboration: No Success"

    def get_installed_inter_extensions(self):
        return self.__installed_inter_extensions


intra_extensions = IntraExtensions()
inter_extensions = InterExtensions(intra_extensions)
tenant_intra_extension_mapping = TenantIntraExtensionMapping()


def get_intra_extensions():
    return intra_extensions


def get_inter_extensions():
    return inter_extensions


def get_tenant_intra_extension_mapping():
    return tenant_intra_extension_mapping


def authz(requesting_intra_extension_uuid, requested_intra_extension_uuid, sub, obj, act):
    if requesting_intra_extension_uuid == requested_intra_extension_uuid:
        return intra_extensions.authz(sub, obj, act)
    else:
        inter_extensions.authz(requesting_intra_extension_uuid, requested_intra_extension_uuid, sub, obj, act)


def admin(requesting_intra_extension_uuid, requested_intra_extension_uuid, sub, obj, act):
    if requesting_intra_extension_uuid == requested_intra_extension_uuid:
        return intra_extensions.admin(sub, obj, act)
    else:
        inter_extensions.admin(requesting_intra_extension_uuid, requested_intra_extension_uuid, sub, obj, act)
