import json

class Metadata:
    def __init__(self, jsonfile):
        _json_data = json.loads(jsonfile.read())
        self.subject_categories = list()
        # examples: "role" , "security_level"
        self.object_categories = list()
        self.meta_rules = {
            'sub_meta_rules': [
                {
                    'subject_categories': [],
                    'object_categories': [],
                    'relation': ''
                }
            ],
            'aggregation': ''
        }


class Configuration:
    def __init__(self):
        self.subject_category_values = dict()
        # examples: { "role": {"admin", "dev", }, }
        self.object_category_values = dict()
        self.rules = list()


class Perimeter:
    def __init__(self):
        self.subjects = set()
        self.objects = set()


class Assignment:
    def __init__(self):
        self.subject_category_assignments = dict()
        # examples: { "role": {"user1": {"dev"}, "user2": {"admin",}}, }  TODO: limit to one value for each attr
        self.object_category_assignments = dict()


class AuthzData:
    def __init__(self, sub, obj, act):
        self.validation = "",  # "OK, KO, Out of Scope"  # "auth": False,
        self.subject = sub,  # subject,
        self.subject_attrs = dict(),
        self.object = obj,
        self.object_attrs = dict(),
        self.action = act,  # action,
        self.type = "",  # intra-tenant, inter-tenant, Out of Scope
        self.requesting_tenant = "",  # "subject_tenant": subject_tenant,
        self.requested_tenant = "",  # "object_tenant": object_tenant,
        # "tenant_name": "None",
        # "rule_name": "None",
        # "object_name": object_name,
        # "object_uuid": "",
        # "object_type": object_type,
        # "extension_name": "None"


class Extension:
    def __init__(self):
        self.__metadata = Metadata()
        self.__configuration = Configuration()
        self.__perimeter = Perimeter()
        self.__assignment = Assignment()

    def authz(self, sub, obj, act):
        authz_data = AuthzData(sub, obj, act)
        if authz_data.subject in self.__perimeter.subjects and authz_data.object in self.__perimeter.objects:
            authz_data.type = "intra-tenant"
            for sub_cat in self.__metadata.subject_categories:
                # authz_data.subject_attrs[sub_cat] = set(self.__assignment[sub_cat][sub])  TODO: limit to one value for each attr
                authz_data.subject_attrs[sub_cat] = self.__assignment[sub_cat][sub]

            for obj_cat in self.__metadata.object_categories:
                # authz_data.object_attrs[obj_cat] = set(self.__assignment[obj_cat][obj]) TODO: limit to one value for each attr
                authz_data.object_attrs[obj_cat] = self.__assignment[obj_cat][obj]

            _aggreation_args = []

            for sub_meta_rule in self.__metadata.meta_rules['sub_meta_rules']:
                _tmp_relation_args = []

                for tmp_sub_cat in sub_meta_rule["subject_categories"]:
                    _tmp_relation_args.append(authz_data.subject_attrs[tmp_sub_cat])

                for tmp_obj_cat in sub_meta_rule["object_categories"]:
                    _tmp_relation_args.append(authz_data.object_attrs[tmp_obj_cat])

                _relation_args = list()
                # _relation_agrs = _tmp_relation_args  TODO: find out the matrix solution in NumPy
                _relation_args[0] = _tmp_relation_args

                if sub_meta_rule['relation'] == 'relation_super':  # TODO: replace by Prolog
                    _relation_resulat = False
                    for _relation_arg in _relation_args:
                        if _relation_arg[0] > _relation_arg[1]:
                            _relation_resulat = True
                elif sub_meta_rule['relation'] == 'relation_equal_constant':
                    if _relation_arg[0] == 'READ':
                        _relation_resulat = True
                    else:
                        _relation_resulat = False
                _aggreation_args.append(_relation_resulat)

            if self.__metadata.meta_rules['aggregation'] == 'and_true_aggreation':
                authz_data.validation = True
                for _resulat in _aggreation_args:
                    if not _resulat:
                        authz_data.validation = False

            return authz_data.validation

        else:
            authz_data.validation = 'Out of Scope'


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
        return set(self.__perimeter.subjects)

    def add_subject(self, subject_id):
        self.__perimeter.subjects.add(subject_id)

    def del_subject(self, subject_id):  # TODO later
        pass

    def get_objects(self):
        return set(self.__perimeter.objects)

    def add_object(self, object_id):
        self.__perimeter.objects.add(object_id)

    def del_object(self, object_id):  # TODO later
        pass


# ---------------- assignment api ----------------

    def get_subject_assignments(self, category_id):
        pass

    def add_subject_assignment(self, category_id, subject_id, category_value):
        pass

    def del_subject_assignment(self, category_id, subject_id, category_value):
        pass

    def get_object_assignments(self, category_id):
        pass

    def add_object_assignment(self, category_id, object_id, category_value):
        pass

    def del_object_assignment(self, category_id, object_id, category_value):
        pass