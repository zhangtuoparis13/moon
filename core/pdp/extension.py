import os.path
import copy
import json
import itertools
from uuid import uuid4
from moon.tools.log import get_authz_logger


authz_logger = get_authz_logger()


class Metadata:

    def __init__(self):
        self.__name = ''
        self.__model = ''
        self.__genre = ''
        self.__description = ''
        self.__subject_categories = list()
        self.__object_categories = list()
        self.__meta_rule = dict()
        self.__meta_rule['sub_meta_rules'] = list()
        self.__meta_rule['aggregation'] = ''

    def load_from_json(self, extension_setting_dir):
        metadata_path = os.path.join(extension_setting_dir, 'metadata.json')
        f = open(metadata_path)
        json_metadata = json.load(f)
        self.__name = json_metadata['name']
        self.__model = json_metadata['model']
        self.__genre = json_metadata['genre']
        self.__description = json_metadata['description']
        self.__subject_categories = copy.deepcopy(json_metadata['subject_categories'])
        self.__object_categories = copy.deepcopy(json_metadata['object_categories'])
        self.__meta_rule = copy.deepcopy(json_metadata['meta_rule'])

    def get_name(self):
        return self.__name

    def get_genre(self):
        return self.__genre

    def get_subject_categories(self):
        return self.__subject_categories

    def get_object_categories(self):
        return self.__object_categories

    def get_meta_rule(self):
        return self.__meta_rule

    def get_meta_rule_aggregation(self):
        return self.__meta_rule['aggregation']

    def get_data(self):
        data = dict()
        data["name"] = self.get_name()
        data["model"] = self.__model
        data["genre"] = self.__genre
        data["description"] = self.__description
        data["subject_categories"] = self.get_subject_categories()
        data["object_categories"] = self.get_object_categories()
        data["meta_rule"] = dict(self.get_meta_rule())
        return data

    def set_data(self, data):
        self.__name = data["name"]
        self.__model = data["model"]
        self.__genre = data["genre"]
        self.__description = data["description"]
        self.__subject_categories = list(data["subject_categories"])
        self.__object_categories = list(data["object_categories"])
        self.__meta_rule = dict(data["meta_rule"])


class Configuration:
    def __init__(self):
        self.__subject_category_values = dict()
        # examples: { "role": {"admin", "dev", }, }
        self.__object_category_values = dict()
        self.__rules = list()

    def load_from_json(self, extension_setting_dir):
        configuration_path = os.path.join(extension_setting_dir, 'configuration.json')
        f = open(configuration_path)
        json_configuration = json.load(f)
        self.__subject_category_values = copy.deepcopy(json_configuration['subject_category_values'])
        self.__object_category_values = copy.deepcopy(json_configuration['object_category_values'])
        self.__rules = copy.deepcopy(json_configuration['rules'])  # TODO: currently a list, will be a dict with sub-meta-rule as key

    def get_subject_category_values(self):
        return self.__subject_category_values

    def get_object_category_values(self):
        return self.__object_category_values

    def get_rules(self):
        return self.__rules

    def get_data(self):
        data = dict()
        data["subject_category_values"] = self.get_subject_category_values()
        data["object_category_values"] = self.get_object_category_values()
        data["rules"] = self.get_rules()
        return data

    def set_data(self, data):
        self.__subject_category_values = list(data["subject_category_values"])
        self.__object_category_values = list(data["object_category_values"])
        self.__rules = list(data["rules"])


class Perimeter:
    def __init__(self):
        self.__subjects = list()
        self.__objects = list()

    def load_from_json(self, extension_setting_dir):
        perimeter_path = os.path.join(extension_setting_dir, 'perimeter.json')
        f = open(perimeter_path)
        json_perimeter = json.load(f)
        self.__subjects = copy.deepcopy(json_perimeter['subjects'])
        self.__objects = copy.deepcopy(json_perimeter['objects'])
        # print(self.__subjects)
        # print(self.__objects)

    def get_subjects(self):
        return self.__subjects

    def get_objects(self):
        return self.__objects

    def get_data(self):
        data = dict()
        data["subjects"] = self.get_subjects()
        data["objects"] = self.get_objects()
        return data

    def set_data(self, data):
        self.__subjects = list(data["subjects"])
        self.__objects = list(data["objects"])


class Assignment:
    def __init__(self):
        self.__subject_category_assignments = dict()
        # examples: { "role": {"user1": {"dev"}, "user2": {"admin",}}, }  TODO: limit to one value for each attr
        self.__object_category_assignments = dict()

    def load_from_json(self, extension_setting_dir):
        assignment_path = os.path.join(extension_setting_dir, 'assignment.json')
        f = open(assignment_path)
        json_assignment = json.load(f)

        self.__subject_category_assignments = dict(copy.deepcopy(json_assignment['subject_category_assignments']))
        self.__object_category_assignments = dict(copy.deepcopy(json_assignment['object_category_assignments']))

    def get_subject_category_assignments(self):
        return self.__subject_category_assignments

    def get_object_category_assignments(self):
        return self.__object_category_assignments

    def get_data(self):
        data = dict()
        data["subject_category_assignments"] = self.get_subject_category_assignments()
        data["object_category_assignments"] = self.get_object_category_assignments()
        return data

    def set_data(self, data):
        self.__subject_category_assignments = list(data["subject_category_assignments"])
        self.__object_category_assignments = list(data["object_category_assignments"])


class AuthzData:
    def __init__(self, sub, obj, act):
        self.validation = "False"  # "OK, KO, Out of Scope"  # "auth": False,
        self.subject = sub
        self.object = str(obj)
        self.action = str(act)
        self.type = ""  # intra-tenant, inter-tenant, Out of Scope
        self.subject_attrs = dict()
        self.object_attrs = dict()
        self.requesting_tenant = ""  # "subject_tenant": subject_tenant,
        self.requested_tenant = ""  # "object_tenant": object_tenant,

    def __str__(self):
        return """AuthzData:
        validation={}
        subject={}
        object={}
        action={}
        """.format(self.validation, self.subject, self.object, self.action)


class Extension:
    def __init__(self):
        self.metadata = Metadata()
        self.configuration = Configuration()
        self.perimeter = Perimeter()
        self.assignment = Assignment()

    def load_from_json(self, extension_setting_dir):
        self.metadata.load_from_json(extension_setting_dir)
        self.configuration.load_from_json(extension_setting_dir)
        self.perimeter.load_from_json(extension_setting_dir)
        self.assignment.load_from_json(extension_setting_dir)

    def get_name(self):
        return self.metadata.get_name()

    def get_genre(self):
        return self.metadata.get_genre()

    def authz(self, sub, obj, act):
        authz_data = AuthzData(sub, obj, act)
        authz_logger.warning('extension/authz request: [sub {}, obj {}, act {}]'.format(sub, obj, act))

        if authz_data.subject in self.perimeter.get_subjects() and authz_data.object in self.perimeter.get_objects():

            for subject_category in self.metadata.get_subject_categories():
                authz_data.subject_attrs[subject_category] = copy.copy(
                    self.assignment.get_subject_category_attr(subject_category, sub)
                )
                authz_logger.warning('extension/authz subject attribute: [subject attr: {}]'.format(
                    self.assignment.get_subject_category_attr(subject_category, sub))
                )

            for object_category in self.metadata.get_object_categories():
                if object_category == 'action':
                    authz_data.object_attrs[object_category] = [act]
                    authz_logger.warning('extension/authz object attribute: [object attr: {}]'.format([act]))
                else:
                    authz_data.object_attrs[object_category] = copy.copy(
                        self.assignment.get_object_category_attr(object_category, obj)
                    )
                    authz_logger.warning('extension/authz object attribute: [object attr: {}]'.format(
                        self.assignment.get_object_category_attr(object_category, obj))
                    )

            _aggregation_data = dict()

            for sub_meta_rule in self.metadata.get_meta_rule()["sub_meta_rules"].values():
                _tmp_relation_args = list()

                for sub_subject_category in sub_meta_rule["subject_categories"]:
                    _tmp_relation_args.append(authz_data.subject_attrs[sub_subject_category])

                for sub_object_category in sub_meta_rule["object_categories"]:
                    _tmp_relation_args.append(authz_data.object_attrs[sub_object_category])

                _relation_args = list(itertools.product(*_tmp_relation_args))

                if sub_meta_rule['relation'] == 'relation_super':  # TODO: replace by Prolog Engine
                    _aggregation_data['relation_super'] = dict()
                    _aggregation_data['relation_super']['result'] = False
                    for _relation_arg in _relation_args:
                        if list(_relation_arg) in self.configuration.get_rules()[sub_meta_rule['relation']]:
                            authz_logger.warning(
                                'extension/authz relation super OK: [sub_sl: {}, obj_sl: {}, action: {}]'.format(
                                    _relation_arg[0], _relation_arg[1], _relation_arg[2]
                                )
                            )
                            _aggregation_data['relation_super']['result'] = True
                            break
                    _aggregation_data['relation_super']['status'] = 'finished'

                elif sub_meta_rule['relation'] == 'permission':
                    _aggregation_data['permission'] = dict()
                    _aggregation_data['permission']['result'] = False
                    for _relation_arg in _relation_args:
                        if list(_relation_arg) in self.configuration.get_rules()[sub_meta_rule['relation']]:
                            authz_logger.warning(
                                'extension/authz relation permission OK: [role: {}, object: {}, action: {}]'.format(
                                    _relation_arg[0], _relation_arg[1], _relation_arg[2]
                                )
                            )
                            _aggregation_data['permission']['result'] = True
                            break
                    _aggregation_data['permission']['status'] = 'finished'

            if self.metadata.get_meta_rule_aggregation() == 'and_true_aggregation':
                authz_data.validation = "OK"
                for relation in _aggregation_data:
                    if _aggregation_data[relation]['status'] == 'finished' \
                            and _aggregation_data[relation]['result'] == False:
                        authz_data.validation = "KO"
        else:
            authz_data.validation = 'Out of Scope'

        return authz_data.validation

    # ---------------- metadate api ----------------

    def get_subject_categories(self):
        return self.metadata.get_subject_categories()

    def add_subject_category(self, category_id):
        if category_id in self.get_subject_categories():
            return False
        else:
            self.get_subject_categories().append(category_id)
            return self.get_subject_categories()

    def del_subject_category(self, category_id):
        if category_id in self.get_subject_categories():
            self.get_subject_categories().remove(category_id)
            return self.get_subject_categories()
        else:
            return False

    def get_object_categories(self):
        return self.metadata.get_object_categories()

    def add_object_category(self, category_id):
        if category_id in self.get_object_categories():
            return False
        else:
            self.get_object_categories().append(category_id)
            return self.get_object_categories()

    def del_object_category(self, category_id):
        if category_id in self.get_object_categories():
            self.get_object_categories().remove(category_id)
            return self.get_object_categories()
        else:
            return False

    def get_meta_rule(self):
        return self.metadata.get_meta_rule()

    # ---------------- configuration api ----------------

    def get_subject_category_values(self, category_id):
        return self.configuration.get_subject_category_values()[category_id]

    def add_subject_category_value(self, category_id, category_value):
        if category_value in self.configuration.get_subject_category_values()[category_id]:
            return False
        else:
            self.configuration.get_subject_category_values()[category_id].append(category_value)
            return self.configuration.get_subject_category_values()[category_id]

    def del_subject_category_value(self, category_id, category_value):
        if category_value in self.configuration.get_subject_category_values()[category_id]:
            self.configuration.get_subject_category_values()[category_id].remove(category_value)
            return self.configuration.get_subject_category_values()[category_id]
        else:
            return False

    def get_object_category_values(self, category_id):
        return self.configuration.get_object_category_values()[category_id]

    def add_object_category_value(self, category_id, category_value):
        if category_value in self.configuration.get_object_category_values()[category_id]:
            return False
        else:
            self.configuration.get_object_category_values()[category_id].append(category_value)
            return self.configuration.get_object_category_values()[category_id]

    def del_object_category_value(self, category_id, category_value):
        if category_value in self.configuration.get_object_category_values()[category_id]:
            self.configuration.get_object_category_values()[category_id].remove(category_value)
            return self.configuration.get_object_category_values()[category_id]
        else:
            return False

    def get_rules(self):
        return self.configuration.get_rules()

    def add_rule(self, sub_cat_value_dict, obj_cat_value_dict):
        for _relation in self.metadata.get_meta_rule()["sub_meta_rules"]:
            _sub_rule = list()
            for sub_subject_category in self.metadata.get_meta_rule()["sub_meta_rules"][_relation]["subject_categories"]:
                if sub_cat_value_dict[_relation][sub_subject_category] \
                        in self.configuration.get_subject_category_values()[sub_subject_category]:
                    _sub_rule.append(sub_cat_value_dict[_relation][sub_subject_category])
                else:
                    return "[Error] Added Subject Category Value Unknown"

            for sub_object_category in self.metadata.get_meta_rule()["sub_meta_rules"][_relation]["object_categories"]:
                if obj_cat_value_dict[_relation][sub_object_category] \
                        in self.configuration.get_object_category_values()[sub_object_category]:
                    _sub_rule.append(obj_cat_value_dict[_relation][sub_object_category])
                else:
                    return "[Error] Added Object Category Value Unknown"

            if _sub_rule in self.configuration.get_rules()[_relation]:
                return "[Error] Added Rule Exists"
            else:
                self.configuration.get_rules()[_relation].append(_sub_rule)
        return self.configuration.get_rules()

    def del_rule(self, sub_cat_value_dict, obj_cat_value_dict):
        for _relation in self.metadata.get_meta_rule()["sub_meta_rules"]:
            _sub_rule = list()
            for sub_subject_category in self.metadata.get_meta_rule()["sub_meta_rules"][_relation]["subject_categories"]:
                _sub_rule.append(sub_cat_value_dict[_relation][sub_subject_category])

            for sub_object_category in self.metadata.get_meta_rule()["sub_meta_rules"][_relation]["object_categories"]:
                _sub_rule.append(obj_cat_value_dict[_relation][sub_object_category])

            if _sub_rule in self.configuration.get_rules()[_relation]:
                self.configuration.get_rules()[_relation].remove(_sub_rule)
            else:
                return "[Error] Deleted Rule No Exists"
        return self.configuration.get_rules()

    # ---------------- perimeter api ----------------

    def get_subjects(self):
        return self.perimeter.get_subjects()

    def add_subject(self, subject_id):
        if subject_id in self.perimeter.get_subjects():
            return "[ERROR] Added Subject Exists"
        else:
            self.perimeter.get_subjects().append(subject_id)
            return self.perimeter.get_subjects()

    def del_subject(self, subject_id):
        if subject_id in self.perimeter.get_subjects():
            self.perimeter.get_subjects().remove(subject_id)
            return self.perimeter.get_subjects()
        else:
            return "[ERROR] Deleted Subject No Exists"

    def get_objects(self):
        return self.perimeter.get_objects()

    def add_object(self, object_id):
        if object_id in self.perimeter.get_objects():
            return "[ERROR] Added Object Exists"
        else:
            self.perimeter.get_objects().append(object_id)
            return self.perimeter.get_objects()

    def del_object(self, object_id):
        if object_id in self.perimeter.get_objects():
            self.perimeter.get_objects().remove(object_id)
            return self.perimeter.get_objects()
        else:
            return "[ERROR] Deleted Object No Exists"

    # ---------------- assignment api ----------------

    def get_subject_assignments(self, category_id):
        if category_id in self.metadata.get_subject_categories():
            return self.assignment.get_subject_category_assignments()[category_id]
        else:
            return "[ERROR] Get Subject Assignment: Unknown Subject Category"

    def add_subject_assignment(self, category_id, subject_id, category_value):
        if category_id in self.metadata.get_subject_categories():
            if subject_id in self.perimeter.get_subjects():
                if category_value in self.configuration.get_subject_category_values()[category_id]:
                    if category_value in self.assignment.get_subject_category_assignments()[category_id][subject_id]:
                        return "[ERROR] Add Subject Assignment: Subject Assignment Exists"
                    else:
                        if subject_id in self.assignment.get_subject_category_assignments()[category_id]:
                            self.assignment.get_subject_category_assignments()[category_id][subject_id].extend([category_value])
                        else:
                            self.assignment.get_subject_category_assignments()[category_id][subject_id] = [category_value]
                        return self.assignment.get_subject_category_assignments()
                else:
                    return "[ERROR] Add Subject Assignment: Unknown Subject Category Value"
            else:
                return "[ERROR] Add Subject Assignment: Unknown Subject"
        else:
            return "[ERROR] Add Subject Assignment: Unknown Subject Category"

    def del_subject_assignment(self, category_id, subject_id, category_value):
        if category_id in self.metadata.get_subject_categories():
            if subject_id in self.perimeter.get_subjects():
                if category_value in self.configuration.get_subject_category_values()[category_id]:
                    if len(self.assignment.get_subject_category_assignments()[category_id][subject_id]) >= 2:
                        self.assignment.get_subject_category_assignments()[category_id][subject_id].remove(category_value)
                    else:
                        self.assignment.get_subject_category_assignments()[category_id].pop(subject_id)
                    return self.assignment.get_subject_category_assignments()
                else:
                    return "[ERROR] Del Subject Assignment: Assignment No Exists"
            else:
                return "[ERROR] Del Subject Assignment: Unknown Subject"
        else:
            return "[ERROR] Del Subject Assignment: Unknown Subject Category"

    def get_object_assignments(self, category_id):
        if category_id in self.metadata.get_object_categories():
            return self.assignment.get_object_category_assignments()[category_id]
        else:
            return "[ERROR] Get Object Assignment: Unknown Object Category"

    def add_object_assignment(self, category_id, object_id, category_value):
        if category_id in self.metadata.get_object_categories():
            if object_id in self.perimeter.get_objects():
                if category_value in self.configuration.get_object_category_values()[category_id]:
                    if category_value in self.assignment.get_object_category_assignments()[category_id][object_id]:
                        return "[ERROR] Add Object Assignment: Object Assignment Exists"
                    else:
                        if object_id in self.assignment.get_object_category_assignments()[category_id]:
                            self.assignment.get_object_category_assignments()[category_id][object_id].extend([category_value])
                        else:
                            self.assignment.get_object_category_assignments()[category_id][object_id] = [category_value]
                        return self.assignment.get_object_category_assignments()
                else:
                    return "[ERROR] Add Object Assignment: Unknown Object Category Value"
            else:
                return "[ERROR] Add Object Assignment: Unknown Object"
        else:
            return "[ERROR] Add Object Assignment: Unknown Object Category"

    def del_object_assignment(self, category_id, object_id, category_value):
        if category_id in self.metadata.get_object_categories():
            if object_id in self.perimeter.get_objects():
                if category_value in self.configuration.get_object_category_values()[category_id]:
                    if len(self.assignment.get_object_category_assignments()[category_id][object_id]) >= 2:
                        self.assignment.get_object_category_assignments()[category_id][object_id].remove(category_value)
                    else:
                        self.assignment.get_object_category_assignments()[category_id].pop(object_id)
                    return self.assignment.get_object_category_assignments()
                else:
                    return "[ERROR] Del Object Assignment: Assignment No Exists"
            else:
                return "[ERROR] Del Object Assignment: Unknown Object"
        else:
            return "[ERROR] Del Object Assignment: Unknown Object Category"

# ---------------- SyncDB API ----------------

    def get_data(self):
        data = dict()
        data["metadata"] = self.metadata.get_data()
        data["configuration"] = self.configuration.get_data()
        data["perimeter"] = self.perimeter.get_data()
        data["assignment"] = self.assignment.get_data()
        return data

    def set_data(self, extension_data):
        self.metadata.set_data(extension_data["metadata"])
        self.configuration.set_data(extension_data["configuration"])
        self.perimeter.set_data(extension_data["perimeter"])
        self.assignment.set_data(extension_data["assignment"])

# ---------------- inter-extension API ----------------

    def create_requesting_collaboration(self, sub_list, vent_uuid, act):
        _sub_cat_values = dict()
        _obj_cat_values = dict()

        for _sub_cat_id in self.get_subject_categories():
            _sub_cat_value = str(uuid4())
            self.add_subject_category_value(_sub_cat_id, _sub_cat_value)
            _sub_cat_values[_sub_cat_id] = _sub_cat_value

            for _sub in sub_list:
                self.add_subject_assignment(_sub_cat_id, _sub, _sub_cat_value)

        self.add_object(vent_uuid)

        for _obj_cat_id in self.get_object_categories():
            if _obj_cat_id == 'action':
                _obj_cat_values[_obj_cat_id] = act
            else:
                _obj_cat_value = str(uuid4())
                self.add_object_category_value(_obj_cat_id, _obj_cat_value)
                _obj_cat_values[_obj_cat_id] = _obj_cat_value
                self.add_object_assignment(_obj_cat_id, vent_uuid, _obj_cat_value)

        _rule = self.add_rule(_sub_cat_values, _obj_cat_values)
        return {"subject_category_value_dict": _sub_cat_values, "object_category_value_dict": _obj_cat_values, "rule": _rule}

    def destroy_requesting_collaboration(self, vent_uuid, sub_list, sub_cat_value_dict, obj_cat_value_dict):
        for _sub_cat_id in self.get_subject_categories():
            self.del_subject_category_value(_sub_cat_id, sub_cat_value_dict[_sub_cat_id])

            for _sub in sub_list:
                self.del_subject_assignment(_sub_cat_id, _sub, sub_cat_value_dict[_sub_cat_id])

        self.del_object(vent_uuid)

        for _obj_cat_id in self.get_object_categories():
            if _obj_cat_id == "action":
                pass  # TODO: reconsidering the action as object attribute
            else:
                self.del_object_category_value(_obj_cat_id, obj_cat_value_dict[_obj_cat_id])
                self.del_object_assignment(_obj_cat_id, vent_uuid, obj_cat_value_dict[_obj_cat_id])

        self.del_rule(sub_cat_value_dict, obj_cat_value_dict)

    def create_requested_collaboration(self, vent_uuid, obj_list, act):
        _sub_cat_values = dict()
        _obj_cat_values = dict()

        self.add_subject(vent_uuid)

        for _sub_cat_id in self.get_subject_categories():
            _sub_cat_value = str(uuid4())
            self.add_subject_category_value(_sub_cat_id, _sub_cat_value)
            _sub_cat_values[_sub_cat_id] = _sub_cat_value
            self.add_subject_assignment(_sub_cat_id, vent_uuid, _sub_cat_value)

        for _obj_cat_id in self.get_object_categories():
            if _obj_cat_id == 'action':
                _obj_cat_values[_obj_cat_id] = act
            else:
                _obj_cat_value = str(uuid4())
                self.add_object_category_value(_obj_cat_id, _obj_cat_value)
                _obj_cat_values[_obj_cat_id] = _obj_cat_value
                for _obj in obj_list:
                    self.add_object_assignment(_obj_cat_id, _obj, _obj_cat_value)

        _rule = self.add_rule(_sub_cat_values, _obj_cat_values)
        return {"subject_category_value_dict": _sub_cat_values, "object_category_value_dict": _obj_cat_values, "rule": _rule}

    def destroy_requested_collaboration(self, vent_uuid, sub_cat_value_dict, obj_list, obj_cat_value_dict):
        self.del_subject(vent_uuid)

        for _sub_cat_id in self.get_subject_categories():
            self.del_subject_category_value(_sub_cat_id, sub_cat_value_dict[_sub_cat_id])
            self.del_subject_assignment(_sub_cat_id, vent_uuid, sub_cat_value_dict[_sub_cat_id])

        for _obj_cat_id in self.get_object_categories():
            if _obj_cat_id == "action":
                pass  # TODO: reconsidering the action as object attribute
            else:
                self.del_object_category_value(_obj_cat_id, obj_cat_value_dict[_obj_cat_id])

                for _obj in obj_list:
                    self.del_object_assignment(_obj_cat_id, _obj, obj_cat_value_dict[_obj_cat_id])

        self.del_rule(sub_cat_value_dict, obj_cat_value_dict)