"""
Policy Decision Point
"""

import logging
logger = logging.getLogger(__name__)


import pkg_resources
from moon.core.pdp.intra_extension import IntraExtension


class IntraExtensions:
    def __init__(self):
        self.__installed_intra_extensions = dict()

    def install_intra_extension_from_json(self, extension_setting_dir):
        extension_setting_abs_dir = pkg_resources.resource_filename("moon", extension_setting_dir)
        intra_extension = IntraExtension()
        intra_extension.load_from_json(extension_setting_abs_dir)
        self.__installed_intra_extensions[intra_extension.get_name()] = intra_extension

    def get_installed_intra_extensions(self):
        return self.__installed_intra_extensions

    def __getitem__(self, key):
        if key in self.__installed_intra_extensions:
            return self.__installed_intra_extensions[key]
        else:
            return None

    def __setitem__(self, key, item):
        self.__installed_intra_extensions[key] = item

    def authz(
            self,
            subject,
            action,
            object_name,
            object_type,
            object_tenant,
            subject_tenant
    ):
        auth = {
            "auth": False,
            "tenant_name": "None",
            "rule_name": "None",
            "message": "",
            "subject": subject,
            "action": action,
            "object_name": object_name,
            "object_uuid": "",
            "subject_tenant": subject_tenant,
            "object_type": object_type,
            "object_tenant": object_tenant,
            "extension_name": "None"
        }
        return auth

    def sync_db(self):
        pass

intra_extentions = IntraExtensions()


def get_intra_extensions():
    return intra_extentions
