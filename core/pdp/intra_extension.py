import os.path
from moon.core.pdp.extension import Extension
from moon.core.pdp.sync_db import Intra_Extension_Syncer

class IntraExtension():
    def __init__(self):
        self.__intra_extension_authz = Extension()
        self.__intra_extension_admin = Extension()
        self.__syncer = Intra_Extension_Syncer()

    def load_from_json(self, extension_setting_abs_dir):
        self.__intra_extension_authz.load_from_json(os.path.join(extension_setting_abs_dir, 'authz'))
        # self.intra_extension_admin.load_from_json(os.path.join(extension_setting_abs_dir, 'admin'))

    def get_data(self):
        data = dict()
        data["name"] = self.__intra_extension_authz.get_name()
        data["authz"] = self.__intra_extension_authz.get_data()
        data["admin"] = self.__intra_extension_admin.get_data()

    def sync(self):
        self.__syncer.sync(self.get_data())

    def get_name(self):
        return self.__intra_extension_authz.metadata.get_name()

    def authz(self, sub, obj, act):
        return self.__intra_extension_authz.authz(sub, obj, act)

    def admin(self, sub, obj, act):
        return self.__intra_extension_admin.authz(sub, obj, act)
