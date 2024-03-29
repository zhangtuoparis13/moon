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

from uuid import uuid4
from moon_server.tools.sync_db import InterExtensionSyncer


class VirtualEntity:
    def __init__(self):
        self.__uuid = str(uuid4())
        self.__requesting_subject_list = list()
        self.__requesting_subject_category_value_dict = dict()  # {cat_id, created_value}
        self.__requesting_object_category_value_dict = dict()  # {cat_id, created_value}
        self.__requesting_rule_alist = list()
        self.__requested_object_list = list()
        self.__requested_subject_category_value_dict = dict()  # {cat_id, created_value}
        self.__requested_object_category_value_dict = dict()  # {cat_id, created_value}
        self.__requested_rule_alist = list()
        self.__action = ''

    def set_subjects_objects_action(self, sub_list, obj_list, act):
        self.__requesting_subject_list = sub_list
        self.__requested_object_list = obj_list
        self.__action = act

    def set_category_values_and_rule(self, requesting_cat_value_dict, requested_cat_value_dict):
        self.__requesting_subject_category_value_dict = requesting_cat_value_dict["subject_category_value_dict"]
        self.__requesting_object_category_value_dict = requesting_cat_value_dict["object_category_value_dict"]
        self.__requesting_rule_alist = requesting_cat_value_dict["rule"]
        self.__requested_subject_category_value_dict = requested_cat_value_dict["subject_category_value_dict"]
        self.__requested_object_category_value_dict = requested_cat_value_dict["object_category_value_dict"]
        self.__requested_rule_alist = requesting_cat_value_dict["rule"]

    def get_uuid(self):
        return self.__uuid

    def get_requesting_subject_list(self):
        return self.__requesting_subject_list

    def get_requesting_subject_category_value_dict(self):
        return self.__requesting_subject_category_value_dict

    def get_requesting_object_category_value_dict(self):
        return self.__requesting_object_category_value_dict

    def get_requesting_rule_alist(self):
        return self.__requesting_rule_alist

    def get_requested_object_list(self):
        return self.__requested_object_list

    def get_requested_subject_category_value_dict(self):
        return self.__requested_subject_category_value_dict

    def get_requested_object_category_value_dict(self):
        return self.__requested_object_category_value_dict

    def get_requested_rule_alist(self):
        return self.__requested_rule_alist

    def get_action(self):
        return self.__action

    def get_data_dict(self):
        _dict = dict()
        _dict['uuid'] = self.__uuid
        _dict['requesting_subject_list'] = self.__requesting_subject_list
        _dict['requesting_subject_category_value_dict'] = self.__requesting_subject_category_value_dict
        _dict['requesting_object_category_value_dict'] = self.__requesting_object_category_value_dict
        _dict['requesting_rule_alist'] = self.__requesting_rule_alist
        _dict['requested_object_list'] = self.__requested_object_list
        _dict['requested_subject_category_value_dict'] = self.__requested_subject_category_value_dict
        _dict['requested_object_category_value_dict'] = self.__requested_object_category_value_dict
        _dict['requested_rule_alist'] = self.__requested_rule_alist
        _dict['action'] = self.__action
        return _dict


class InterExtension:
    def __init__(self, requesting_intra_extension, requested_intra_extension):
        self.requesting_intra_extension = requesting_intra_extension
        self.requested_intra_extension = requested_intra_extension
        self.__uuid = str(uuid4())
        self.__vents = dict()
        self.__vents["trust"] = list()
        self.__vents["coordinate"] = list()
        self.__syncer = InterExtensionSyncer()

    def authz(self, sub, obj, act):
        for _vent in self.__vents["trust"]:
            if self.requesting_intra_extension.authz(sub, _vent.get_uuid(), act) == "OK" and \
                    self.requested_intra_extension.authz(_vent.get_uuid(), obj, act) == "OK":
                return "OK"
        return "KO"

    def admin(self, sub, obj, act):
        for _vent in self.__vents["coordinate"]:
            if self.requesting_intra_extension.admin(sub, _vent.get_uuid(), act) == "OK" and \
                    self.requested_intra_extension.admin(_vent.get_uuid(), obj, act) == "OK":
                return "OK"
        return "KO"

    def check_requesters(self, requesting_intra_extension_uuid, requested_intra_extension_uuid):
        if requesting_intra_extension_uuid is self.requesting_intra_extension.get_uuid() \
                and requested_intra_extension_uuid is self.requested_intra_extension.get_uuid():
            return True
        else:
            return False

    def create_collaboration(self, genre, sub_list, obj_list, act):
        for _ve in self.__vents[genre]:
            if _ve.get_subjects() is sub_list and _ve.get_objects is obj_list and _ve.get_action() is act:
                return "[InterExtension Error] Create Collaboration: vEnt Exists"

        _vent = VirtualEntity()
        _vent.set_subjects_objects_action(sub_list, obj_list, act)

        _requesting_cat_value_dict = self.requesting_intra_extension.create_requesting_collaboration(
            genre, _vent.get_requesting_subject_list(), _vent.get_uuid(), _vent.get_action())
        _requested_cat_value_dict = self.requested_intra_extension.create_requested_collaboration(
            genre, _vent.get_uuid(), _vent.get_requested_object_list(), _vent.get_action())

        _vent.set_category_values_and_rule(_requesting_cat_value_dict, _requested_cat_value_dict)
        self.__vents[genre].append(_vent)
        return _vent.get_uuid()

    def destroy_collaboration(self, genre, vent_uuid):
        _vent = None
        for _tmp_vent in self.__vents[genre]:
            if _tmp_vent.get_uuid() == vent_uuid:
                _vent = _tmp_vent
                break
        if _vent is None:
            return "[InterExtension ERROR] Destroy Collaboration: No Success"

        self.requesting_intra_extension.destroy_requesting_collaboration(
            genre,
            _vent.get_requesting_subject_list(),
            _vent.get_uuid(),
            _vent.get_requesting_subject_category_value_dict(),
            _vent.get_requesting_object_category_value_dict()
        )

        self.requested_intra_extension.destroy_requested_collaboration(
            genre,
            _vent.get_uuid(),
            _vent.get_requested_object_list(),
            _vent.get_requested_subject_category_value_dict(),
            _vent.get_requested_object_category_value_dict()
        )

        self.__vents[genre].remove(_vent)
        return "[InterExtension] Destroy Collaboration: OK"

    def delegate(self, delegator_uuid, privilege):
        self.requesting_intra_extension.intra_extension_admin.add_subject(delegator_uuid)
        self.requested_intra_extension.intra_extension_admin.add_subject(delegator_uuid)
        if privilege == "list":
            _requesting_add = self.requesting_intra_extension.intra_extension_admin.add_subject_assignment(
                "role",
                delegator_uuid,
                "inter_extension_user")
            _requested_add = self.requested_intra_extension.intra_extension_admin.add_subject_assignment(
                "role",
                delegator_uuid,
                "inter_extension_user")
            if "ERROR" in _requesting_add or "ERROR" in _requested_add:
                return "[InterExtension ERROR]" + _requesting_add + " " + _requested_add
            else:
                return "[InterExtension] Delegate: Add Inter_Extension_User Privilege"
        elif privilege == "create" or privilege == "destroy":
            _requesting_add = self.requesting_intra_extension.intra_extension_admin.add_subject_assignment(
                "role",
                delegator_uuid,
                "inter_extension_admin")
            _requested_add = self.requested_intra_extension.intra_extension_admin.add_subject_assignment(
                "role",
                delegator_uuid,
                "inter_extension_admin")
            if "ERROR" in _requesting_add or "ERROR" in _requested_add:
                return "[InterExtension ERROR] " + \
                       _requesting_add + " " + \
                       _requested_add
            else:
                return "[InterExtension] Delegate: Add Inter_Extension_Admin Privilege"
        elif privilege == "delegate":
            _requesting_add = self.requesting_intra_extension.intra_extension_admin.add_subject_assignment(
                "role",
                delegator_uuid,
                "inter_extension_admin")
            _requested_add = self.requested_intra_extension.intra_extension_admin.add_subject_assignment(
                "role",
                delegator_uuid,
                "inter_extension_admin")
            if "ERROR" in _requesting_add or "ERROR" in _requested_add:
                return "[InterExtension ERROR] " + _requesting_add + " " + _requested_add
            else:
                return "[InterExtension] Delegate: Add Inter_Extension_Root Privilege"
        else:
            return "[InterExtension Error] Collaboration Delegate Unknown Privilege"

    def get_uuid(self):
        return self.__uuid

    def get_vent_data_dict(self, vent_uuid):
        if self.__vents["trust"][vent_uuid]:
            return self.__vents["trust"][vent_uuid].get_data_dict()
        elif self.__vents["coordinate"][vent_uuid]:
            return self.__vents["coordinate"][vent_uuid].get_data_dict()
        else:
            return False

    def get_vents(self):
        return self.__vents

    def get_data(self):
        data = dict()
        data["uuid"] = str(self.__uuid)
        data["requesting_intra_extension"] = self.requesting_intra_extension.get_data()
        data["requested_intra_extension"] = self.requested_intra_extension.get_data()
        data["vents"] = dict()
        data["vents"]["trust"] = map(lambda x: x.get_data_dict(), self.__vents["trust"])
        data["vents"]["coordinate"] = map(lambda x: x.get_data_dict(), self.__vents["coordinate"])
        return data