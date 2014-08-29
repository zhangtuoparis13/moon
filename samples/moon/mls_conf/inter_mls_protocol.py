from moon.core.pdp.intra_extension import IntraExtension
from moon.tools.exceptions import SubjectNotFoundException, ObjectNotFoundException
from moon.tools.exceptions import DuplicateObjectException, DuplicateSubjectException
from uuid import uuid4


class MLSIntraExtension(IntraExtension):

    def add_object(self, name, uuid="", description="", enabled=True, project=None):
        #HYPOTHESIS: objects are only virtual servers, so linking all objects to type server
        IntraExtension.add_object(self, uuid=uuid, name=name, enabled=enabled, description=description, project=project)
        # Default: all objects (ie all VM) have the attribute security_level to medium
        self.add_object_attribute_assignments(object_name=uuid, category="security_level", attributes=["security_medium"])
        # Default: all objects (ie all VM) have all attribute action
        actions = map(lambda x: x["uuid"], self.get_object_attributes(category="action"))
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
        # Default: all subjects (ie all users) have the attribute security_level to medium except *admin*
        if "admin" in name:
            self.add_subject_attribute_assignments(
                subject_name=uuid,
                category="security_level",
                attributes=["security_high"])
        else:
            self.add_subject_attribute_assignments(
                subject_name=uuid,
                category="security_level",
                attributes=["security_medium"])

    def delete_attributes_from_vent(self, vent_uuid):
        attributes = []
        try:
            vent = self.get_subjects(uuid=vent_uuid).next()
            self.del_subject_attributes(uuid=vent_uuid)
            attributes.append(vent)
        except StopIteration:
            pass
        try:
            vent = self.get_objects(uuid=vent_uuid).next()
            self.del_object_attributes(uuid=vent_uuid)
            attributes.append(vent)
        except StopIteration:
            pass
        for attr in attributes:
            self.del_subject_attribute_assignments(uuid=attr)
            self.del_object_attribute_assignments(uuid=attr)
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
                try:
                    hl_uuid = self.get_subject_attributes(value=s_attr, category="security_level")[0]["uuid"]
                    if hl_uuid in map(lambda x: x["value"], rule["s_attr"]):
                        indexes.append(rule["uuid"])
                    break
                except IndexError:
                    pass
            for o_attr in o_attrs:
                try:
                    hl_uuid = self.get_object_attributes(value=o_attr, category="security_level")[0]["uuid"]
                    if hl_uuid in map(lambda x: x["value"], rule["s_attr"]):
                        indexes.append(rule["uuid"])
                    break
                except IndexError:
                    pass
        indexes.reverse()
        for index in indexes:
            IntraExtension.del_rule(self, uuid=index)

    def requesting_vent_create(self, vent, subjects_list):
        try:
            self.add_object(uuid=vent.uuid, name=vent.name, description="virtual entity")
        except DuplicateObjectException:
            pass
        # Assign the security_level vent_uuid to the virtual entity
        try:
            hl_uuid = self.get_object_attributes(value=vent.uuid, category="security_level").next()["uuid"]
        except StopIteration:
            hl_uuid = self.add_object_attributes(value=vent.uuid, category="security_level")
            self.add_object_attribute_assignments(
                object_name=vent.uuid,
                category="security_level",
                attributes=[hl_uuid, ])
        hl_name = self.get_object_attributes(value=vent.uuid, category="security_level").next()["value"]
        # Assign all actions to the virtual entity
        actions = self.get_object_attributes(category="action")
        for action in actions:
            self.add_object_attribute_assignments(
                object_name=vent.uuid,
                category="security_level",
                attributes=[action["uuid"]])
        # Add rules
        #TODO what append if one of the subjects doesn't have the security_level to high ?
        self.add_rule(
            name="requesting_rule_vent_{}".format(str(uuid4())),
            subject_attrs=[
                {u'category': u'security_level', u'value': hl_name},
            ],
            object_attrs=[
                {u'category': u'id', u'value': vent.uuid},
                {u'category': u'action', u'value': [x["uuid"] for x in actions]},
            ],
            description="Rule for security_level high in order to use the virtual entity {}".format(
                vent.uuid
            ),)

    def requested_vent_create(self, vent, objects_list):
        try:
            self.add_subject(uuid=vent.uuid, name=vent.name, description="virtual entity")
        except DuplicateSubjectException:
            pass
        # Assign the security_level vent_uuid to the virtual entity
        try:
            hl = self.get_subject_attributes(value=vent.uuid, category="security_level").next()
        except StopIteration:
            hl = self.add_subject_attributes(value=vent.uuid, category="security_level")
            self.add_subject_attribute_assignments(
                subject_name=vent.uuid,
                category="security_level",
                attributes=[hl["uuid"], ])
        actions = self.get_object_attributes(category="action")
        for obj in objects_list:
            _actions = []
            assign = self.get_object_attribute_assignments(uuid=obj)
            for action in actions:
                if action["value"] in assign["attributes"]:
                    _actions.append(action)
            self.add_rule(
                name="requested_rule_vent_{}".format(str(uuid4())),
                subject_attrs=[
                    {u'category': u'security_level', u'value': hl["uuid"]},
                ],
                object_attrs=[
                    {u'category': u'id', u'value': obj},
                    {u'category': u'action', u'value': [x["value"] for x in _actions]},
                ],
                description="Rule for security_level high in order to use the virtual entity {}".format(
                    vent.uuid
                )
            )
