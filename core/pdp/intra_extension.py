import os.path
from uuid import uuid4
from moon.core.pdp.extension import Extension
from moon.core.pdp.sync_db import IntraExtensionSyncer



class IntraExtension:
    def __init__(self):
        self.__uuid = str(uuid4())
        self.__tenant_uuid = ""
        self.intra_extension_authz = Extension()
        self.intra_extension_admin = Extension()
        self.__syncer = IntraExtensionSyncer()

    def load_from_json(self, extension_setting_abs_dir):
        self.intra_extension_authz.load_from_json(os.path.join(extension_setting_abs_dir, 'authz'))
        self.intra_extension_admin.load_from_json(os.path.join(extension_setting_abs_dir, 'admin'))

    def get_data(self):
        data = dict()
        data["_id"] = self.__uuid
        data["tenant_uuid"] = self.__tenant_uuid
        data["authz"] = self.intra_extension_authz.get_data()
        data["admin"] = self.intra_extension_admin.get_data()
        return data

    def set_data(self, data):
        self.__uuid = data["_id"]
        self.__tenant_uuid = data["tenant_uuid"]
        self.intra_extension_authz.set_data(data["authz"])
        self.intra_extension_admin.set_data(data["admin"])

    def set_to_db(self):
        self.__syncer.set_to_db(self.get_data())

    def get_from_db(self, uuid):
        self.set_data(self.__syncer.get_from_db(uuid))

    def get_uuid(self):
        return str(self.__uuid)

    def get_tenant_uuid(self):
        return self.__tenant_uuid

    def authz(self, sub, obj, act):
        # authz_logger.warning('intra_extension/authz request: [sub {}, obj {}, act {}]'.format(sub, obj, act))
        return self.intra_extension_authz.authz(sub, obj, act)

    def admin(self, sub, obj, act):
        return self.intra_extension_admin.authz(sub, obj, act)

    def create_requesting_collaboration(self, type, subs, vent, act):
        if type == 'authz':
            self.intra_extension_authz.create_requesting_collaboration(subs, vent, act)
        elif type == 'admin':
            self.intra_extension_admin.create_requesting_collaboration(subs, vent, act)

    def create_requested_collaboration(self, type, vent, objs, act):
        if type == 'authz':
            self.intra_extension_authz.create_requested_collaboration(vent, objs, act)
        elif type == 'admin':
            self.intra_extension_admin.create_requested_collaboration(vent, objs, act)

    def __str__(self):
        return """IntraExtension {}
    subjects: {}
    objects: {}
        """.format(
            self.get_uuid(),
            self.intra_extension_authz.get_subjects(),
            self.intra_extension_authz.get_objects(),
        )
