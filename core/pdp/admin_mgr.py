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
            ext = self.intra_dispatcher.get(attributes={"tenant.uuid": tenant_uuid})[0]
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
        assignment = self.inter_dispatcher.add_tenant_assignment(
            requested=requested,
            requesting=requesting,
            type=type,
        )
        requesting_tenant = self.get_tenant(tenant_uuid=requesting)[0]
        requesting_extension = self.get_intra_extensions(tenant_uuid=requesting)[0]
        requested_tenant = self.get_tenant(tenant_uuid=requested)[0]
        requested_extension = self.get_intra_extensions(tenant_uuid=requested)[0]
        vent = self.get_virtual_entity(uuid=assignment["category"])
        for ext in (requesting_extension, requested_extension):
            if not ext.has_object_attributes(name="virtual_entity"):
                ext.add_object_attribute(
                    category="type",
                    value="virtual_entity",
                    description="Virtual entity for {} to {}".format(
                        requesting_tenant["name"],
                        requested_tenant["name"]))
        requesting_extension.add_object(uuid=vent["uuid"], name=vent["name"], description="Virtual Entity")
        requesting_extension.add_object_attributes_relation(
            object=vent["uuid"],
            attributes=[requesting_extension.get_object_attributes(name="virtual_entity", category="type"), ]
        )
        requested_extension.add_subject(uuid=vent["uuid"], name=vent["name"], description="Virtual Entity")
        requested_extension.add_object_attributes_relation(
            object=vent["uuid"],
            attributes=[requested_extension.get_object_attributes(name="virtual_entity", category="type"), ]
        )
        return assignment

    def get_virtual_entity(self, uuid=None, name=None):
        return self.inter_dispatcher.get_virtual_entity(uuid=uuid, name=name)

manager = AdminManager()


def get_manager():
    return manager