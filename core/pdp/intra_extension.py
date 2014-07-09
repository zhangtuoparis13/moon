from uuid import uuid4
import json
import logging
import os
import imp
try:
    from django.utils.safestring import mark_safe
except ImportError:
    mark_safe = str
from moon.intra_extension_manager import get_dispatcher
from moon import settings

logger = logging.getLogger(__name__)


class IntraExtension(object):

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
            tenant=None,
            model="RBAC",
            protocol=None):
        self.name = name
        if not uuid:
            self.uuid = str(uuid4()).replace("-", "")
        else:
            self.uuid = str(uuid).replace("-", "")
        self.subjects = subjects
        self.objects = objects
        self.metadata = metadata
        self.rules = rules
        #TODO: separate profiles in o_attr, s_attr, ...
        self.profiles = profiles
        self.description = description
        self.tenant = tenant
        self.dispatcher = get_dispatcher()
        self.model = model
        self.protocol = protocol
        # if not self.protocol or "requesting" not in self.protocol or "requested" not in self.protocol:
        #     raise Exception("Cannot find an adequate protocol for extension {}".format(self.uuid))
        # requesting_filename = self.protocol["requesting"].split(":")[0]
        # requesting_function = self.protocol["requesting"].split(":")[-1]
        # requested_filename = self.protocol["requested"].split(":")[0]
        # requested_function = self.protocol["requested"].split(":")[-1]
        # if not os.path.isfile(requesting_filename) or not os.path.isfile(requested_filename):
        #     raise Exception("Cannot find an adequate protocol for extension {}".format(self.uuid))
        # requesting_module = imp.load_source("requesting_vent_create", requesting_filename)
        # self.__requesting_vent_create = eval("requesting_module.{}".format(requesting_function))
        # requested_module = imp.load_source("requested_vent_create", requested_filename)
        # self.__requested_vent_create = eval("requested_module.{}".format(requested_function))

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

    #TODO @check_admin_auth
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
        obj["tenant"] = self.tenant
        self.objects.append(obj)
        self.sync()

    def get_object_attributes(self, uuid=None, name=None, category=None):
        if not uuid and not name and not category:
            return self.profiles["o_attr"]
        ret_objects = []
        for obj in self.profiles["o_attr"]:
            if uuid and obj["uuid"] == uuid:
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
            elif not name and not uuid:
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
            elif not name and not uuid:
                result.append(obj)
        return result

    def has_subject_attributes_relation(
            self,
            uuid=None,
            name=None,
            category=None,
            attribute=[]):
        data = self.profiles["s_attr_assign"]
        if not uuid:
            uuid = self.get_subject(name=name)[0]["uuid"]
        for sbj in data:
            if type(attribute) not in (list, tuple):
                attribute = [attribute, ]
            for att in attribute:
                if uuid == sbj["subject"] and att in sbj["attributes"]:
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
            subject=None,
            attributes=[]):
        for assignment in self.profiles["s_attr_assign"]:
            if assignment["subject"] == subject:
                _attr = assignment["attributes"]
                _attr.extend(attributes)
                assignment["attributes"] = _attr
                self.sync()
                return
        if not uuid:
            uuid = str(uuid4()).replace("-", "")
        rel = {}
        rel["uuid"] = uuid
        rel["subject"] = subject
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
            attribute=[]):
        if name == "*":
            return True
        data = self.profiles["o_attr_assign"]
        if not uuid:
            uuid = self.get_subject(name=name)[0]["uuid"]
        for obj in data:
            if type(attribute) not in (list, tuple):
                attribute = [attribute, ]
            for att in attribute:
                if uuid == obj["object"] and att in obj["attributes"]:
                    return True
        return False

    def has_assignment(
            self,
            subject_name=None,
            subject_uuid=None,
            object_name=None,
            object_uuid=None,
            attribute_uuid=[],
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
        if attribute_uuid == "*":
                return True
        if attribute_name and not attribute_uuid:
            if attribute_name == "*":
                return True
            if subject_uuid or subject_name:
                # try:
                if type(attribute_name) not in (list, tuple):
                    attribute_name = [attribute_name, ]
                for att in attribute_name:
                    _uuid = self.get_subject_attributes(name=att)[0]["uuid"]
                    if _uuid:
                        attribute_uuid.append(_uuid)
                    # attribute_uuid = self.get_subject_attributes(name=attribute_name)[0]["uuid"]
                # except IndexError:
                #     try:
                #         attribute_uuid = self.get_subject_attributes(uuid=attribute_name)[0]["uuid"]
                #     except IndexError:
                #         # There is no subject with this name in our database.
                #         return False
            elif object_uuid or object_name:
                if type(attribute_name) not in (list, tuple):
                    attribute_name = [attribute_name, ]
                for att in attribute_name:
                    _uuid = self.get_object_attributes(name=att)[0]["uuid"]
                    if _uuid:
                        attribute_uuid.append(_uuid)
                # try:
                #     attribute_uuid = self.get_object_attributes(name=attribute_name)[0]["uuid"]
                # except IndexError:
                #     try:
                #         attribute_uuid = self.get_object_attributes(uuid=attribute_name)[0]["uuid"]
                #     except IndexError:
                #         # There is no object with this name in our database.
                #         return False
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
        self.sync()

    def requesting_vent_create(self, vent, objects_list):
        #TODO: identifier tous les objets
        #TODO: creer des attr et attr_assign et des rules pour que le vent accede aux objects
        return None

    def requested_vent_create(self, vent, subjects_list):
        #TODO: identifier tous les subjets
        #TODO: creer des attr et attr_assign et des rules pour que les subjects accedent au vent
        return None

    def sync(self):

        self.dispatcher.new_extension(
            uuid=self.uuid,
            name=self.name,
            subjects=self.subjects,
            objects=self.objects,
            metadata=self.metadata,
            rules=self.rules,
            profiles=self.profiles,
            description=self.description,
            tenant=self.tenant,
            model=self.model,
            protocol=self.protocol
        )

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


class IntraExtensions:

    def __init__(self):
        #TODO create a MongoDB collection per extension
        self.dispatcher = get_dispatcher()
        self.extensions = {}
        for ext in self.dispatcher.list(type="extension"):
            extension_filename = ext["configuration"]["protocol"].split(":")[0]
            extension_class = ext["configuration"]["protocol"].split(":")[-1]
            if not os.path.isfile(extension_filename) or not os.path.isfile(extension_filename):
                raise Exception("Cannot find an adequate protocol for extension {}".format(ext["uuid"]))
            requesting_module = imp.load_source("requesting_vent_create", extension_filename)
            __IntraExtension = eval("requesting_module.{}".format(extension_class))
            self.extensions[ext["uuid"]] = __IntraExtension(
                name=ext["name"],
                uuid=ext["uuid"],
                subjects=ext["perimeter"]["subjects"],
                objects=ext["perimeter"]["objects"],
                metadata=ext["configuration"]["metadata"],
                rules=ext["configuration"]["rules"],
                profiles=ext["profiles"],
                description=ext["description"],
                tenant=ext["tenant"],
                model=ext["model"],
                protocol=ext["configuration"]["protocol"]
            )

    def list(self, ):
        return self.extensions.values()

    def keys(self):
        return self.extensions.keys()

    def get(self, uuid=None, name=None, attributes=dict()):
        """
        :param uuid: uuid of the extension
        :param name: name of the extension
        :param attributes: other attributes to look for
        :return: a list of extensions
        """
        if not uuid and not name and not attributes:
            return self.extensions.values()
        elif uuid:
            return [self.extensions[uuid], ]
        elif name:
            for ext in self.extensions.values():
                if ext.name == name:
                    return [ext, ]
        else:
            uuids = map(lambda x: x["uuid"], tuple(self.dispatcher.get(attributes=attributes)))
            exts = []
            for uuid in uuids:
                exts.append(self.extensions[uuid])
            return exts

    def get_object(self, uuid=None, name=None):
        objects = []
        for ext in self.extensions.values():
            for obj in ext.objects:
                if uuid and obj["uuid"] == uuid:
                    return [obj]
                elif name and obj["name"] == name:
                    return [obj]
                elif not uuid and not name:
                    objects.append(obj)
        return objects

    def new_from_json(self, json_data):
        # all_tenants = map(lambda x: x.tenant["uuid"], self.extensions.values())
        # if json_data["tenant"]["uuid"] not in all_tenants:
        extension_filename = json_data["configuration"]["protocol"].split(":")[0]
        extension_class = json_data["configuration"]["protocol"].split(":")[-1]
        if not os.path.isfile(extension_filename) or not os.path.isfile(extension_filename):
            raise Exception("Cannot find an adequate protocol for extension {}".format(self.uuid))
        requesting_module = imp.load_source("requesting_vent_create", extension_filename)
        __IntraExtension = eval("requesting_module.{}".format(extension_class))
        ext = __IntraExtension(
            name=json_data["name"],
            uuid=json_data["uuid"],
            subjects=[],#json_data["perimeter"]["subjects"],
            objects=[],#json_data["perimeter"]["objects"],
            metadata=json_data["configuration"]["metadata"],
            rules=json_data["configuration"]["rules"],
            profiles=json_data["profiles"],
            description=json_data["description"],
            tenant=json_data["tenant"],
            model=json_data["model"],
            protocol=json_data["configuration"]["protocol"],
        )
        ext.sync()
        self.extensions[json_data["uuid"]] = ext
        #Adding subjects and objects after so we can tune afterward the creation process
        for sbj in json_data["perimeter"]["subjects"]:
            if "description" not in sbj:
                sbj["description"] = ""
            if "mail" not in sbj:
                sbj["mail"] = ""
            if "project" not in sbj:
                sbj["project"] = ""
            ext.add_subject(
                uuid=sbj["uuid"], 
                name=sbj["name"], 
                domain=sbj["domain"], 
                enabled=sbj["enabled"], 
                mail=sbj["mail"], 
                project=sbj["project"], 
                description=sbj["description"])
        for obj in json_data["perimeter"]["objects"]:
            if "description" not in obj:
                obj["description"] = ""
            ext.add_object(
                uuid=obj["uuid"], 
                name=obj["name"], 
                enabled=obj["enabled"],
                description=obj["description"])
        return ext
        # else:
        #     return None

    def new(
            self,
            uuid=None,
            name="",
            subjects=None,
            objects=None,
            metadata=None,
            rules=None,
            profiles=None,
            description=""):
        """Create a new Intra-extension
        :param uuid: uuid of this extension (optional)
        :param name: name of this extension
        :param subjects: list of subjects example:
            [{
                "uuid": "user1_uuid",
                "name": "admin",
                "mail": "admin@localhost",
                "tenant_id": "0123456789",
                "description": "an administrator",
                "enabled": True
            },]
        :param objects: list of objects example:
            [{
                "uuid": "object1_uuid",
                "name": "vm1",
                "description": "the virtual machine number 1",
                "enabled": True
            },]
        :param metadata: list of authorized attributes for subject and object, example:
            {
                "subject": [
                    "role",
                    "group"
                ],
                "object": [
                    "type",
                    "security"
                ]
            }
        :param rules: list of rules, example:
            [{
                "name": "rule1",
                "s_attr": { "category": "role", "value": "subject_attribute_uuid1" },
                "o_attr": { "category": "type", "value": "object_attribute_uuid1" },
                "a_attr": { "category": "action", "value": "list" },
                "description": "..."
            },]
        :param profiles: list of profiles, example:
            {
                "s_attr": {
                    "s_attr_uuid1": {
                        "category": "role",
                        "value": "admin",
                        "description": "le role admin"
                    },
                    "s_uuid2": {
                        "category": "role",
                        "value": "dev"
                    },
                    "s_uuid3": {
                        "category": "group",
                        "value": "prog"
                    }
                },
                "o_attr": {
                    "o_attr_uuid1": {
                        "category": "type",
                        "value": "stockage",
                        "description": ""
                    },
                    "o_uuid2": {
                        "category": "size",
                        "value": "medium"
                    }
                },
                "s_attr_assign": {
                    "assign1_uuid": {
                        "subject": "user1_uuid",
                        "attributes": [ "s_uuid1", "s_uuid3" ]
                    },
                    "assign2_uuid": {
                        "subject": "user3_uuid",
                        "attributes": [ "s_uuid1", "s_uuid2", "s_uuid3" ]
                    }
                },
                "o_attr_assign": {
                    "assign3_uuid": {
                        "object": "object1_uuid",
                        "attributes": [ "o_uuid1", "o_uuid3" ]
                    },
                    "assign4_uuid": {
                        "object": "object3_uuid",
                        "attributes": [ "o_uuid1", "o_uuid2", "o_uuid3" ]
                    }
                }
            }
        :param description: string describing the new extension.
        :return the created UUID
        """
        filename = getattr(settings, "DEFAULT_EXTENSION_TABLE")
        json_data = json.loads(file(filename).read())
        all_tenants = map(lambda x: x.tenant["uuid"], self.extensions.values())
        if uuid:
            json_data["uuid"] = uuid
        else:
            json_data["uuid"] = str(uuid4()).replace("-", "")
        if name:
            json_data["name"] = name
        if subjects:
            json_data["perimeter"]["subjects"] = subjects
        if objects:
            json_data["perimeter"]["objects"] = objects
        if metadata:
            json_data["configuration"]["metadata"] = metadata
        if rules:
            json_data["configuration"]["rules"] = rules
        if profiles:
            json_data["profiles"] = profiles
        if description:
            json_data["description"] = description
        json_data["tenant"] = {}
        json_data["tenant"]["uuid"] = str(uuid4()).replace("-", "")
        if json_data["tenant"]["uuid"] not in all_tenants:
            ext = IntraExtension(
                name=json_data["name"],
                uuid=json_data["uuid"],
                subjects=json_data["perimeter"]["subjects"],
                objects=json_data["perimeter"]["objects"],
                metadata=json_data["configuration"]["metadata"],
                rules=json_data["configuration"]["rules"],
                profiles=json_data["profiles"],
                description=json_data["description"],
                tenant=json_data["tenant"]
            )
            ext.sync()
            self.extensions[json_data["uuid"]] = ext
            return ext
        else:
            return None

    # def add_user(self, user):
    #     return self.db.add_user(user)
    #
    # def add_role(self, role):
    #     return self.db.add_role(role)

    def delete(self, uuid):
        self.extensions.pop(uuid)
        return self.dispatcher.delete(uuid=uuid)

    def delete_tables(self):
        logger.warning("Dropping Intra Extension Database")
        self.extensions = dict()
        return self.dispatcher.drop()


intra_extentions = IntraExtensions()


def get_intra_extentions():
    return intra_extentions