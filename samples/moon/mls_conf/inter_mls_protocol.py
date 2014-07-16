from moon.core.pdp.intra_extension import IntraExtension
from uuid import uuid4


class MLSIntraExtension(IntraExtension):

    # def __init__(
    #         self,
    #         name="",
    #         uuid=None,
    #         subjects=None,
    #         objects=None,
    #         metadata=None,
    #         rules=None,
    #         profiles=None,
    #         description="",
    #         tenant=None,
    #         model="RBAC",
    #         protocol=None):
    #     super(MLSIntraExtension, self).__init__(
    #         name=name,
    #         uuid=uuid,
    #         subjects=subjects,
    #         objects=objects,
    #         metadata=metadata,
    #         rules=rules,
    #         profiles=profiles,
    #         description=description,
    #         tenant=tenant,
    #         model=model,
    #         protocol=protocol)

    def add_object(self, uuid=None, name=None, enabled=True, description=""):
        #HYPOTHESIS: objects are only virtual servers, so linking all objects to type server
        IntraExtension.add_object(self, uuid=uuid, name=name, enabled=enabled, description=description)
        # Default: all objects (ie all VM) have the attribute security_level to medium
        self.add_object_attributes_relation(object=uuid, attributes=["security_medium"])
        # Default: all objects (ie all VM) have all attribute action
        actions = self.get_object_attributes(category="action")
        for action in actions:
            self.add_object_attributes_relation(object=uuid, attributes=[action["uuid"]])

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
            self.add_subject_attributes_relation(subject=uuid, attributes=["security_high"])
        else:
            self.add_subject_attributes_relation(subject=uuid, attributes=["security_medium"])

    def delete_attributes_from_vent(self, vent_uuid):
        attributes = []
        if self.has_subject_attributes(name=vent_uuid, category="security_level"):
            attributes.append(self.delete_subject_attributes(name=vent_uuid))
        if self.has_object_attributes(name=vent_uuid, category="security_level"):
            attributes.append(self.delete_object_attributes(name=vent_uuid))
        self.delete_attributes_relations(s_attrs=attributes, o_attrs=attributes)
        IntraExtension.delete_attributes_from_vent(self, vent_uuid=vent_uuid)

    def delete_rules(self, s_attrs=[], o_attrs=[]):
        if type(s_attrs) not in (list, tuple):
            s_attrs = [s_attrs, ]
        if type(o_attrs) not in (list, tuple):
            o_attrs = [o_attrs, ]
        indexes = []
        for index, rule in enumerate(self.get_rules()):
            for s_attr in s_attrs:
                try:
                    hl_uuid = self.get_subject_attributes(name=s_attr, category="security_level")[0]["uuid"]
                    if hl_uuid in map(lambda x: x["value"], rule["s_attr"]):
                        indexes.append(index)
                    break
                except IndexError:
                    pass
            for o_attr in o_attrs:
                try:
                    hl_uuid = self.get_object_attributes(name=o_attr, category="security_level")[0]["uuid"]
                    if hl_uuid in map(lambda x: x["value"], rule["s_attr"]):
                        indexes.append(index)
                    break
                except IndexError:
                    pass
        indexes.reverse()
        for index in indexes:
            try:
                self.get_rules().pop(index)
            except IndexError:
                pass
        IntraExtension.delete_rules(self, s_attrs=s_attrs, o_attrs=o_attrs)

    def requesting_vent_create(self, vent, subjects_list):
        if not self.has_object(uuid=vent.uuid):
            self.add_object(uuid=vent.uuid, name=vent.name, description="virtual entity")
        # Assign the security_level vent_uuid to the virtual entity
        try:
            hl_uuid = self.get_object_attributes(name=vent.uuid, category="security_level")[0]
        except IndexError:
            hl_uuid = self.add_object_attribute(value=vent.uuid, category="security_level")
            self.add_object_attributes_relation(object=vent.uuid, attributes=[hl_uuid, ])
        # Assign all actions to the virtual entity
        actions = self.get_object_attributes(category="action")
        for action in actions:
            self.add_object_attributes_relation(object=vent.uuid, attributes=[action["uuid"]])
        # Add rules
        #TODO what append if one of the subjects doesn't have the security_level to high ?
        rule = {
            "name": "requesting_rule_vent_{}".format(str(uuid4())),
            "description": "Rule for security_level high in order to use the virtual entity {}".format(
                vent.uuid
            ),
            "s_attr": [
                {u'category': u'security_level', u'value': hl_uuid},
            ],
            "o_attr": [
                {u'category': u'id', u'value': vent.uuid},
                {u'category': u'action', u'value': [x["uuid"] for x in actions]},
            ],
        }
        self.add_rule(rule)

    def requested_vent_create(self, vent, objects_list):
        if not self.has_subject(uuid=vent.uuid):
            self.add_subject(uuid=vent.uuid, name=vent.name, description="virtual entity")
        # Assign the security_level vent_uuid to the virtual entity
        try:
            hl_uuid = self.get_subject_attributes(name=vent.uuid, category="security_level")[0]
        except IndexError:
            hl_uuid = self.add_subject_attribute(value=vent.uuid, category="security_level")
            self.add_subject_attributes_relation(subject=vent.uuid, attributes=[hl_uuid, ])
        actions = self.get_object_attributes(category="action")
        for obj in objects_list:
            _actions = []
            for action in actions:
                if self.has_object_attributes_relation(uuid=obj, attribute=action["uuid"]):
                    _actions.append(action)
            rule = {
                "name": "requested_rule_vent_{}".format(str(uuid4())),
                "description": "Rule for security_level high in order to use the virtual entity {}".format(
                    vent.uuid
                ),
                "s_attr": [
                    {u'category': u'security_level', u'value': hl_uuid},
                ],
                "o_attr": [
                    {u'category': u'id', u'value': obj},
                    {u'category': u'action', u'value': [x["value"] for x in _actions]},
                ],
            }
            self.add_rule(rule)
