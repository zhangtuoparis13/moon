"""
Policy Decision Point
"""

import os
import imp
import logging
from moon import settings
import re
import json
import os.path
import pkg_resources
from uuid import uuid4
from moon.core.pdp.intra_extension import IntraExtension
from moon.tools.exceptions import *
logger = logging.getLogger(__name__)


class IntraExtensions:

    def __init__(self):
        _installed_extensions = dict()

    def install_extension_from_json(self, extension_setting_dir):
        extension_setting_abs_dir = pkg_resources.resource_filename("moon", extension_setting_dir)
        intra_extension = IntraExtension(extension_setting_abs_dir)
        _installed_extensions[intra_extension.name] = intra_extension

        # metadata_path = os.path.join(metadatadir, "metadata.json")
        # f = open(metadata_path)
        # metadata = Metadata(f)


intra_extentions = IntraExtensions()


def get_intra_extensions():
    return intra_extentions
