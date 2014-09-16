from moon.core.pdp.intra_extension import IntraExtension
from uuid import uuid4
from moon.tools.exceptions import *


class RBACIntraExtension(IntraExtension):

    def add_object(self, name, uuid="", enabled=True, description="", project=None):
        if uuid:
            uuid = uuid.replace("-", "")
        IntraExtension.add_object(self, uuid=uuid, name=name, enabled=enabled, description=description, project=project)
        # Default: all objects (ie all VM) have the attribute id linked to the uuid of the object
        attr = self.add_object_attributes(
            category="id",
            value=uuid,
            description="attribute id for {}".format(name))
        self.add_object_attribute_assignments(object_name=uuid, category="id", attributes=[attr["uuid"]])
        # Default: all objects (ie all VM) have all attribute action
        actions = map(lambda x: x["uuid"], self.get_object_attributes(category="action"))
        # for action in actions:
        self.add_object_attribute_assignments(object_name=uuid, category="action", attributes=actions)

    def add_subject(self, uuid=None, name=None, domain="default", enabled=True, mail="", project="", description=""):
        IntraExtension.add_subject(
            self,
            uuid=uuid,
            name=name,
            domain=domain,
            enabled=enabled,
            mail=mail,
            project=project,
            description=description
        )
        # No need to add roles, they have been already added

    def delete_attributes_from_vent(self, vent_uuid):
        attributes = []
        #Delete attributes
        try:
            attr = self.get_object_attributes(
                value="virtual_entity_role_{}".format(vent_uuid),
                category="role").next()
            self.del_object_attributes(uuid=attr["uuid"])
            attributes.append(attr["uuid"])
        except StopIteration:
            pass
        try:
            attr = self.get_subject_attributes(
                value="virtual_entity_role_{}".format(vent_uuid),
                category="role").next()
            self.del_subject_attributes(uuid=attr["uuid"])
            attributes.append(attr["uuid"])
        except StopIteration:
            pass
        try:
            attr = self.get_subject_attributes(
                value="virtual_entity_role_{}".format(vent_uuid),
                category="id").next()
            self.del_subject_attributes(uuid=attr["uuid"])
            attributes.append(attr["uuid"])
        except StopIteration:
            pass
        try:
            attr = self.get_object_attributes(
                value="virtual_entity_role_{}".format(vent_uuid),
                category="id").next()
            self.del_object_attributes(uuid=attr["uuid"])
            attributes.append(attr["uuid"])
        except StopIteration:
            pass
        #Delete attribute assignments
        for attr in attributes:
            try:
                self.del_subject_attribute_assignments(attr)
            except SubjectAssignmentNotFoundException:
                pass
            try:
                self.del_object_attribute_assignments(attr)
            except ObjectAssignmentNotFoundException:
                pass
        #Delete VENT
        try:
            self.del_subject(uuid=vent_uuid)
        except SubjectNotFoundException:
            pass
        try:
            self.del_object(uuid=vent_uuid)
        except ObjectNotFoundException:
            pass

    def delete_rules(self, s_attrs=[], o_attrs=[]):
        if type(s_attrs) not in (list, tuple):
            s_attrs = [s_attrs, ]
        if type(o_attrs) not in (list, tuple):
            o_attrs = [o_attrs, ]
        indexes = []
        for rule in self.get_rules():
            for s_attr in s_attrs:
                vent_role_uuid = self.get_subject_attributes(
                    value="virtual_entity_role_{}".format(s_attr),
                    category="role").next()["uuid"]
                if vent_role_uuid in map(lambda x: x["value"], rule["s_attr"]):
                    indexes.append(vent_role_uuid)
                    break
        for index in indexes:
            try:
                self.del_rule(uuid=index)
            except RuleNotFoundException:
                pass

    def requesting_vent_create(self, vent, subjects_list):
        try:
            self.add_object(uuid=vent.uuid, name=vent.name, description="virtual entity")
        except DuplicateObjectException:
            pass
        # Get or Create the virtual entity role
        try:
            vent_role = self.get_subject_attributes(
                value="virtual_entity_role_{}".format(vent.uuid),
                category="role").next()
        except StopIteration:
            #Create it
            vent_role = self.add_subject_attributes(
                value="virtual_entity_role_{}".format(vent.uuid),
                category="role",
                description="The role for managing virtual entities")
        #Create relation between subjects and virtual_entity_role
        for subject_uuid in subjects_list:
            try:
                assignments = self.get_subject_attribute_assignments(subject_name=subject_uuid, category="role").next()
            except StopIteration:
                self.add_subject_attribute_assignments(
                    subject_name=subject_uuid,
                    category="role",
                    attributes=[subject_uuid,])
            else:
                attributes = assignments["attributes"]
                attributes.append(subject_uuid)
                self.set_subject_attribute_assignments(
                    uuid=assignments["uuid"],
                    attributes=attributes)
        # Create an attribute "id" for the Vent
        try:
            _uuid = self.add_object_attributes(
                category="id",
                value=vent.uuid,
                description="object attribute for the vent")
            self.add_object_attribute_assignments(object_name=vent.uuid, category="id", attributes=[_uuid, ])
        except DuplicateObjectAttributeException:
            pass
        # Assign all actions to the virtual entity
        actions = self.get_object_attributes(category="action")
        for action in actions:
            self.add_object_attribute_assignments(object_name=vent.uuid, category="action", attributes=[action["uuid"]])
        self.add_rule(
            name="requesting_rule_vent_{}".format(str(uuid4())),
            description="Rule for role {} in order to use the virtual entity {}".format(
                vent_role["uuid"],
                vent.uuid
            ),
            subject_attrs=[
                {u'category': u'role', u'value': vent_role["value"]},
            ],
            object_attrs=[
                {u'category': u'id', u'value': vent.name},
                {u'category': u'action', u'value': [x["uuid"] for x in actions]},
            ]
        )

    def requested_vent_create(self, vent, objects_list):
        try:
            self.add_subject(uuid=vent.uuid, name=vent.name, description="virtual entity")
        except DuplicateSubjectException:
            pass
        # Get or Create the virtual entity role
        try:
            vent_role = self.get_subject_attributes(
                value="virtual_entity_role_{}".format(vent.uuid),
                category="role").next()
        except StopIteration:
            #Create it
            self.add_subject_attributes(
                value="virtual_entity_role_{}".format(vent.uuid),
                category="role",
                description="The role for managing virtual entities")
            vent_role = self.get_subject_attributes(
                value="virtual_entity_role_{}".format(vent.uuid),
                category="role").next()
        #Create relation between virtual entity and virtual_entity_role
        self.add_subject_attribute_assignments(
            subject_name=vent.uuid,
            category="role",
            attributes=[vent_role["uuid"]]
        )
        # Add rules
        actions = self.get_object_attributes(category="action")
        for obj in objects_list:
            _id_obj = self.get_object_attributes(category="id", value=obj).next()["value"]
            _actions = []
            for action in actions:
                if action["uuid"] in self.get_object_attribute_assignments(
                    object_name=obj,
                    category="action"
                ).next()["attributes"]:
                    _actions.append(action)
            self.add_rule(
                name="requested_rule_vent_{}".format(str(uuid4())),
                description="Rule for role {} in order to use the virtual entity {}".format(
                    vent_role["uuid"],
                    vent.uuid
                ),
                subject_attrs=[
                    {u'category': u'role', u'value': vent_role["uuid"]},
                ],
                object_attrs=[
                    {u'category': u'id', u'value': _id_obj},
                    {u'category': u'action', u'value': [x["value"] for x in _actions]},
                ]
            )
