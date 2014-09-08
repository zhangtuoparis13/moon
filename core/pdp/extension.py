import os.path
import copy
import json
import itertools


class Metadata:
    def __init__(self):
        self.__name = ''
        self.__model = ''
        self.__type = ''
        self.__description = ''
        self.__subject_categories = set()
        self.__object_categories = set()
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
        # print(self.__subject_category_values)
        # print(self.__object_category_values)
        # print(self.__rules)


class Perimeter:
    def __init__(self):
        self.__subjects = set()
        self.__objects = set()

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


class Assignment:
    def __init__(self):
        self.__subject_category_assignments = dict()
        # examples: { "role": {"user1": {"dev"}, "user2": {"admin",}}, }  TODO: limit to one value for each attr
        self.__object_category_assignments = dict()

    def load_from_json(self, extension_setting_dir):
        assignment_path = os.path.join(extension_setting_dir, 'assignment.json')
        f = open(assignment_path)
        json_assignment = json.load(f)

        self.__subject_category_assignments = dict(copy.deepcopy(json_assignment['subject_category_assignment']))
        self.__object_category_assignments = dict(copy.deepcopy(json_assignment['object_category_assignment']))
        # print(self.__subject_category_assignments)
        # print(self.__object_category_assignments)

    def get_subject_category_assignments(self):
        return self.__subject_category_assignments

    def get_subject_category_attr(self, subject_category, subject):
        return self.__subject_category_assignments[subject_category][subject]

    def get_object_category_assignments(self):
        return self.__object_category_assignments

    def get_object_category_attr(self, object_category, obj):
        return self.__object_category_assignments[object_category][obj]


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

    def authz(self, sub, obj, act):
        authz_data = AuthzData(sub, obj, act)

        if authz_data.subject in self.perimeter.get_subjects() and authz_data.object in self.perimeter.get_objects():
            authz_data.type = "intra-tenant"

            for subject_category in self.metadata.get_subject_categories():
                authz_data.subject_attrs[subject_category] = copy.copy(self.assignment.get_subject_category_attr(subject_category, sub))

            for object_category in self.metadata.get_object_categories():
                authz_data.object_attrs[object_category] = copy.copy(self.assignment.get_object_category_attr(object_category, obj))

            _aggreation_args = list()

            for sub_meta_rule in self.metadata.get_meta_rule_sub_meta_rules():  # sub_meta_rules is a list
                _tmp_relation_args = list()

                for sub_subject_category in sub_meta_rule["subject_categories"]:
                    _tmp_relation_args.append(authz_data.subject_attrs[sub_subject_category])

                for sub_object_category in sub_meta_rule["object_categories"]:
                    _tmp_relation_args.append(authz_data.object_attrs[sub_object_category])

                _relation_args = list(itertools.product(*_tmp_relation_args))
                print('_relation_args', _relation_args)

                if sub_meta_rule['relation'] == 'relation_super':  # TODO: replace by Prolog Engine
                    for _relation_arg in _relation_args:
                        if int(_relation_arg[0]) > int(_relation_arg[1]):
                            _resulat = True
                            break
                        else:
                            _resulat = False

                elif sub_meta_rule['relation'] == 'relation_equal_constant':
                    for _relation_arg in _relation_args:
                        if _relation_arg[0] == 'read':
                            _resulat = True
                            break
                        else:
                            _resulat = False

                _aggreation_args.append(_resulat)

            if self.metadata.get_meta_rule_aggregation() == 'and_true_aggregation':
                authz_data.validation = True
                for _resulat in _aggreation_args:
                    if not _resulat:
                        authz_data.validation = False
        else:
            authz_data.validation = 'Out of Scope'

        return authz_data.validation

# ---------------- metadate api ----------------

    def get_subject_categories(self):
        return set(self.__metadata.subject_categories)

    def add_subject_category(self, category_id):
        self.__metadata.subject_categories.add(category_id)

    def del_subject_category(self, category_id):
        self.__metadata.subject_categories.remove(category_id)

    def get_object_categories(self):
        return set(self.__metadata.object_categories)

    def add_object_category(self, category_id):
        self.__metadata.object_categories.add(category_id)

    def del_object_category(self, category_id):
        self.__metadata.object_categories.remove(category_id)

# ---------------- configuration api ----------------

    def get_subject_category_values(self, category_id):
        return set(self.__configuration.subject_category_values[category_id])

    def add_subject_category_values(self, category_id, category_value):
        self.__configuration.subject_category_values[category_id].add(category_value)

    def del_subject_category_values(self, category_id, category_value):  # TODO later
        pass

    def get_object_category_values(self, category_id):
        return set(self.__configuration.object_category_values[category_id])

    def add_object_category_values(self, category_id, category_value):
        self.__configuration.object_category_values[category_id].add(category_value)

    def del_object_category_values(self, category_id, category_value):  # TODO later
        pass

    def get_rules(self):
        return set(self.__configuration.rules)

    def add_rules(self):  # TODO  later
        pass

    def del_rules(self):  # TODO later
        pass

# ---------------- perimeter api ----------------

    def get_subjects(self):
        return set(self.perimeter.get_subjects())

    def add_subject(self, subject_id):
        self.__perimeter.subjects.add(subject_id)

    def del_subject(self, subject_id):  # TODO later
        pass

    def get_objects(self):
        return set(self.perimeter.get_objects())

    def add_object(self, object_id):
        self.__perimeter.objects.add(object_id)

    def del_object(self, object_id):  # TODO later
        pass

# ---------------- assignment api ----------------

    def get_subject_assignments(self, category_id):
        return self.get_subject_assignments(category_id)

    def add_subject_assignment(self, category_id, subject_id, category_value):
        pass

    def del_subject_assignment(self, category_id, subject_id, category_value):
        pass

    def get_subject_attr(self, category_id, subject_id):
        return self.get_subject_attr(category_id, subject_id)

    def get_object_assignments(self, category_id):
        return self.get_object_assignments(category_id)

    def add_object_assignment(self, category_id, object_id, category_value):
        pass

    def del_object_assignment(self, category_id, object_id, category_value):
        pass

    def get_object_attr(self, category_id, object_id):
        return self.get_object_attr(category_id, object_id)
