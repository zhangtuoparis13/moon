import os.path
import copy
import json
import itertools
from uuid import uuid4
from moon.log_repository import authz_logger


class Metadata:
    def __init__(self):
        self.__name = ''
        self.__model = ''
        self.__type = ''
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
        self.__type = json_metadata['type']
        self.__description = json_metadata['description']
        self.__subject_categories = copy.deepcopy(json_metadata['subject_categories'])
        self.__object_categories = copy.deepcopy(json_metadata['object_categories'])
        self.__meta_rule = copy.deepcopy(json_metadata['meta_rule'])

        # self.__meta_rule['aggregation'] = json_metadata['meta_rule']['aggregation']
        # for sub_rule in json_metadata['meta_rule']['sub_meta_rules']:
        #     tmp_sub_rule = dict()
        #     tmp_sub_rule['subject_categories'] = copy.deepcopy(sub_rule['subject_categories'])
        #     tmp_sub_rule['object_categories'] = copy.deepcopy(sub_rule['object_categories'])
        #     tmp_sub_rule['relation'] = sub_rule['relation']
        #     self.__meta_rule['sub_meta_rules'].append(tmp_sub_rule)

    def get_name(self):
        return self.__name

    def get_subject_categories(self):
        return self.__subject_categories

    def get_object_categories(self):
        return self.__object_categories

    def get_meta_rule_aggregation(self):
        return self.__meta_rule['aggregation']

    def get_meta_rule_sub_meta_rules(self):
        return self.__meta_rule['sub_meta_rules']

    def get_data(self):
        data = dict()
        data["name"] = self.get_name()
        data["model"] = self.__model
        data["type"] = self.__type
        data["description"] = self.__description
        data["subject_categories"] = self.get_subject_categories()
        data["object_categories"] = self.get_object_categories()
        data["meta_rule"] = dict()
        data["meta_rule"]["sub_meta_rules"] = self.get_meta_rule_sub_meta_rules()
        data["meta_rule"]["aggregation"] = self.get_meta_rule_aggregation()
        return data

    def set_data(self, data):
        self.__name = data["name"]
        self.__model = data["model"]
        self.__type = data["type"]
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
        self.__rules = copy.deepcopy(json_configuration['rules'])

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
        data["object"] = self.get_objects()
        return data

    def set_data(self, data):
        self.__subjects = list(data["subjects"])
        self.__objects = list(data["object"])


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

    def get_subject_category_attr(self, subject_category, subject):
        return self.__subject_category_assignments[subject_category][subject]

    def get_object_category_assignments(self):
        return self.__object_category_assignments

    def get_object_category_attr(self, object_category, obj):
        return self.__object_category_assignments[object_category][obj]

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


class VirtualEntity:
    def __init__(self, type):
        self.__uuid = str(uuid4())
        self.__type = type

    def get_uuid(self):
        return self.__uuid


class Extension:
    def __init__(self):
        self.metadata = Metadata()
        self.configuration = Configuration()
        self.perimeter = Perimeter()
        self.assignment = Assignment()

    def get_name(self):
        self.metadata.get_name()

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

    def load_from_json(self, extension_setting_dir):
        self.metadata.load_from_json(extension_setting_dir)
        self.configuration.load_from_json(extension_setting_dir)
        self.perimeter.load_from_json(extension_setting_dir)
        self.assignment.load_from_json(extension_setting_dir)

    def authz(self, sub, obj, act):
        authz_data = AuthzData(sub, obj, act)
        authz_logger.warning('extension/authz request: [sub {}, obj {}, act {}]'.format(sub, obj, act))

        if authz_data.subject in self.perimeter.get_subjects() and authz_data.object in self.perimeter.get_objects():
            authz_data.type = "intra-tenant"

            for subject_category in self.metadata.get_subject_categories():
                authz_data.subject_attrs[subject_category] = copy.copy(self.assignment.get_subject_category_attr(subject_category, sub))
                authz_logger.warning('extension/authz subject attribute: [subject attr: {}]'.format(self.assignment.get_subject_category_attr(subject_category, sub)))

            for object_category in self.metadata.get_object_categories():
                if object_category == 'action':
                    authz_data.object_attrs[object_category] = [act]
                    authz_logger.warning('extension/authz object attribute: [object attr: {}]'.format([act]))
                else:
                    authz_data.object_attrs[object_category] = copy.copy(self.assignment.get_object_category_attr(object_category, obj))
                    authz_logger.warning('extension/authz object attribute: [object attr: {}]'.format(self.assignment.get_object_category_attr(object_category, obj)))

            _aggregation_data = dict()

            for sub_meta_rule in self.metadata.get_meta_rule_sub_meta_rules():  # sub_meta_rules is a list
                _tmp_relation_args = list()

                for sub_subject_category in sub_meta_rule["subject_categories"]:
                    _tmp_relation_args.append(authz_data.subject_attrs[sub_subject_category])

                for sub_object_category in sub_meta_rule["object_categories"]:
                    _tmp_relation_args.append(authz_data.object_attrs[sub_object_category])

                _relation_args = list(itertools.product(*_tmp_relation_args))
                # print('_relation_args: ', _relation_args)

                if sub_meta_rule['relation'] == 'relation_super':  # TODO: replace by Prolog Engine
                    _aggregation_data['relation_super'] = dict()
                    _aggregation_data['relation_super']['result'] = False
                    for _relation_arg in _relation_args:
                        if list(_relation_arg) in self.configuration.get_rules():
                            authz_logger.warning('extension/authz relation super OK: [sub_sl: {}, obj_sl: {}, action: {}]'.format(_relation_arg[0], _relation_arg[1], _relation_arg[2]))
                            _aggregation_data['relation_super']['result'] = True
                            break
                    _aggregation_data['relation_super']['status'] = 'finished'

                elif sub_meta_rule['relation'] == 'permission':
                    _aggregation_data['permission'] = dict()
                    _aggregation_data['permission']['result'] = False
                    for _relation_arg in _relation_args:
                        if list(_relation_arg) in self.configuration.get_rules():
                            authz_logger.warning('extension/authz relation permission OK: [role: {}, object: {}, action: {}]'.format(_relation_arg[0], _relation_arg[1], _relation_arg[2]))
                            _aggregation_data['permission']['result'] = True
                            break
                    _aggregation_data['permission']['status'] = 'finished'

            if self.metadata.get_meta_rule_aggregation() == 'and_true_aggregation':
                authz_data.validation = True
                for relation in _aggregation_data:
                    if _aggregation_data[relation]['status'] == 'finished' and _aggregation_data[relation]['result'] == False:
                        authz_data.validation = False
        else:
            authz_data.validation = 'Out of Scope'

        return authz_data.validation

# ---------------- metadate api ----------------

    def get_subject_categories(self):
        return self.metadata.get_subject_categories()

    def add_subject_category(self, category_id):
        self.get_subject_categories().append(category_id)

    def del_subject_category(self, category_id):
        self.get_subject_categories().remove(category_id)

    def get_object_categories(self):
        return self.get_object_categories()

    def add_object_category(self, category_id):
        self.get_object_categories().append(category_id)

    def del_object_category(self, category_id):
        self.get_object_categories().remove(category_id)

# ---------------- configuration api ----------------

    def get_subject_category_values(self, category_id):
        return self.configuration.get_subject_category_values()[category_id]

    def add_subject_category_value(self, category_id, category_value):
        self.configuration.get_subject_category_values()[category_id].append(category_value)

    def del_subject_category_value(self, category_id, category_value):  # TODO later
        pass

    def get_object_category_values(self, category_id):
        return self.configuration.get_object_category_values()[category_id]

    def add_object_category_value(self, category_id, category_value):
        self.configuration.get_object_category_values()[category_id].append(category_value)

    def del_object_category_value(self, category_id, category_value):  # TODO later
        pass

    def get_rules(self):
        return self.get_rules()

    def add_rule(self):  # TODO  later
        pass

    def del_rule(self):  # TODO later
        pass

# ---------------- perimeter api ----------------

    def get_subjects(self):
        return self.perimeter.get_subjects()

    def add_subject(self, subject_id):
        self.perimeter.get_objects().append(subject_id)

    def del_subject(self, subject_id):  # TODO later
        pass

    def get_objects(self):
        return self.perimeter.get_objects()

    def add_object(self, object_id):
        self.perimeter.get_objects().append(object_id)

    def del_object(self, object_id):  # TODO later
        pass

# ---------------- assignment api ----------------

    def get_subject_assignments(self, category_id):
        return self.assignment.get_subject_category_assignments()[category_id]

    def add_subject_assignment(self, category_id, subject_id, category_value):
        if subject_id in self.assignment.get_subject_category_assignments()[category_id]:
            self.assignment.get_subject_category_assignments()[category_id][subject_id].append(category_value)
        else:
            self.assignment.get_subject_category_assignments()[category_id][subject_id] = list(category_id)

    def del_subject_assignment(self, category_id, subject_id, category_value):
        self.assignment.get_subject_category_assignments()[category_id][subject_id].remove(category_value)

    def get_subject_attr(self, category_id, subject_id):
        return self.get_subject_attr(category_id, subject_id)

    def get_object_assignments(self, category_id):
        return self.assignment.get_object_category_assignments()[category_id]

    def add_object_assignment(self, category_id, object_id, category_value):
        if object_id in self.assignment.get_object_category_assignments()[category_id]:
            self.assignment.get_object_category_assignments()[category_id][object_id].append(category_value)
        else:
            self.assignment.get_object_category_assignments()[category_id][object_id] = list(category_id)

    def del_object_assignment(self, category_id, object_id, category_value):
        self.assignment.get_object_category_assignments()[category_id][object_id].remove(category_value)

    def get_object_attr(self, category_id, object_id):
        return self.get_object_attr(category_id, object_id)
