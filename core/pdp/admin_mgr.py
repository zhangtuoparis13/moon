from intra_extension_manager import get_dispatcher as get_intra_dispatcher
from inter_extension_manager import get_dispatcher as get_inter_dispatcher
from uuid import uuid4
import logging


class AdminManager:

    def __init__(self):
        self.intra_dispatcher = get_intra_dispatcher()
        self.inter_dispatcher = get_inter_dispatcher()
        self.intra_pdps = self.intra_dispatcher.extensions
        self.inter_pdps = self.inter_dispatcher.extensions
        self.tenants = self.inter_dispatcher.tenants

    def get_intra_extensions(self, uuid=None, tenant_uuid=None, tenant_name=None):
        if not uuid and not tenant_uuid:
            return self.intra_pdps.values()
        elif uuid and uuid in self.intra_pdps:
            return self.intra_pdps[uuid]
        elif tenant_uuid:
            for ext in self.intra_pdps.values():
                if ext.tenant["uuid"] == tenant_uuid:
                    return ext
        elif tenant_name:
            for ext in self.intra_pdps.values():
                if ext.tenant["name"] == tenant_name:
                    return ext

    def get_users(self, extension_uuid=None, uuid=None, name=None, tenant_uuid=None):
        if tenant_uuid:
            try:
                ext = self.intra_dispatcher.get(attributes={"tenant.uuid": tenant_uuid})[0]
            except IndexError:
                return []
            return self.intra_pdps[ext.uuid].get_subject(uuid=uuid, name=name)
        else:
            return self.intra_pdps[extension_uuid].get_subject(uuid=uuid, name=name)

    def get_objects(self, extension_uuid=None, uuid=None, name=None, tenant_uuid=None):
        if tenant_uuid:
            ext = self.intra_dispatcher.get(attributes={"tenant.uuid": tenant_uuid})[0]
            return self.intra_pdps[ext.uuid].get_object(uuid=uuid, name=name)
        else:
            return self.intra_pdps[extension_uuid].get_object(uuid=uuid, name=name)

    def get_roles(self, extension_uuid=None, uuid=None, name=None):
        return self.intra_pdps[extension_uuid].get_subject_attributes(uuid=uuid, name=name, category="role")

    def get_groups(self, extension_uuid=None, uuid=None, name=None):
        return self.intra_pdps[extension_uuid].get_subject_attributes(uuid=uuid, name=name, category="group")

    def get_object_attributes(self, extension_uuid=None, uuid=None, name=None, category=None):
        return self.intra_pdps[extension_uuid].get_object_attributes(uuid=uuid, name=name, category=category)

    def get_subject_attributes(self, extension_uuid=None, uuid=None, name=None, category=None):
        return self.intra_pdps[extension_uuid].get_subject_attributes(uuid=uuid, name=name, category=category)

    def get_tenant(self, tenant_uuid=None, tenant_name=None):
        if not tenant_uuid and not tenant_name:
            return self.inter_dispatcher.list()
        else:
            return self.inter_dispatcher.get(uuid=tenant_uuid, name=tenant_name)

    def get_inter_extensions(self, uuid=None):
        return self.inter_dispatcher.get(uuid=uuid)

    def add_inter_extension(self,
                            requesting=None,
                            requested=None,
                            type=None,
                            requesting_subjects=None,
                            requested_objects=None):
        """Add a new Inter Tenant Extension

        :param requesting: UUID of the requesting tenant
        :param requested: UUID of the requested tenant
        :param type: type of the connection ("trust", "coordinate", ...)
        :param requesting_subjects: list of subjects for rule creation
        :param requested_objects: list of objects for rule creation
        :return: new extension

        Methodology:
        - Add tenant assignment
        - Add virtual entity object vent1 in requesting tenant
        - Add relation (in o_attrs_assignment) from vent1 to o_attrs.virtual_entity in requesting tenant
        - Add virtual entity subject vent2 in requested tenant
        - Add relation (in o_attrs_assignment) from vent2 to o_attrs.virtual_entity in requested tenant
        - Add rule from one or more subjects to vent1 in requesting tenant
        - Add rule from one or more objects to vent2 in requested tenant
        """
        #Add tenant assignment
        assignment = self.inter_dispatcher.add_tenant_assignment(
            requested=requested,
            requesting=requesting,
            type=type,
        )
        requesting_tenant = self.get_tenant(tenant_uuid=requesting)[0]
        requesting_extension = self.get_intra_extensions(tenant_uuid=requesting)
        requested_tenant = self.get_tenant(tenant_uuid=requested)[0]
        requested_extension = self.get_intra_extensions(tenant_uuid=requested)
        #Get the Virtual entity created during the creation of "assignment"
        vent = self.get_virtual_entity(uuid=assignment.category)[0]
        #Get virtual entity role and create it if it doesn't exist
        try:
            vent_role = requesting_extension.get_subject_attributes(name="virtual_entity_role", category="role")[0]
        except IndexError:
            #Create it
            requesting_extension.add_subject_attribute(
                value="virtual_entity_role",
                category="role",
                description="The role for managing virtual entities")
            vent_role = requesting_extension.get_subject_attributes(name="virtual_entity_role", category="role")[0]
        print("vent_role={} for {}".format(vent_role, requesting_extension.profiles["s_attr"]))
        #Create relation between subjects and virtual_entity_role
        for subject_uuid in requesting_subjects:
            if not requesting_extension.has_subject_attributes_relation(uuid=subject_uuid, attribute=vent_role["uuid"]):
                requesting_extension.add_subject_attributes_relation(
                    object=subject_uuid,
                    attributes=[vent_role["uuid"]]
                )
        for ext in (requesting_extension, requested_extension):
            #Create the virtual_entity type
            # if not ext.has_object_attributes(name="virtual_entity", category="type"):
            #     ext.add_object_attributes(value="virtual_entity", category="type")
            #Create the "security_level" type
            if not ext.has_object_attributes(category="security_level", name=vent.uuid):
                #add the category security_level->vent_uuid1 to the o_attr requested_extension
                slevel_uuid = ext.add_object_attribute(
                    category="security_level",
                    value=vent.uuid,
                    description="Virtual entity for {} to {}".format(
                        requesting_tenant.name,
                        requested_tenant.name))
                for obj in requested_objects:
                    #add a relation in o_attr_assign from object to security_level.ventuuid
                    ext.add_object_attributes_relation(
                        object=obj,
                        attributes=[slevel_uuid]
                    )
            if not ext.has_subject_attributes(category="security_level", name=vent.uuid):
                #add the category security_level->vent_uuid1 to the s_attr requested_extension
                slevel_uuid = ext.add_subject_attribute(
                    category="security_level",
                    value=vent.uuid,
                    description="Virtual entity for {} to {}".format(
                        requesting_tenant.name,
                        requested_tenant.name))
                for sbj in requesting_subjects:
                    #add a relation in s_attr_assign from subject to security_level.ventuuid
                    ext.add_subject_attributes_relation(
                        object=sbj,
                        attributes=[slevel_uuid]
                    )
        #Add virtual entity object vent1 in requesting tenant
        requesting_extension.add_object(uuid=vent.uuid, name=vent.name, description="Virtual Entity")
        requesting_extension.add_object_attributes_relation(
            object=vent.uuid,
            attributes=[
                requesting_extension.get_object_attributes(name=vent.uuid, category="security_level")[0]["uuid"]
            ]
            # attributes=[requesting_extension.get_object_attributes(name="virtual_entity", category="type"), ]
        )
        #Add virtual entity subject vent2 in requested tenant
        requested_extension.add_subject(uuid=vent.uuid, name=vent.name, description="Virtual Entity")
        requested_extension.add_object_attributes_relation(
            object=vent.uuid,
            attributes=[
                requested_extension.get_object_attributes(name=vent.uuid, category="security_level")[0]["uuid"]
            ]

            # attributes=[requested_extension.get_object_attributes(name="virtual_entity", category="type"), ]
        )
        #Add rule from one or more subjects to vent1 in requesting tenant
        slevel_uuid = requesting_extension.get_object_attributes(name=vent.uuid, category="security_level")[0]["uuid"]
        rule = {
            "name": "rule_vent_{}".format(vent_role["uuid"]),
            "description": "Rule for role {} in order to use the virtual entity {}".format(
                vent_role["uuid"],
                vent.uuid
            ),
            "s_attr": [
                {u'category': u'role', u'value': vent_role["value"]},
            ],
            "o_attr": [
                {u'category': u'security_level', u'value': slevel_uuid},
            ],
        }
        requesting_extension.add_rule(rule)
        #Add rule from one or more objects to vent2 in requested tenant
        slevel_uuid = requested_extension.get_object_attributes(name=vent.uuid, category="security_level")[0]["uuid"]
        rule = {
            "name": "rule_vent_{}".format(vent_role["uuid"]),
            "description": "Rule for role {} in order to use the virtual entity {}".format(
                vent_role["uuid"],
                vent.uuid
            ),
            "s_attr": [
            #     {u'category': u'security_level', u'value': slevel_uuid},
            ],
            "o_attr": [
                {u'category': u'security_level', u'value': slevel_uuid},
            ],
        }
        requested_extension.add_rule(rule)
        return assignment

    def get_virtual_entity(self, uuid=None, name=None):
        return self.inter_dispatcher.get_virtual_entity(uuid=uuid, name=name)

manager = AdminManager()


def get_manager():
    return manager