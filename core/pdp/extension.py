class Metadata:
    def __init__(self):
        self.subject_categories = set()
        # examples: "role" , "security_level"
        self.object_categories = set()
        self.meta_rules = None


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
        # examples: { "role": {"user1": {"dev", "admin"}, "user2": {"admin",}}, }
        self.object_category_assignments = dict()


class Extension:
    def __init__(self):
        self.__metadata = Metadata()
        self.__configuration = Configuration()
        self.__perimeter = Perimeter()
        self.__assignment = Assignment()

    def authz(self, sub, obj, act):
        pass

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