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
        self.__requesting_subject_category_value_dict = requesting_cat_value_dict["subject_category_value"]
        self.__requesting_object_category_value_dict = requesting_cat_value_dict["object_category_value"]
        self.__requesting_rule_alist = requesting_cat_value_dict["rule"]
        self.__requested_subject_category_value_dict = requested_cat_value_dict["subject_category_value"]
        self.__requested_object_category_value_dict = requested_cat_value_dict["object_category_value"]
        self.__requested_rule_alist = requesting_cat_value_dict["rule"]

    def get_uuid(self):
        return self.__uuid

    def get_subjects(self):
        return self.__requesting_subject_list

    def get_objects(self):
        return self.__requested_object_list

    def get_action(self):
        return self.__action


class InterExtension:
    def __init__(self, requesting_intra_extension, requested_intra_extension):
        self.requesting_intra_extension = requesting_intra_extension
        self.requested_intra_extension = requested_intra_extension
        self.__uuid = str(uuid4())
        self.__vents = dict()
        self.__syncer = InterExtensionSyncer()

    def create_collaboration(self, type, sub_list, obj_list, act):
        for _ve in self.__vents:
            if _ve.get_subjects() == sub_list and _ve.get_objects == obj_list and _ve.get_action() == act:
                return False
            else:
                _vent = VirtualEntity(type)
                _vent.set_subjects_objects_action(sub_list, obj_list, act)

                _requesting_cat_value_dict = self.requesting_intra_extension.create_requesting_collaboration(
                    type, _vent.get_subjects(), _vent.get_uuid(), _vent.get_action())
                _requested_cat_value_dict = self.requested_intra_extension.create_requested_collaboration(
                    type, _vent.get_uuid(), _vent.get_objects(), _vent.get_action())

                _vent.set_category_value_and_rule(_requesting_cat_value_dict, _requested_cat_value_dict)
                self.__vents[_vent.get_uuid()] = _vent
                return True

    def authz(self, sub, obj, act):
        for _vent in self.__vents:
            if self.requesting_intra_extension(sub, _vent, act) and self.requested_intra_extension(_vent, obj, act):
                return True

    def get_uuid(self):
        return self.__uuid

    def check_requesters(self, requesting_intra_extension_uuid, requested_intra_extension_uuid):
        if requesting_intra_extension_uuid == self.requesting_intra_extension.get_uuid() \
                and requested_intra_extension_uuid == self.requested_intra_extension.get_uuid():
            return True
        else:
            return False