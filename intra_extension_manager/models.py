from uuid import uuid4
try:
    from django.utils.safestring import mark_safe
except ImportError:
    mark_safe = str


class Extension:

    def __init__(
            self,
            name="",
            uuid=None,
            subjects=None,
            objects=None,
            metadata=None,
            rules=None,
            profiles=None,
            description="",
            tenant=None):
        self.name = name,
        if not uuid:
            self.uuid = str(uuid4()).replace("-", "")
        else:
            self.uuid = str(uuid).replace("-", "")
        self.subjects = subjects
        self.objects = objects
        self.metadata = metadata
        self.rules = rules
        self.profiles = profiles
        self.description = description
        self.tenant = tenant
        self.db = None

    def get(self, data, uuid=None, name=None, attribute=None, category=None):
        attr_list = []
        if uuid:
            uuid = uuid.replace("_", "-")
        for obj in data:
            if uuid \
                    and attribute \
                    and obj["object"] == uuid \
                    and attribute in obj["attributes"] \
                    and obj["category"] == category:
                # Searching for an object assignment given its uuid
                return obj
            elif name and attribute:
                # Searching for an object assignment given its name
                #FIXME: get_subject or get_object depending on the data
                try:
                    uuid = self.get_subject(name=name)[0]["uuid"]
                except IndexError:
                    uuid = self.get_object(name=name)[0]["uuid"]
                if obj["object"] == uuid and attribute in obj["attributes"] and obj["category"] == category:
                    return obj
            elif category and obj["category"] != category:
                # if the object has not the correct category, continue
                continue
            if uuid is None and name is None:
                attr_list.append(obj)
            elif uuid and obj["uuid"] == uuid:
                return obj
            elif name and "name" in obj and obj["name"] == name:
                return obj
            elif name and "value" in obj and type(obj["value"]) in (str, unicode) and obj["value"] == name:
                return obj
            elif name and "value" in obj and type(obj["value"]) in (tuple, list) and name in obj["value"]:
                return obj
        return attr_list

    def has(self, data, uuid=None, name=None):
        return self.get(data, uuid=uuid, name=name)

    def get_subject(self, uuid=None, name=None):
        return self.get(self.subjects, uuid=uuid, name=name)

    def get_object(self, uuid=None, name=None):
        if not uuid and not name:
            return self.objects
        try:
            uuid = uuid.replace("_", "-")
        except AttributeError:
            name = name.replace("_", "-")
        for obj in self.objects:
            if uuid and obj["uuid"] == uuid:
                return [obj, ]
            elif name and obj["name"] == name:
                return [obj, ]
        return []

    def has_subject(self, uuid=None, name=None):
        return self.has(self.subjects, uuid=uuid, name=name)

    def add_subject(self, uuid=None, name=None, domain="default", enabled=True, mail="", project="", description=""):
        if not uuid:
            uuid = str(uuid4()).replace("-", "")
        sbj = {}
        sbj["uuid"] = uuid
        sbj["name"] = name
        sbj["enabled"] = enabled
        sbj["description"] = description
        sbj["domain"] = domain
        sbj["mail"] = mail
        sbj["project"] = project
        self.subjects.append(sbj)
        self.sync()

    def has_object(self, uuid=None, name=None):
        return self.get_object(uuid=uuid, name=name)

    def add_object(self, uuid=None, name=None, enabled=True, description=""):
        if not uuid:
            uuid = str(uuid4()).replace("-", "")
        obj = {}
        obj["uuid"] = uuid
        obj["name"] = name
        obj["enabled"] = enabled
        obj["description"] = description
        self.objects.append(obj)
        self.sync()

    def get_object_attributes(self, uuid=None, name=None, category=None):
        if not uuid and not name and not category:
            return self.profiles["o_attr"]
        ret_objects = []
        for obj in self.profiles["o_attr"]:
            if uuid == "a65f2b9ca6fe429a890054db108350fe": print(uuid, obj["uuid"])
            if uuid and obj["uuid"] == uuid:
                if uuid == "a65f2b9ca6fe429a890054db108350fe": print("Found")
                return [obj, ]
            elif name and type(obj["value"]) in (str, unicode) and obj["value"] == name:
                if category and obj["category"] == category:
                    return [obj, ]
                else:
                    return [obj, ]
            elif name and type(obj["value"]) in (list, tuple) and name in obj["value"]:
                if category and obj["category"] == category:
                    return [obj, ]
                else:
                    return [obj, ]
            elif not name and not uuid and category and obj["category"] == category:
                ret_objects.append(obj)
        return ret_objects

    def has_object_attributes(self, uuid=None, name=None, category=None):
        result = []
        for obj in self.profiles["o_attr"]:
            if category and obj["category"] != category:
                continue
            if uuid and obj["uuid"] == uuid:
                return [obj]
            elif name and obj["value"] == name:
                return [obj]
            else:
                result.append(obj)
        return result

    def add_object_attribute(self, category=None, value=None, description=""):
        o_attr = {}
        o_attr["uuid"] = str(uuid4()).replace("-", "")
        o_attr["category"] = category
        o_attr["value"] = value
        o_attr["description"] = description
        self.profiles["o_attr"].append(o_attr)
        self.sync()
        return o_attr["uuid"]

    def add_subject_attribute(self, category=None, value=None, description="", enabled=True):
        s_attr = {}
        s_attr["uuid"] = str(uuid4()).replace("-", "")
        s_attr["category"] = category
        s_attr["value"] = value
        s_attr["enabled"] = enabled
        s_attr["description"] = description
        self.profiles["s_attr"].append(s_attr)
        self.sync()
        return s_attr["uuid"]

    def get_subject_attributes(self, uuid=None, name=None, category=None):
        if not uuid and not name and not category:
            return self.profiles["s_attr"]
        ret_objects = []
        for obj in self.profiles["s_attr"]:
            if uuid and obj["uuid"] == uuid:
                return [obj, ]
            elif name and obj["value"] == name:
                return [obj, ]
            elif not uuid and not name and category and obj["category"] == category:
                ret_objects.append(obj)
        return ret_objects

    def has_subject_attributes(self, uuid=None, name=None, category=None):
        result = []
        for obj in self.profiles["s_attr"]:
            if category and obj["category"] != category:
                continue
            if obj["enabled"] not in (True, "true"):
                continue
            if uuid and obj["uuid"] == uuid:
                return [obj]
            elif name and obj["value"] == name:
                return [obj]
            else:
                result.append(obj)
        return result

    def has_subject_attributes_relation(
            self,
            uuid=None,
            name=None,
            category=None,
            attribute=""):
        data = self.profiles["s_attr_assign"]
        if not uuid:
            uuid = self.get_subject(name=name)[0]["uuid"]
        for obj in data:
            if uuid == obj["object"] and attribute in obj["attributes"]:
                return True
        return False

    def add_object_attributes_relation(
            self,
            uuid=None,
            object=None,
            attributes=[]):
        for assignment in self.profiles["o_attr_assign"]:
            if assignment["object"] == object:
                _attr = assignment["attributes"]
                _attr.extend(attributes)
                assignment["attributes"] = _attr
                self.sync()
                return
        if not uuid:
            uuid = str(uuid4()).replace("-", "")
        rel = {}
        rel["uuid"] = uuid
        rel["object"] = object
        if type(attributes) in (list, tuple):
            rel["attributes"] = attributes
        else:
            rel["attributes"] = [attributes, ]
        self.profiles["o_attr_assign"].append(rel)
        self.sync()

    def add_subject_attributes_relation(
            self,
            uuid=None,
            object=None,
            attributes=[]):
        for assignment in self.profiles["s_attr_assign"]:
            if assignment["object"] == object:
                _attr = assignment["attributes"]
                _attr.extend(attributes)
                assignment["attributes"] = _attr
                self.sync()
                return
        if not uuid:
            uuid = str(uuid4()).replace("-", "")
        rel = {}
        rel["uuid"] = uuid
        rel["object"] = object
        if type(attributes) in (list, tuple):
            rel["attributes"] = attributes
        else:
            rel["attributes"] = [attributes, ]
        self.profiles["s_attr_assign"].append(rel)
        self.sync()

    def has_object_attributes_relation(
            self,
            uuid=None,
            name=None,
            category=None,
            attribute=""):
        if name == "*":
            return True
        try:
            attribute_uuid = self.get_object_attributes(name=attribute)[0]["uuid"]
        except IndexError:
            try:
                attribute_uuid = self.get_object_attributes(uuid=attribute)[0]["uuid"]
            except IndexError:
                return False
        data = self.profiles["o_attr_assign"]
        if not uuid:
            try:
                uuid = self.get_object(name=name)[0]["uuid"]
            except IndexError:
                # There is no object with this name in our database.
                return False
        for obj in data:
            if uuid == obj["object"] and attribute_uuid in obj["attributes"]:
                return True
        return False

    def has_assignment(
            self,
            subject_name=None,
            subject_uuid=None,
            object_name=None,
            object_uuid=None,
            attribute_uuid=None,
            attribute_name=None,
            category=None):
        """
        :param subject_name: name of the user
        :param subject_uuid: uuid of the user
        :param object_name: name of the object
        :param object_uuid: uuid of the object
        :param attribute_uuid: uuid of the object attribute
        :param attribute_name: name of the object attribute
        :param category: name of the category attribute
        :return: None if no assignment, a dictionary if an assignment was found
        one of (`attribute_uuid`, `attribute_name`) is mandatory
        one of (`subject_name`, `subject_uuid`, `object_name`, `object_uuid`) is also mandatory
        """
        if object_uuid:
            object_uuid = object_uuid.replace("_", "-")
        if attribute_name and not attribute_uuid:
            if attribute_name == "*":
                return True
            if subject_uuid or subject_name:
                try:
                    attribute_uuid = self.get_subject_attributes(name=attribute_name)[0]["uuid"]
                except IndexError:
                    try:
                        attribute_uuid = self.get_subject_attributes(uuid=attribute_name)[0]["uuid"]
                    except IndexError:
                        # There is no subject with this name in our database.
                        return False
            elif object_uuid or object_name:
                try:
                    attribute_uuid = self.get_object_attributes(name=attribute_name)[0]["uuid"]
                except IndexError:
                    try:
                        attribute_uuid = self.get_object_attributes(uuid=attribute_name)[0]["uuid"]
                    except IndexError:
                        # There is no object with this name in our database.
                        return False
        if subject_uuid or subject_name:
            return self.has_subject_attributes_relation(
                uuid=subject_uuid,
                name=subject_name,
                category=category,
                attribute=attribute_uuid)
        if object_uuid or object_name:
            return self.has_object_attributes_relation(
                uuid=object_uuid,
                name=object_name,
                category=category,
                attribute=attribute_uuid)
        if not subject_uuid and not subject_name and not object_uuid and not object_name:
            # special case when Object is null because the action is for example list all tenants
            return True
        return False

    def get_rules(self):
        return self.rules

    def add_rule(self, rule):
        """Add a new rule in this extension
        :param rule: dict: the rule to add

        The new rule must be formed like this:
        {
            "name": "the name of the rule",
            "description": "a short description",
            "s_attr": [
                {u'category': u'role', u'value': u'admin'},
            ],
            "o_attr": [
                {u'category': u'type', u'value': u'server'},
                {u'category': u'action', u'value': u'get.os-start'},
            ],
        }
        """
        self.rules.append(rule)
        if self.db:
            self.sync()

    def sync(self, db=None):
        if db:
            self.db = db
        self.db.new_extension(
            uuid=self.uuid,
            name=self.name,
            subjects=self.subjects,
            objects=self.objects,
            metadata=self.metadata,
            rules=self.rules,
            profiles=self.profiles,
            description=self.description,
            tenant=self.tenant)

    def html(self):
        return mark_safe("""<b>Extension</b> {} for <b>tenant {}</b><br/><br/>
        <b>Subjects:</b> <ul>{}</ul><br>
        <b>Objects:</b> <ul>{}</ul>
        """.format(
            self.name,
            self.tenant["name"],
            "".join(map(lambda x: "<li>"+x["name"]+"</li>", self.subjects)),
            "".join(map(lambda x: "<li>"+x["name"]+"</li>", self.objects)),
        ))

    def __repr__(self):
        return """Extension {} ({}) for tenant {}
        Subjects: {}
        Objects: {}
        """.format(
            self.name,
            self.uuid,
            self.tenant["name"],
            map(lambda x: x["name"], self.subjects),
            map(lambda x: x["name"], self.objects),
        )