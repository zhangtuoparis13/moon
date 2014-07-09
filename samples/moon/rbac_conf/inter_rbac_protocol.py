from moon.core.pdp.intra_extension import IntraExtension
from uuid import uuid4


class RBACIntraExtension(IntraExtension):

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
        super(RBACIntraExtension, self).__init__(
            name=name,
            uuid=uuid,
            subjects=subjects,
            objects=objects,
            metadata=metadata,
            rules=rules,
            profiles=profiles,
            description=description,
            tenant=tenant,
            model=model,
            protocol=protocol)

    def add_object(self, uuid=None, name=None, enabled=True, description=""):
        #HYPOTHESIS: objects are only virtual servers, so linking all objects to type server
        uuid = uuid.replace("-", "")
        IntraExtension.add_object(self, uuid=uuid, name=name, enabled=enabled, description=description)
        # Default: all objects (ie all VM) have the attribute id linked to the uuid of the object
        attr_uuid = self.add_object_attribute(category="id", value=uuid, description="attribute id for {}".format(name))
        self.add_object_attributes_relation(object=uuid, attributes=[attr_uuid])
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
        # No need to add roles, they have been already added

    # def delete_object(self, uuid):
    #     # Suppresion de l'objet
    #     IntraExtension.delete_object()
    #     # Suppression des o_attr et o_attr_assign associes

    def requesting_vent_create(self, vent, subjects_list):
        if not self.has_object(uuid=vent.uuid):
            self.add_object(uuid=vent.uuid, name=vent.name, description="virtual entity")
        # Get or Create the virtual entity role
        try:
            vent_role = self.get_subject_attributes(name="virtual_entity_role", category="role")[0]
        except IndexError:
            #Create it
            self.add_subject_attribute(
                value="virtual_entity_role",
                category="role",
                description="The role for managing virtual entities")
            vent_role = self.get_subject_attributes(name="virtual_entity_role", category="role")[0]
        #Create relation between subjects and virtual_entity_role
        for subject_uuid in subjects_list:
            if not self.has_subject_attributes_relation(uuid=subject_uuid, attribute=vent_role["uuid"]):
                self.add_subject_attributes_relation(
                    subject=subject_uuid,
                    attributes=[vent_role["uuid"]]
                )
        # Create an attribute "id" for the Vent
        if not self.has_object_attributes(name=vent["uuid"], category="id"):
            _uuid = self.add_object_attribute(
                category="id",
                value=vent["uuid"],
                description="object attribute for the vent")
            self.add_object_attributes_relation(object=vent.uuid, attributes=[_uuid, ])
        # Assign all actions to the virtual entity
        actions = self.get_object_attributes(category="action")
        for action in actions:
            self.add_object_attributes_relation(object=vent.uuid, attributes=[action["uuid"]])
        # Add rules
        rule = {
            "name": "requesting_rule_vent_{}".format(str(uuid4())),
            "description": "Rule for role {} in order to use the virtual entity {}".format(
                vent_role["uuid"],
                vent.uuid
            ),
            "s_attr": [
                {u'category': u'role', u'value': vent_role["uuid"]},
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
        # Get or Create the virtual entity role
        try:
            vent_role = self.get_subject_attributes(name="virtual_entity_role", category="role")[0]
        except IndexError:
            #Create it
            self.add_subject_attribute(
                value="virtual_entity_role",
                category="role",
                description="The role for managing virtual entities")
            vent_role = self.get_subject_attributes(name="virtual_entity_role", category="role")[0]
        #Create relation between virtual entity and virtual_entity_role
        self.add_subject_attributes_relation(
            subject=vent.uuid,
            attributes=[vent_role["uuid"]]
        )
        # Add rules
        actions = self.get_object_attributes(category="action")
        for obj in objects_list:
            _id_obj = self.get_object_attributes(category="id", name=obj)[0]["uuid"]
            _actions = []
            for action in actions:
                if self.has_object_attributes_relation(uuid=obj, attribute=action["uuid"]):
                    _actions.append(action)
            rule = {
                "name": "requested_rule_vent_{}".format(str(uuid4())),
                "description": "Rule for role {} in order to use the virtual entity {}".format(
                    vent_role["uuid"],
                    vent.uuid
                ),
                "s_attr": [
                    {u'category': u'role', u'value': vent_role["uuid"]},
                ],
                "o_attr": [
                    {u'category': u'id', u'value': _id_obj},
                    {u'category': u'action', u'value': [x["value"] for x in _actions]},
                ],
            }
            self.add_rule(rule)
