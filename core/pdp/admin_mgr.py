from intra_extension_manager import get_dispatcher as get_intra_dispatcher
from inter_extension_manager import get_dispatcher as get_inter_dispatcher
import logging


class AdminManager:

    def __init__(self):
        self.intra_dispatcher = get_intra_dispatcher()
        self.inter_dispatcher = get_inter_dispatcher()
        self.intra_pdps = self.intra_dispatcher.extensions
        self.inter_pdps = self.inter_dispatcher.extensions
        self.tenants = self.inter_dispatcher.tenants

    def get_intra_extensions(self, uuid=None, tenant_uuid=None, tenant_name=None):
        if not uuid and not tenant_uuid:
            return self.intra_pdps.values()
        elif uuid and uuid in self.intra_pdps:
            return self.intra_pdps[uuid]
        elif tenant_uuid:
            for ext in self.intra_pdps.values():
                if ext.tenant["uuid"] == tenant_uuid:
                    return ext
        elif tenant_name:
            for ext in self.intra_pdps.values():
                if ext.tenant["name"] == tenant_name:
                    return ext

    def get_users(self, extension_uuid=None, uuid=None, name=None):
        return self.intra_pdps[extension_uuid].get_subject(uuid=uuid, name=name)

    def get_objects(self, extension_uuid=None, uuid=None, name=None):
        return self.intra_pdps[extension_uuid].get_object(uuid=uuid, name=name)

    def get_roles(self, extension_uuid=None, uuid=None, name=None):
        return self.intra_pdps[extension_uuid].get_object_attributes(self, uuid=uuid, name=name, category="role")

    def get_groups(self, extension_uuid=None, uuid=None, name=None):
        return self.intra_pdps[extension_uuid].get_object_attributes(self, uuid=uuid, name=name, category="group")

manager = AdminManager()


def get_manager():
    return manager