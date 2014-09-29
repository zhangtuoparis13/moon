from uuid import uuid4
from moon.core.pdp.extension import Extension


tenant_intra_extension_mapping = {
    "admin": {
        "tenant_uuid": "",
        "intra_extension_uuids": []
    }
}


class SuperExtension:
    def __init__(self):
        self.__uuid = str(uuid4())
        self.__tenant_uuid = ""
        self.super_extension = Extension()
        # self.super_extension.load_from_json("path")

    def get_tenant_list(self):
        pass

    def get_intra_extension_list(self):
        pass

    def add_mapping(self, intra_extension_uuid, tenant_uuid):
        pass

    def del_mapping(self, intra_extension_uuid, tenant_uuid):
        pass


super_extension = SuperExtension()


def authz(subject_uuid, object_uuid, action):
    return super_extension.super_extension.authz(subject_uuid, object_uuid, action)


def manage(user_uuid, privilege):
    return super_extension.manage(user_uuid, privilege)
