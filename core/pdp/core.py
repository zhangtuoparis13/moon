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

    def install_intra_extension_from_json(self, extension_setting_dir):
        extension_setting_abs_dir = extension_setting_dir
        if not os.path.isdir(extension_setting_dir):
            extension_setting_abs_dir = pkg_resources.resource_filename("moon", extension_setting_dir)
        intra_extension = IntraExtension()
        intra_extension.load_from_json(extension_setting_abs_dir)
        self.__installed_intra_extensions[intra_extension.get_uuid()] = intra_extension

    def install_intra_extension_from_db(self):
        intra_extension = IntraExtension()
        intra_extension.get_from_db()
        self.__installed_intra_extensions[intra_extension.get_uuid()] = intra_extension

    def get_installed_intra_extensions(self):
        return self.__installed_intra_extensions

    def set_to_db(self):
        for _intra_extension in self.__installed_intra_extensions:
            _intra_extension.set_to_db()

    def get_from_db(self):
        _intra_extension_dict = self.__syncer.get_intra_extensions_from_db()
        for _intra_extension_uuid in _intra_extension_dict:
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


class InterExtensions:  # TODO to test
    def __init__(self, installed_intra_extensions):
        self.__installed_intra_extensions = installed_intra_extensions
        self.__installed_inter_extensions = dict()

    def create_collaboration(self, requesting_intra_extension_uuid, requested_intra_extension_uuid, type, subs, objs, act):
        for _intra_extension in self.__installed_intra_extensions:
            if _intra_extension.get_uuid() == requesting_intra_extension_uuid:
                _requesting_intra_extension = _intra_extension
            elif _intra_extension.get_uuid() == requested_intra_extension_uuid:
                _requested_intra_extension = _intra_extension
            else:
                pass
            _inter_extension = InterExtension(_requesting_intra_extension, _requested_intra_extension)
            _inter_extension.create_collaboration(type, subs, objs, act)
            self.__installed_inter_extensions[_requesting_intra_extension.get_uudi()][_requested_intra_extension.get_uudi()][_inter_extension.get_uuid()] = _inter_extension

    def get_installed_inter_extensions(self):
        return self.__installed_inter_extensions


intra_extensions = IntraExtensions()
inter_extensions = InterExtensions(intra_extensions)


def get_intra_extensions():
    return intra_extensions


def get_inter_extensions():
    return inter_extensions