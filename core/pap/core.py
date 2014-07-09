"""
"""
import logging
from intra_extension_manager import get_dispatcher as get_intra_dispatcher
from inter_extension_manager import get_dispatcher as get_inter_dispatcher
from moon.core.pdp.inter_extension import get_inter_extentions
from moon.core.pdp.intra_extension import get_intra_extentions


logger = logging.getLogger("moon.pap")


class PAP:
    """
    Policy Administration Point
    """

    def __init__(self, kclient=None):
        if not kclient:
            self.kclient = None
            # TODO: need authentication
        else:
            self.kclient = kclient
        self.admin_manager = get_manager()

    def get_roles(self, extension_uuid):
        return self.admin_manager.get_roles(extension_uuid=extension_uuid)

    def get_groups(self, extension_uuid):
        return self.admin_manager.get_groups(extension_uuid=extension_uuid)

    def get_object_attributes(self, extension_uuid, category=None):
        return self.admin_manager.get_object_attributes(extension_uuid=extension_uuid, category=category)

    def get_subject_attributes(self, extension_uuid, category=None):
        return self.admin_manager.get_subject_attributes(extension_uuid=extension_uuid, category=category)


class AdminManager:

    def __init__(self):
        self.intra_pdps = get_intra_extentions()
        self.inter_pdps = get_inter_extentions()
        self.tenants = get_inter_extentions().tenants

    def get_intra_extensions(self, uuid=None, tenant_uuid=None, tenant_name=None):
        if not uuid and not tenant_uuid:
            return self.intra_pdps.get()
        elif uuid and uuid in self.intra_pdps.keys():
            return self.intra_pdps.get(uuid=uuid)
        elif tenant_uuid:
            for ext in self.intra_pdps.get():
                if ext.tenant["uuid"] == tenant_uuid:
                    return ext
        elif tenant_name:
            for ext in self.intra_pdps.get():
                if ext.tenant["name"] == tenant_name:
                    return ext

    def get_users(self, extension_uuid=None, uuid=None, name=None, tenant_uuid=None):
        if tenant_uuid:
            try:
                ext = self.intra_pdps.get(attributes={"tenant.uuid": tenant_uuid})[0]
            except IndexError:
                return []
            return self.intra_pdps.get(ext.uuid)[0].get_subject(uuid=uuid, name=name)
        else:
            return self.intra_pdps.get(extension_uuid)[0].get_subject(uuid=uuid, name=name)

    def get_objects(self, extension_uuid=None, uuid=None, name=None, tenant_uuid=None):
        if tenant_uuid:
            try:
                ext = self.intra_pdps.get(attributes={"tenant.uuid": tenant_uuid})[0]
                return ext.get_object(uuid=uuid, name=name)
            except IndexError:
                return []
        else:
            return self.intra_pdps.get(extension_uuid)[0].get_object(uuid=uuid, name=name)

    def get_roles(self, extension_uuid=None, uuid=None, name=None):
        return self.intra_pdps.get(uuid=extension_uuid)[0].get_subject_attributes(uuid=uuid, name=name, category="role")

    def get_groups(self, extension_uuid=None, uuid=None, name=None):
        return self.intra_pdps.get(uuid=extension_uuid)[0].get_subject_attributes(uuid=uuid, name=name, category="group")

    def get_object_attributes(self, extension_uuid=None, uuid=None, name=None, category=None):
        return self.intra_pdps.get(uuid=extension_uuid)[0].get_object_attributes(uuid=uuid, name=name, category=category)

    def get_subject_attributes(self, extension_uuid=None, uuid=None, name=None, category=None):
        return self.intra_pdps.get(uuid=extension_uuid)[0].get_subject_attributes(uuid=uuid, name=name, category=category)

    def get_tenant(self, tenant_uuid=None, tenant_name=None):
        if not tenant_uuid and not tenant_name:
            return self.inter_pdps.list()
        else:
            return self.inter_pdps.get(uuid=tenant_uuid, name=tenant_name)

    def get_inter_extensions(self, uuid=None):
        return self.inter_pdps.get(uuid=uuid)

    def add_inter_extension(self,
                            requesting=None,
                            requested=None,
                            connexion_type=None,
                            requesting_subjects=None,
                            requested_objects=None):
        """Add a new Inter Tenant Extension

        :param requesting: UUID of the requesting tenant
        :param requested: UUID of the requested tenant
        :param connexion_type: connexion_type of the connection ("trust", "coordinate", ...)
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
        assignment = self.inter_pdps.add_tenant_assignment(
            requested=requested,
            requesting=requesting,
            type=connexion_type,
        )
        requesting_extension = self.get_intra_extensions(tenant_uuid=requesting)
        requested_extension = self.get_intra_extensions(tenant_uuid=requested)
        #Get the Virtual entity created during the creation of "assignment"
        vent = self.get_virtual_entity(uuid=assignment.category)[0]
        requesting_extension.requesting_vent_create(vent, requesting_subjects)
        requested_extension.requested_vent_create(vent, requested_objects)
        return assignment

    def get_virtual_entity(self, uuid=None, name=None):
        return self.inter_pdps.get_virtual_entity(uuid=uuid, name=name)

    def delete_inter_extension(self, uuid):
        self.inter_pdps.delete(uuid=uuid)

manager = AdminManager()


def get_manager():
    return manager