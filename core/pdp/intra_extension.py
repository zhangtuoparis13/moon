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
from moon.core.pdp.authz import enforce

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
            protocol=None,
            administration=None):
        self.__name = name
        if not uuid:
            self.__uuid = str(uuid4()).replace("-", "")
        else:
            self.__uuid = str(uuid).replace("-", "")
        self.__subjects = subjects
        self.__objects = objects
        self.__metadata = metadata
        self.__rules = rules
        #TODO: separate profiles in o_attr, s_attr, ...
        self.__profiles = profiles
        self.__description = description
        self.__tenant = tenant
        self.__model = model
        self.__protocol = protocol
        self.__administration = administration
        self.__dispatcher = get_dispatcher()

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

    @enforce("tenant")
    def get_tenant(self):
        return dict(self.__tenant)

    def get_uuid(self):
        return self.__uuid

    def get_name(self):
        return self.__name

    @enforce("perimeter.subjects")
    def get_subject(self, uuid=None, name=None, **kwargs):
        return self.get(self.__subjects, uuid=uuid, name=name)

    @enforce("perimeter.objects")
    def get_object(self, uuid=None, name=None):
        if not uuid and not name:
            return self.__objects
        try:
            uuid = uuid.replace("_", "-")
        except AttributeError:
            name = name.replace("_", "-")
        for obj in self.__objects:
            if uuid and obj["uuid"] == uuid:
                return [obj, ]
            elif name and obj["name"] == name:
                return [obj, ]
        return []

    @enforce("perimeter.subjects")
    def has_subject(self, uuid=None, name=None):
        return self.has(self.__subjects, uuid=uuid, name=name)

    @enforce("perimeter.subjects", "w")
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
        self.__subjects.append(sbj)
        self.sync()

    @enforce("perimeter.objects")
    def has_object(self, uuid=None, name=None):
        return self.get_object(uuid=uuid, name=name)

    @enforce("perimeter.objects", "w")
    def add_object(self, uuid=None, name=None, enabled=True, description=""):
        if not uuid:
            uuid = str(uuid4()).replace("-", "")
        obj = {}
        obj["uuid"] = uuid
        obj["name"] = name
        obj["enabled"] = enabled
        obj["description"] = description
        obj["tenant"] = self.__tenant
        self.__objects.append(obj)
        self.sync()

    @enforce("profiles.o_attr")
    def get_object_attributes(self, uuid=None, name=None, category=None):
        if not uuid and not name and not category:
            return self.__profiles["o_attr"]
        ret_objects = []
        for obj in self.__profiles["o_attr"]:
            if uuid and obj[""] == uuid:
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

    @enforce("profiles.o_attr")
    def has_object_attributes(self, uuid=None, name=None, category=None):
        result = []
        for obj in self.__profiles["o_attr"]:
            if category and obj["category"] != category:
                continue
            if uuid and obj["uuid"] == uuid:
                return [obj]
            elif name and obj["value"] == name:
                return [obj]
            elif not name and not uuid:
                result.append(obj)
        return result

    @enforce("profiles.o_attr", "w")
    def add_object_attribute(self, category=None, value=None, description=""):
        o_attr = {}
        o_attr["uuid"] = str(uuid4()).replace("-", "")
        o_attr["category"] = category
        o_attr["value"] = value
        o_attr["description"] = description
        self.__profiles["o_attr"].append(o_attr)
        self.sync()
        return o_attr["uuid"]

    @enforce("profiles.s_attr", "w")
    def add_subject_attribute(self, uuid=None, category=None, value=None, description="", enabled=True):
        s_attr = {}
        if not uuid:
            s_attr["uuid"] = str(uuid4()).replace("-", "")
        else:
            s_attr["uuid"] = uuid
        s_attr["category"] = category
        s_attr["value"] = value
        s_attr["enabled"] = enabled
        s_attr["description"] = description
        self.__profiles["s_attr"].append(s_attr)
        self.sync()
        return s_attr["uuid"]

    @enforce("profiles.s_attr")
    def get_subject_attributes(self, uuid=None, name=None, category=None):
        if not uuid and not name and not category:
            return self.__profiles["s_attr"]
        ret_objects = []
        for obj in self.__profiles["s_attr"]:
            if uuid and obj["uuid"] == uuid:
                return [obj, ]
            elif name and obj["value"] == name:
                return [obj, ]
            elif not uuid and not name and category and obj["category"] == category:
                ret_objects.append(obj)
        return ret_objects

    @enforce("profiles.s_attr")
    def has_subject_attributes(self, uuid=None, name=None, category=None):
        result = []
        for obj in self.__profiles["s_attr"]:
            if category and obj["category"] != category:
                continue
            if "enabled" in obj and obj["enabled"] not in (True, "true"):
                continue
            if uuid and obj["uuid"] == uuid:
                return [obj]
            elif name and obj["value"] == name:
                return [obj]
            elif not name and not uuid:
                result.append(obj)
        return result

    @enforce("profiles.s_attr_assign")
    def has_subject_attributes_relation(
            self,
            uuid=None,
            name=None,
            category=None,
            attribute=[]):
        data = self.__profiles["s_attr_assign"]
        if not uuid:
            uuid = self.get_subject(name=name)[0]["uuid"]
        for sbj in data:
            if type(attribute) not in (list, tuple):
                attribute = [attribute, ]
            for att in attribute:
                if uuid == sbj["subject"] and att in sbj["attributes"]:
                    return True
        return False

    @enforce("profiles.o_attr_assign", "w")
    def add_object_attributes_relation(
            self,
            uuid=None,
            object=None,
            attributes=[]):
        for assignment in self.__profiles["o_attr_assign"]:
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
        self.__profiles["o_attr_assign"].append(rel)
        self.sync()

    @enforce("profiles.s_attr_assign", "w")
    def add_subject_attributes_relation(
            self,
            uuid=None,
            subject=None,
            attributes=[]):
        for assignment in self.__profiles["s_attr_assign"]:
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
        self.__profiles["s_attr_assign"].append(rel)
        self.sync()

    @enforce("profiles.s_attr_assign")
    def get_subject_attributes_relation(self):
        return self.__profiles["s_attr_assign"]

    @enforce("profiles.o_attr_assign")
    def get_object_attributes_relation(self):
        return self.__profiles["o_attr_assign"]

    @enforce("profiles.o_attr_assign")
    def has_object_attributes_relation(
            self,
            uuid=None,
            name=None,
            category=None,
            attribute=[]):
        if name == "*":
            return True
        data = self.__profiles["o_attr_assign"]
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

    @enforce("configuration.rules")
    def get_rules(self):
        return self.__rules

    @enforce("configuration.rules", "w")
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
        self.__rules.append(rule)
        self.sync()

    def requesting_vent_create(self, vent, objects_list):
        return None

    def requested_vent_create(self, vent, subjects_list):
        return None

    @enforce("perimeter.subjects", "w")
    def delete_subject(self, uuid):
        for index, sbj in enumerate(self.__subjects):
            if sbj["uuid"] == uuid:
                self.__subjects.pop(index)

    @enforce("perimeter.objects", "w")
    def delete_object(self, uuid):
        for index, sbj in enumerate(self.__objects):
            if sbj["uuid"] == uuid:
                self.__objects.pop(index)

    @enforce("profiles.o_attr")
    def delete_object_attributes(self, uuid=None, name=None):
        for index, o_attr in enumerate(self.__profiles["o_attr"]):
            if o_attr["uuid"] == uuid or o_attr["value"] == name:
                return self.__profiles["o_attr"].pop(index)

    @enforce("profiles.s_attr")
    def delete_subject_attributes(self, uuid=None, name=None):
        for index, s_attr in enumerate(self.__profiles["s_attr"]):
            if s_attr["uuid"] == uuid or s_attr["value"] == name:
                return self.__profiles["s_attr"].pop(index)

    def delete_attributes_from_vent(self, vent_uuid):
        if self.has_subject(uuid=vent_uuid):
            self.delete_subject(uuid=vent_uuid)
        if self.has_object(uuid=vent_uuid):
            self.delete_object(uuid=vent_uuid)

    @enforce("configuration.rules", "w")
    def delete_rules(self, s_attrs=[], o_attrs=[]):
        if type(s_attrs) not in (list, tuple):
            s_attrs = [s_attrs, ]
        if type(o_attrs) not in (list, tuple):
            o_attrs = [o_attrs, ]
        indexes = []
        for index, rule in enumerate(self.get_rules()):
            for s_attr in s_attrs:
                if s_attr in map(lambda x: x["value"], rule["s_attr"]):
                    indexes.append(index)
                    break
            for o_attr in o_attrs:
                if o_attr in map(lambda x: x["value"], rule["o_attr"]):
                    indexes.append(index)
                    break
        indexes.reverse()
        for index in indexes:
            try:
                self.get_rules().pop(index)
            except IndexError:
                pass

    @enforce("profiles.s_attr", "w")
    def delete_subject_relation(self, attributes=[]):
        for relation in self.__profiles["s_attr_assign"]:
            for att in attributes:
                try:
                    relation["attributes"].remove(att)
                except ValueError:
                    pass

    @enforce("profiles.o_attr", "w")
    def delete_object_relation(self, attributes=[]):
        for relation in self.__profiles["o_attr_assign"]:
            for att in attributes:
                try:
                    relation["attributes"].remove(att)
                except ValueError:
                    pass

    def delete_attributes_relations(self, s_attrs=[], o_attrs=[]):
        self.delete_subject_relation(attributes=s_attrs)
        self.delete_object_relation(attributes=o_attrs)

    def __has_admin_assignment(
            self,
            object_uuid=None,
            attribute_uuid=None
        ):
        if object_uuid == "*":
            return True
        data = self.__administration["assignments"]
        for obj in data:
            if type(attribute_uuid) not in (list, tuple):
                attribute_uuid = [attribute_uuid, ]
            for att in attribute_uuid:
                if object_uuid == obj["object"] and att in obj["attributes"]:
                    return True
        return False

    def authz(self, auth):
        if "objects" not in self.__administration:
            auth["message"] = "No administration protocol for extension"
            auth["auth"] = True
            return auth
        if self.__tenant["name"] != auth["tenant_name"]:
            auth["message"] = "Tenant not found."
            return auth
        if auth["subject"] not in map(lambda x: x["uuid"], self.__subjects):
            auth["message"] = "User not found."
            return auth
        if auth["object_name"] not in map(lambda x: x["name"], self.__administration["objects"]):
            auth["message"] = "Object not found."
            return auth
        for obj in self.__administration["objects"]:
            if obj["name"] == auth["object_name"]:
                auth["object_uuid"] = obj["uuid"]
                break
        for rule in self.__administration["rules"]:
            _auth = False
            for s_rule in rule["s_attr"]:
                data = self.__profiles["s_attr_assign"]
                attribute = s_rule["value"]
                for sbj in data:
                    if type(attribute) not in (list, tuple):
                        attribute = [attribute, ]
                    for att in attribute:
                        if auth["subject"] == sbj["subject"] and att in sbj["attributes"]:
                            _auth = True
                            break
            if not _auth:
                auth["message"] = "Rules on subject don't match."
                continue
            for o_rule in rule["o_attr"]:
                    if o_rule["category"] == "action":
                        _auth = self.__has_admin_assignment(
                            object_uuid=auth["object_uuid"],
                            attribute_uuid=auth["action"])
                        if not _auth:
                            auth["message"] = "Rules on action assignments don't match."
                            break
                        if auth["action"] not in o_rule["value"]:
                            auth["message"] = "Rules on action don't match."
                            break
                    else:
                        _auth = self.__has_admin_assignment(
                            object_uuid=auth["object_uuid"],
                            attribute_uuid=o_rule["value"])
                        if not _auth:
                            auth["message"] = "Rules on object don't match."
                            print(auth["object_uuid"], o_rule["value"])
                            break
            else:
                auth["message"] = ""
                auth["auth"] = True
                break
        return auth

    def sync(self):
        self.__dispatcher.new_extension(
            uuid=self.__uuid,
            name=self.__name,
            subjects=self.__subjects,
            objects=self.__objects,
            metadata=self.__metadata,
            rules=self.__rules,
            profiles=self.__profiles,
            description=self.__description,
            tenant=self.__tenant,
            model=self.__model,
            type="extension",
            protocol=self.__protocol,
            administration=self.__administration
        )

    @enforce(("tenant", "perimeter.subjects", "perimeter.objects"))
    def html(self):
        return mark_safe("""<b>Extension</b> {} for <b>tenant {}</b><br/><br/>
        <b>Subjects:</b> <ul>{}</ul><br>
        <b>Objects:</b> <ul>{}</ul>
        """.format(
            self.__name,
            self.__tenant["name"],
            "".join(map(lambda x: "<li>"+x["name"]+"</li>", self.__subjects)),
            "".join(map(lambda x: "<li>"+x["name"]+"</li>", self.__objects)),
        ))

    def __repr__(self):
        return """Extension {} ({}) for tenant {}
        Subjects: {}
        Objects: {}
        """.format(
            self.__name,
            self.__uuid,
            self.__tenant["name"],
            map(lambda x: x["name"], self.__subjects),
            map(lambda x: x["name"], self.__objects),
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
                protocol=ext["configuration"]["protocol"],
                administration=ext["administration"]
            )

    def values(self):
        return self.extensions.values()

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
        if not uuid and not name:
            return self.extensions
        for ext in self.extensions.values():
            for obj in ext.get_object():
                if uuid and obj["uuid"] == uuid:
                    return [obj]
                elif name and obj["name"] == name:
                    return [obj]
        return []

    def new_from_json(self, json_data):
        # all_tenants = map(lambda x: x.tenant["uuid"], self.extensions.values())
        # if json_data["tenant"]["uuid"] not in all_tenants:
        extension_filename = json_data["configuration"]["protocol"].split(":")[0]
        extension_class = json_data["configuration"]["protocol"].split(":")[-1]
        if not os.path.isfile(extension_filename) or not os.path.isfile(extension_filename):
            raise Exception("Cannot find an adequate protocol for extension {}".format(extension_filename))
        requesting_module = imp.load_source("requesting_vent_create", extension_filename)
        __IntraExtension = eval("requesting_module.{}".format(extension_class))
        administration = dict()
        administration["filename"] = json_data["configuration"]["administration"]
        adm_obj = None
        try:
            adm_obj = json.loads(open(administration["filename"]).read())
        except IOError:
            pass
        if adm_obj:
            administration["objects"] = adm_obj["perimeter"]["objects"]
            administration["attributes"] = adm_obj["profiles"]["o_attr"]
            administration["assignments"] = adm_obj["profiles"]["o_attr_assign"]
            administration["rules"] = adm_obj["configuration"]["rules"]
            admin_role = filter(lambda x: x["value"] == "admin", json_data["profiles"]["s_attr"])[0]
            default_admin_rule = {
                "name": "default_rule_for_admin_user",
                "s_attr": [
                    {"category": "role", "value": admin_role["uuid"]}
                ],
                "o_attr": [
                    {
                        "category": "id", "value": [
                            "id_subjects_list",
                            "id_objects_list",
                            "id_rules_list",
                            "id_s_attr_list",
                            "id_o_attr_list",
                            "id_s_attr_assign_list",
                            "id_o_attr_assign_list",
                            "id_tenant"
                        ]
                    },
                    {"category": "action", "value": ["action-read", "action-write"]}
                ],
                "description": "The admin has all authorisations by default"
            }
            administration["rules"].append(default_admin_rule)
        ext = __IntraExtension(
            name=json_data["name"],
            uuid=json_data["uuid"],
            subjects=[],
            objects=[],
            metadata=json_data["configuration"]["metadata"],
            rules=json_data["configuration"]["rules"],
            profiles=json_data["profiles"],
            description=json_data["description"],
            tenant=json_data["tenant"],
            model=json_data["model"],
            protocol=json_data["configuration"]["protocol"],
            administration=administration
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

    def delete_attributes_from_vent(self, uuid):
        for ext in self.get():
            ext.delete_attributes_from_vent(uuid)

    def delete_rules(self, s_attrs=None, o_attrs=None):
        for ext in self.get():
            ext.delete_rules(s_attrs=s_attrs, o_attrs=o_attrs)

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