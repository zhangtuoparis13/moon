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
                uuid = self.get_subject(name=name)["uuid"]
                if obj["object"] == uuid and attribute in obj["attributes"] and obj["category"] == category:
                    return obj
            elif category and obj["category"] != category:
                # if the object has not the correct category, continue
                continue
            elif uuid and obj["uuid"] == uuid:
                return obj
            elif name and "name" in obj and obj["name"] == name:
                return obj
            elif name and "value" in obj and type(obj["value"]) in (str, unicode) and obj["value"] == name:
                return obj
            elif name and "value" in obj and type(obj["value"]) in (tuple, list) and name in obj["value"]:
                return obj
        return None

    def has(self, data, uuid=None, name=None):
        return self.get(data, uuid=uuid, name=name)

    def get_subject(self, uuid=None, name=None):
        return self.get(self.subjects, uuid=uuid, name=name)

    def get_object(self, uuid=None, name=None):
        return self.get(self.objects, uuid=uuid, name=name)

    def has_subject(self, uuid=None, name=None):
        return self.has(self.subjects, uuid=uuid, name=name)

    def has_object(self, uuid=None, name=None):
        return self.get_object(uuid=uuid, name=name)

    def get_object_attributes(self, uuid=None, name=None, category=None):
        return self.get(self.profiles["o_attr"], uuid=uuid, name=name, category=category)

    def has_object_attributes(self, uuid=None, name=None):
        return self.has(self.profiles["o_attr"], uuid=uuid, name=name)

    def get_subject_attributes(self, uuid=None, name=None, category=None):
        return self.get(self.profiles["s_attr"], uuid=uuid, name=name, category=category)

    def has_subject_attributes(self, uuid=None, name=None):
        return self.has(self.profiles["s_attr"], uuid=uuid, name=name)

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
        if attribute_name and not attribute_uuid:
            if attribute_name == "*":
                return True
            if subject_uuid or subject_name:
                attribute_uuid = self.get_subject_attributes(name=attribute_name)["uuid"]
            elif object_uuid or object_name:
                attribute_uuid = self.get_object_attributes(name=attribute_name)["uuid"]
        if subject_uuid or subject_name:
            return self.get(
                data=self.profiles["s_attr_assign"],
                uuid=subject_uuid,
                name=subject_name,
                category=category,
                attribute=attribute_uuid)
        if object_uuid or object_name:
            return self.get(
                data=self.profiles["o_attr_assign"],
                uuid=object_uuid,
                name=object_name,
                category=category,
                attribute=attribute_uuid)
        if not subject_uuid and not subject_name and not object_uuid and not object_name:
            # special case when Object is null because the action is for example list all tenants
            return True
        return None

    def get_rules(self):
        return self.rules

    def add_rule(self, rule):
        self.rules.append(rule)
        if self.db:
            self.sync()

    def sync(self, db=None):
        if db:
            self.db = db
        #TODO: self.name is modified from a string to a list; I don't know why
        if type(self.name) in (tuple, list):
            self.name = self.name[0]
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
        #TODO: self.name is modified from a string to a list; I don't know why
        if type(self.name) in (tuple, list):
            self.name = self.name[0]
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