# Copyright 2014 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os.path
from uuid import uuid4
from moon_server.core.pdp.extension import Extension
from moon_server.tools.sync_db import IntraExtensionSyncer


class IntraExtension:
    def __init__(self):
        self.__uuid = str(uuid4())
        self.__tenant_uuid = ""
        self.intra_extension_authz = Extension()
        self.intra_extension_admin = Extension()
        self.__syncer = IntraExtensionSyncer()
        self.__name = ""

    def load_from_json(self, extension_setting_abs_dir, name="Intra_Extension"):
        self.intra_extension_authz.load_from_json(os.path.join(extension_setting_abs_dir, 'authz'))
        self.intra_extension_admin.load_from_json(os.path.join(extension_setting_abs_dir, 'admin'))
        self.__name = name

    def get_uuid(self):
        return str(self.__uuid)

    def get_name(self):
        return self.__name

    def get_tenant_uuid(self):
        return self.__tenant_uuid

    def set_tenant_uuid(self, tenant_uuid):
        self.__tenant_uuid = tenant_uuid

    def authz(self, sub, obj, act):
        # authz_logger.warning('intra_extension/authz request: [sub {}, obj {}, act {}]'.format(sub, obj, act))
        return self.intra_extension_authz.authz(sub, obj, act)

    def admin(self, sub, obj, act):
        return self.intra_extension_admin.authz(sub, obj, act)

    def create_requesting_collaboration(self, genre, sub_list, vent_uuid, act):
        if genre == 'trust':
            return self.intra_extension_authz.create_requesting_collaboration(sub_list, vent_uuid, act)
        elif genre == 'coordinate':
            return self.intra_extension_admin.create_requesting_collaboration(sub_list, vent_uuid, act)

    def destroy_requesting_collaboration(self, genre, sub_list, vent_uuid, sub_cat_value, obj_cat_value):
        if genre == 'trust':
            return self.intra_extension_authz.destroy_requesting_collaboration(sub_list, vent_uuid,
                                                                               sub_cat_value, obj_cat_value)
        elif genre == 'coordinate':
            return self.intra_extension_admin.destroy_requesting_collaboration(sub_list, vent_uuid,
                                                                               sub_cat_value, obj_cat_value)

    def create_requested_collaboration(self, genre, vent_uuid, obj_list, act):
        if genre == 'trust':
            return self.intra_extension_authz.create_requested_collaboration(vent_uuid, obj_list, act)
        elif genre == 'coordinate':
            return self.intra_extension_admin.create_requested_collaboration(vent_uuid, obj_list, act)

    def destroy_requested_collaboration(self, genre, vent_uuid, obj_list, sub_cat_value_dict, obj_cat_value_dict):
        if genre == 'trust':
            return self.intra_extension_authz.destroy_requested_collaboration(vent_uuid, obj_list,
                                                                              sub_cat_value_dict, obj_cat_value_dict)
        elif genre == 'coordinate':
            return self.intra_extension_admin.destroy_requested_collaboration(vent_uuid, obj_list,
                                                                              sub_cat_value_dict, obj_cat_value_dict)

    def __str__(self):
        return """IntraExtension {} ({})
    subjects: {}
    objects: {}
        """.format(
            self.__name,
            self.get_uuid(),
            self.intra_extension_authz.get_subjects(),
            self.intra_extension_authz.get_objects(),
        )

    def get_data(self):
        data = dict()
        data["name"] = self.__name,
        data["_id"] = self.__uuid
        data["tenant_uuid"] = self.__tenant_uuid
        data["authz"] = self.intra_extension_authz.get_data()
        data["admin"] = self.intra_extension_admin.get_data()
        return data

    def set_data(self, data):
        self.__uuid = data["_id"]
        self.__name = data["name"]
        self.__tenant_uuid = data["tenant_uuid"]
        self.intra_extension_authz.set_data(data["authz"])
        self.intra_extension_admin.set_data(data["admin"])

    def backup_intra_extension_to_db(self):
        self.__syncer.backup_intra_extension_to_db(self.get_data())

    def load_from_db(self, uuid):
        self.set_data(self.__syncer.get_intra_extension_from_db(uuid))
