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

    def sync_db(self):
        pass

intra_extentions = IntraExtensions()


def get_intra_extensions():
    return intra_extentions
