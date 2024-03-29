# Copyright 2014 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Policy Decision Point
"""

import os
from moon_server.core.pdp.inter_extension import InterExtension
import pkg_resources
from moon_server.core.pdp.intra_extension import IntraExtension
from moon_server.tools.sync_db import IntraExtensionsSyncer
from moon_server.core.pip import get_pip


class TenantIntraExtensionMapping:
    def __init__(self):
        self.tenant_intra_extension_mapping = [
            {
                "tenant_uuid": "admin",
                "intra_extension_uuids": ["super_extension"]
            }
        ]
        self.__tenants = dict()

    def get_tenants(self):
        # TODO check by super_extension
        self.__tenants = get_pip().get_tenants()
        return self.__tenants

    def list_mappings(self):
        return self.tenant_intra_extension_mapping

    def create_mapping(self, tenant_uuid, intra_extension_uuid):
        for _mapping in self.tenant_intra_extension_mapping:
            if tenant_uuid == _mapping["tenant_uuid"]:
                if intra_extension_uuid in _mapping["intra_extension_uuids"]:
                    return "[SuperExtension Error] Create Mapping for Existing Mapping"
                else:
                    _mapping["intra_extension_uuids"].append(intra_extension_uuid)
                    get_intra_extensions()[intra_extension_uuid].set_tenant_uuid(tenant_uuid)
                    return "[SuperExtension] Create Mapping for Existing Tenant: OK"

        _mapping = dict()
        _mapping["tenant_uuid"] = tenant_uuid
        _mapping["intra_extension_uuids"] = [intra_extension_uuid]
        self.tenant_intra_extension_mapping.append(_mapping)
        get_intra_extensions()[intra_extension_uuid].set_tenant_uuid(tenant_uuid)
        return "[SuperExtension] Create Mapping for No Existing Mapping: OK"

    def destroy_mapping(self, tenant_uuid, intra_extension_uuid):
        for _mapping in self.tenant_intra_extension_mapping:
            if tenant_uuid == _mapping["tenant_uuid"] and intra_extension_uuid in _mapping["intra_extension_uuids"]:
                if len(_mapping["intra_extension_uuids"]) >= 2:
                    _mapping["intra_extension_uuids"].remove(intra_extension_uuid)
                else:
                    self.tenant_intra_extension_mapping.remove(_mapping)
                get_intra_extensions()[intra_extension_uuid].set_tenant_uuid(None)
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

    def authz_for_tenant(self, tenant_uuid, sub, obj, act):
        for uuid in self.__installed_intra_extensions.keys():
            if self.__installed_intra_extensions[uuid].get_tenant_uuid() == tenant_uuid:
                if self.__installed_intra_extensions[uuid].authz(sub, obj, act) == 'OK':
                    return 'OK'
                else:
                    return 'KO'
        else:
            return 'NoExtension'

    def admin(self, sub, obj, act):
        for _intra_extension in self.__installed_intra_extensions.values():
            if _intra_extension.admin(sub, obj, act) == 'OK':
                return 'OK'
        return 'KO'

    def get_installed_intra_extensions(self):
        return self.__installed_intra_extensions

    def install_intra_extension_from_json(self, extension_setting_dir, name="Intra_Extension"):
        extension_setting_abs_dir = extension_setting_dir
        if not os.path.isdir(extension_setting_dir):
            extension_setting_abs_dir = pkg_resources.resource_filename("moon", extension_setting_dir)
        _intra_extension = IntraExtension()
        _intra_extension.load_from_json(extension_setting_abs_dir, name=name)
        self.__installed_intra_extensions[_intra_extension.get_uuid()] = _intra_extension
        return _intra_extension.get_uuid()

    def install_intra_extension_from_db(self):  # TODO test
        intra_extension = IntraExtension()
        intra_extension.load_from_db()
        self.__installed_intra_extensions[intra_extension.get_uuid()] = intra_extension

    def delete_intra_extension(self, intra_extension_uuid):
        if intra_extension_uuid not in self.__installed_intra_extensions.keys():
            return "Error {} not found in installed intra_extensions".format(intra_extension_uuid)
        return self.__installed_intra_extensions.pop(intra_extension_uuid)

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

    def delegate_privileges(self, inter_extension_uuid, delegator_uuid, privilege):
        return self.__installed_inter_extensions[inter_extension_uuid].delegate(delegator_uuid, privilege)

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

"""
def pdp_authz(sub, obj, act, requesting_tenant_uuid=None, requested_tenant_uuid=None):
    requesting_intra_extension_uuid = None
    requested_intra_extension_uuid = None
    if requesting_tenant_uuid and requested_tenant_uuid:
        if requesting_tenant_uuid == requested_tenant_uuid:
            return intra_extensions.authz_for_tenant(requesting_tenant_uuid, sub, obj, act)
        else:
            mapping_list = tenant_intra_extension_mapping.list_mappings()
            for mapping in mapping_list:
                if mapping["tenant_uuid"] == requesting_tenant_uuid:
                    requesting_intra_extension_uuid = mapping["intra_extension_uuids"][0]
                if mapping["tenant_uuid"] == requested_tenant_uuid:
                    requested_intra_extension_uuid = mapping["intra_extension_uuids"][0]
                # TODO multiple intra_extensions for each tenant
            if requesting_intra_extension_uuid and requested_intra_extension_uuid:
                inter_extensions.authz(requesting_intra_extension_uuid, requested_intra_extension_uuid, sub, obj, act)
            else:
                # raise Error unknow tenant uuid
                pass
    else:
        return intra_extensions.authz(sub, obj, act)
"""

def pdp_authz(sub, obj, act, requesting_tenant_uuid=None, requested_tenant_uuid=None):
    requesting_intra_extension_uuid = None
    requested_intra_extension_uuid = None
    if requesting_tenant_uuid and requested_tenant_uuid:
        if requesting_tenant_uuid == requested_tenant_uuid:
            return intra_extensions.authz_for_tenant(requesting_tenant_uuid, sub, obj, act)
        else:
            mapping_list = tenant_intra_extension_mapping.list_mappings()
            for mapping in mapping_list:
                if mapping["tenant_uuid"] == requesting_tenant_uuid:
                    requesting_intra_extension_uuid = mapping["intra_extension_uuids"][0]
                if mapping["tenant_uuid"] == requested_tenant_uuid:
                    requested_intra_extension_uuid = mapping["intra_extension_uuids"][0]
                # TODO multiple intra_extensions for each tenant
            if requesting_intra_extension_uuid and requested_intra_extension_uuid:
                inter_extensions.authz(requesting_intra_extension_uuid, requested_intra_extension_uuid, sub, obj, act)
            else:
                # raise Error unknow tenant uuid
                print("one extension is missing", requesting_intra_extension_uuid, requested_intra_extension_uuid)
    else:
        return intra_extensions.authz(sub, obj, act)


def pdp_admin(requesting_intra_extension_uuid, requested_intra_extension_uuid, sub, obj, act):
    if requesting_intra_extension_uuid == requested_intra_extension_uuid:
        return intra_extensions.admin(sub, obj, act)
    else:
        return inter_extensions.admin(requesting_intra_extension_uuid, requested_intra_extension_uuid, sub, obj, act)
