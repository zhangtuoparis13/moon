from moon.core.pdp.intra_extension import IntraExtension


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
        # Default: all objects (ie all VM) have some attribute action
        self.add_object_attributes_relation(object=uuid, attributes=[
            "action-get",
            "action-post",
            "action-delete",
            "action-post.os-start"])

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
        # TODO: Ajout des s_attr et s_attr_assign qui vont bien

    # def delete_object(self, uuid):
    #     # Suppresion de l'objet
    #     IntraExtension.delete_object()
    #     # Suppression des o_attr et o_attr_assign associes

    def requesting_vent_create(self, vent, subjects_list):
        print("\033[34mrbac requesting_vent_create {} {} {}\033[m".format(self, vent, subjects_list))
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

    def requested_vent_create(self, vent, objects_list):
        print("\033[34mrbac_requested_vent_create {} {} {}\033[m".format(self, vent, objects_list))
