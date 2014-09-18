from uuid import uuid4
try:
    from django.utils.safestring import mark_safe
except ImportError:
    mark_safe = str

from moon.core.pdp.sync_db import InterExtensionSyncer


class VirtualEntity:
    def __init__(self, type):
        self.__uuid = str(uuid4())
        self.__type = type
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

    def set_category_value_and_rule(self, requesting_cat_value_dict, requested_cat_value_dict):
        self.__requesting_subject_category_value_dict = requesting_cat_value_dict["subject_category_value_dict"]
        self.__requesting_object_category_value_dict = requesting_cat_value_dict["object_category_value_dict"]
        self.__requesting_rule_alist = requesting_cat_value_dict["rule"]
        self.__requested_subject_category_value_dict = requested_cat_value_dict["subject_category_value_dict"]
        self.__requested_object_category_value_dict = requested_cat_value_dict["object_category_value_dict"]
        self.__requested_rule_alist = requesting_cat_value_dict["rule"]

    def get_uuid(self):
        return self.__uuid

    def get_type(self):
        return self.__type

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
        _dict['type'] = self.__type
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
        self.__syncer = InterExtensionSyncer()

    def authz(self, sub, obj, act):
        for _vent in self.__vents.values():
            if self.requesting_intra_extension.authz(sub, _vent.get_uuid(), act) == "OK" and \
                    self.requested_intra_extension.authz(_vent.get_uuid(), obj, act) == "OK":
                return True
        return False

    def check_requesters(self, requesting_intra_extension_uuid, requested_intra_extension_uuid):
        if requesting_intra_extension_uuid == self.requesting_intra_extension.get_uuid() \
                and requested_intra_extension_uuid == self.requested_intra_extension.get_uuid():
            return True
        else:
            return False

    def create_collaboration(self, type, sub_list, obj_list, act):
        for _ve in self.__vents:
            if _ve.get_subjects() == sub_list and _ve.get_objects == obj_list and _ve.get_action() == act:
                return False

        _vent = VirtualEntity(type)
        _vent.set_subjects_objects_action(sub_list, obj_list, act)

        _requesting_cat_value_dict = self.requesting_intra_extension.create_requesting_collaboration(
            type, _vent.get_requesting_subject_list(), _vent.get_uuid(), _vent.get_action())
        _requested_cat_value_dict = self.requested_intra_extension.create_requested_collaboration(
            type, _vent.get_uuid(), _vent.get_requested_object_list(), _vent.get_action())

        _vent.set_category_value_and_rule(_requesting_cat_value_dict, _requested_cat_value_dict)
        self.__vents[_vent.get_uuid()] = _vent
        return _vent.get_uuid()

    def destroy_collaboration(self, vent_uuid):
        _vent = self.__vents[vent_uuid]
        self.requesting_intra_extension.destory_requesting_collaboration(_vent.get_type(), vent_uuid,
                                                                         _vent.get_requesting_subject_list(),
                                                                         _vent.get_requesting_subject_category_value_dict(),
                                                                         _vent.get_requesting_object_category_value_dict())
        self.requested_intra_extension.destory_requested_collaboration(_vent.get_type(), vent_uuid,
                                                                         _vent.get_requested_subject_category_value_dict(),
                                                                         _vent.get_requested_object_list(),
                                                                         _vent.get_requested_object_category_value_dict())
        self.__vents.pop(vent_uuid)

    def get_uuid(self):
        return self.__uuid

    def get_vent_data_dict(self, vent_uuid):
        return self.__vents[vent_uuid].get_data_dict()

    def get_vents(self):
        return self.__vents