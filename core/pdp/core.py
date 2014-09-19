"""
Policy Decision Point
"""

import logging
import os
from moon.core.pdp.inter_extension import InterExtension
logger = logging.getLogger(__name__)


import pkg_resources
from moon.core.pdp.intra_extension import IntraExtension
from moon.core.pdp.sync_db import IntraExtensionsSyncer


class IntraExtensions:
    def __init__(self):
        self.__installed_intra_extensions = dict()
        self.__syncer = IntraExtensionsSyncer()

    def authz(self, sub, obj, act):
        for _intra_extension in self.__installed_intra_extensions.values():
            if _intra_extension.authz(sub, obj, act) == 'OK':
                return 'OK'
        return 'KO'

    def install_intra_extension_from_json(self, extension_setting_dir):
        extension_setting_abs_dir = extension_setting_dir
        if not os.path.isdir(extension_setting_dir):
            extension_setting_abs_dir = pkg_resources.resource_filename("moon", extension_setting_dir)
        _intra_extension = IntraExtension()
        _intra_extension.load_from_json(extension_setting_abs_dir)
        self.__installed_intra_extensions[_intra_extension.get_uuid()] = _intra_extension
        return _intra_extension.get_uuid()

    def install_intra_extension_from_db(self):
        intra_extension = IntraExtension()
        intra_extension.get_from_db()
        self.__installed_intra_extensions[intra_extension.get_uuid()] = intra_extension

    def get_installed_intra_extensions(self):
        return self.__installed_intra_extensions

    def get_intra_extensions_from_db(self):
        return self.__syncer.get_intra_extensions_from_db()

    def backup_intra_extensions_to_db(self):
        for _intra_extension in self.__installed_intra_extensions:
            self.__installed_intra_extensions[_intra_extension].backup_intra_extension_to_db()

    def install_intra_extensions_from_db(self):
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


class InterExtensions:  # TODO: to test
    def __init__(self, installed_intra_extensions):
        self.__installed_intra_extensions = installed_intra_extensions
        self.__installed_inter_extensions = dict()

    def authz(self, requesting_intra_extension_uuid, requested_intra_extension_uuid, sub, obj, act):
        for _installed_inter_extension in self.__installed_inter_extensions.values():
            if _installed_inter_extension.check_requesters(requesting_intra_extension_uuid, requested_intra_extension_uuid):
                if _installed_inter_extension.authhz(sub, obj, act) == 'OK':
                    return 'OK'
        return "KO"

    def admin(self, sub, obj, act):
        #TODO later
        return "OK"

    def create_collaboration(self, requesting_intra_extension_uuid, requested_intra_extension_uuid,
                             type, sub_list, obj_list, act):
        for _installed_inter_extension in self.__installed_inter_extensions.values():
            if _installed_inter_extension.check_requesters(requesting_intra_extension_uuid, requested_intra_extension_uuid):
                _inter_extension_uuid = _installed_inter_extension.get_uuid()
                _vent_uuid = _installed_inter_extension.create_collaboration(type, sub_list, obj_list, act)
                return _inter_extension_uuid, _vent_uuid

        _new_inter_extension = InterExtension(self.__installed_intra_extensions[requesting_intra_extension_uuid],
                                              self.__installed_intra_extensions[requested_intra_extension_uuid])
        _inter_extension_uuid = _new_inter_extension.get_uuid()
        self.__installed_inter_extensions[_inter_extension_uuid] = _new_inter_extension
        _vent_uuid = _new_inter_extension.create_collaboration(type, sub_list, obj_list, act)
        return _inter_extension_uuid, _vent_uuid

    def destroy_collaboration(self, inter_extension_uuid, vent_uuid):
        self.__installed_inter_extensions[inter_extension_uuid].destroy_collaboration(vent_uuid)
        self.__installed_inter_extensions.pop(inter_extension_uuid)

    def get_installed_inter_extensions(self):
        return self.__installed_inter_extensions


intra_extensions = IntraExtensions()
inter_extensions = InterExtensions(intra_extensions)


def get_intra_extensions():
    return intra_extensions


def get_inter_extensions():
    return inter_extensions


def authz(requesting_intra_extension_uuid, requested_intra_extension_uuid, sub, obj, act):
    if requesting_intra_extension_uuid == requested_intra_extension_uuid:
        return intra_extensions.authz(sub, obj, act)
    else:
        inter_extensions.authz(requesting_intra_extension_uuid, requested_intra_extension_uuid, sub, obj, act)
