"""
"""
import logging
from moon.core.pdp import get_admin_manager

logger = logging.getLogger("moon.pap")


class PAP:
    """
    Policy Administration Point
    """

    def __init__(self, kclient=None):
        if not kclient:
            self.kclient = None
            # TODO: need authentication
        else:
            self.kclient = kclient
        self.admin_manager = get_admin_manager()

    def get_roles(self, extension_uuid):
        return self.admin_manager.get_roles(extension_uuid=extension_uuid)

    def get_groups(self, extension_uuid):
        return self.admin_manager.get_groups(extension_uuid=extension_uuid)

    def get_object_attributes(self, extension_uuid, category=None):
        return self.admin_manager.get_object_attributes(extension_uuid=extension_uuid, category=category)
