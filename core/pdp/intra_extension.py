import os.path
from moon.core.pdp.extension import Extension
from uuid import uuid4


class IntraExtension:

    def __init__(self):
        self.__uuid = str(uuid4())
        self.intra_extension_authz = Extension()
        self.intra_extension_admin = Extension()

    def load_from_json(self, extension_setting_abs_dir):
        self.intra_extension_authz.load_from_json(os.path.join(extension_setting_abs_dir, 'authz'))
        # self.intra_extension_admin.load_from_json(os.path.join(extension_setting_abs_dir, 'admin'))

    def get_uuid(self):
        return str(self.__uuid)

    def get_name(self):
        return self.intra_extension_authz.metadata.get_name()

    def authz(self, sub, obj, act):
        return self.intra_extension_authz.authz(sub, obj, act)

    def admin(self, sub, obj, act):
        return self.intra_extension_admin.authz(sub, obj, act)
