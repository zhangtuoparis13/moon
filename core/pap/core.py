"""
"""
import logging
import os
import json
from uuid import uuid4
from moon import settings
from moon.core.pdp import get_intra_extensions
from moon.core.pdp import get_inter_extensions
# from moon.core.pdp import Extension
from moon.core.pip import get_pip

logger = logging.getLogger("moon.pap")


class PAP:

    def __init__(self):
        self.intra_extensions = get_intra_extensions()
        self.inter_extensions = get_inter_extensions()
        self.tenants = get_inter_extensions().tenants

    def get_intra_extensions(self, uuid=None):
        if not uuid:
            return self.intra_extensions.values()
        elif uuid and uuid in self.intra_extensions.keys():
            return self.intra_extensions[uuid]

    ##########################################
    # Specific functions for Keystone and Nova
    ##########################################

    @staticmethod
    def get_tenants(name=None, uuid=None):
        return get_pip().get_tenants(name=name, uuid=uuid)

    ##################################################
    # Specific functions for Intra-Extension interface
    ##################################################

    def get_subjects(self, extension_uuid, user_uuid):
        if extension_uuid in self.intra_extensions.values():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subjects", "r") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_subjects()

    def add_subject(self, extension_uuid, user_uuid, subject_id):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "subjects", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.add_subject(subject_id)

    def del_subject(self, extension_uuid, user_uuid, subject_id):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "subjects", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.del_subject(subject_id)
                #TODO need to check if the subject is not in other tables like assignment

    def get_objects(self, extension_uuid, user_uuid):
        if extension_uuid in self.intra_extensions.values():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "objects", "r") == "OK":
                return self.intra_extensions[extension_uuid].authz_extension.get_objects()

    def add_object(self, extension_uuid, user_uuid, object_id):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "objects", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.add_object(object_id)

    def del_object(self, extension_uuid, user_uuid, object_id):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "objects", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.del_object(object_id)
                #TODO need to check if the subject is not in other tables like assignment

    def get_subject_categories(self, extension_uuid, user_uuid):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "subject_categories", "r") == "OK":
                return self.intra_extensions[extension_uuid].authz_extension.get_subject_categories()

    def add_subject_category(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "subject_categories", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.add_subject_category(category_id)

    def del_subject_category(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "subject_categories", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.del_subject_category(category_id)

    def get_object_categories(self, extension_uuid, user_uuid):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "object_categories", "r") == "OK":
                return self.intra_extensions[extension_uuid].authz_extension.get_object_categories()

    def add_object_category(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "object_categories", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.add_object_category(category_id)

    def del_object_category(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "object_categories", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.del_object_category(category_id)

    def get_meta_rules(self, extension_uuid, user_uuid):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "meta_rules", "r") == "OK":
                return self.intra_extensions[extension_uuid].authz_extension.get_meta_rules()

    def add_meta_rules(self, extension_uuid, user_uuid, rule):
        if extension_uuid in self.intra_extensions:
            #TODO to be defined
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "meta_rules", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.add_meta_rules(rule)

    def del_meta_rules(self, extension_uuid, user_uuid, rule_id):
        if extension_uuid in self.intra_extensions:
            #TODO to be defined
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "meta_rules", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.del_meta_rules(rule_id)

    def get_subject_category_values(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "subject_category_values", "r") == "OK":
                return self.intra_extensions[extension_uuid].authz_extension.get_subject_category_values(category_id)

    def add_subject_category_values(self, extension_uuid, user_uuid, category_id, category_value):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "subject_category_values", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.add_subject_category_values(category_id, category_value)

    def del_subject_category_values(self, extension_uuid, user_uuid, category_id, category_value):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "subject_category_values", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.del_subject_category_values(category_id, category_value)
                #TODO need to check if the value is not in other tables like assignment

    def get_object_category_values(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "object_category_values", "r") == "OK":
                return self.intra_extensions[extension_uuid].authz_extension.get_object_category_values(category_id)

    def add_object_category_values(self, extension_uuid, user_uuid, category_id, category_value):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "object_category_values", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.add_object_category_values(category_id, category_value)

    def del_object_category_values(self, extension_uuid, user_uuid, category_id, category_value):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "object_category_values", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.del_object_category_values(category_id, category_value)
                #TODO need to check if the value is not in other tables like assignment

    def get_subject_assignments(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "subject_category_assignments", "r") == "OK":
                return self.intra_extensions[extension_uuid].authz_extension.get_subject_assignments(category_id)

    def add_subject_assignment(self, extension_uuid, user_uuid, category_id, subject_id, category_value):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "subject_category_assignments", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.add_subject_assignment(
                    category_id, subject_id, category_value
                )

    def del_subject_assignment(self, extension_uuid, user_uuid, category_id, subject_id, category_value):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "subject_category_assignments", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.del_subject_assignment(
                    category_id, subject_id, category_value
                )

    def get_object_assignments(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "object_category_assignments", "r") == "OK":
                return self.intra_extensions[extension_uuid].authz_extension.get_object_assignments(category_id)

    def add_object_assignment(self, extension_uuid, user_uuid, category_id, object_id, category_value):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "object_category_assignments", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.add_object_assignment(
                    category_id, object_id, category_value
                )

    def del_object_assignment(self, extension_uuid, user_uuid, category_id, object_id, category_value):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "object_category_assignments", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.del_object_assignment(
                    category_id, object_id, category_value
                )

    def get_rules(self, extension_uuid, user_uuid):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "rules", "r") == "OK":
                return self.intra_extensions[extension_uuid].authz_extension.get_rules()

    def add_rule(self, extension_uuid, user_uuid, name, subject_attrs, object_attrs, description=""):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "rules", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.add_rules(name, subject_attrs, object_attrs, description)

    def del_rule(self, extension_uuid, user_uuid, rule_id):
        if extension_uuid in self.intra_extensions:
            if self.intra_extensions[extension_uuid].admin_extension.authz(user_uuid, "rules", "w") == "OK":
                self.intra_extensions[extension_uuid].authz_extension.add_rules(rule_id)

    ########################################
    # Specific functions for Intra-Extension
    ########################################

    def add_from_json(self, json_directory):
        get_intra_extensions().install_intra_extension_from_json(json_directory)

    def add_from_db(self):
        get_intra_extensions().install_intra_extension_from_db()

    #########################################
    # Specific functions for Inter Extensions
    #########################################

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
        ext = self.inter_pdps.get(uuid=uuid)[0]
        vent_uuid = ext.get_vent()
        self.intra_pdps.delete_rules(s_attrs=vent_uuid, o_attrs=vent_uuid)
        try:
            self.intra_pdps.delete_attributes_from_vent(uuid=vent_uuid)
        except:
            import sys
            print(sys.exc_info())
        self.inter_pdps.delete(uuid=uuid)

    ###########################################
    # Misc functions for Intra/Inter-Extensions
    ###########################################

    def sync_db_with_keystone(self, tenant_uuid=None):
        pip = get_pip()
        logs = ""
        json_data = None
        pip.set_creds_for_tenant()
        for tenant in self.get_tenants():
            #TODO: if new tenant
            #       -> need to add a new intra extension
            #       -> need to add a new inter extension with a new vent
            #TODO: if not new tenant -> need to synchronize users, roles, ...
            # extension = get_intra_dd().sync_extension(
            #     tenant_uuid=tenant["uuid"],
            #     users=self.get_subjects(client),
            #     roles=self.get_roles(client),
            #     groups=self.get_groups(client))
            if tenant_uuid and not tenant_uuid == tenant["uuid"]:
                continue
            SYNC_CONF_FILENAME = getattr(settings, "SYNC_CONF_FILENAME", None)
            sync = json.loads(open(SYNC_CONF_FILENAME).read())
            if SYNC_CONF_FILENAME:
                if tenant["name"] not in map(lambda x: x["name"], sync["tenants"]):
                    logs += "Tenant {} not in configuration file -> KO".format(tenant["name"])
                    continue
                for conf in sync["tenants"]:
                    if conf["name"] == tenant["name"]:
                        if not os.path.isfile(conf["extension_conf"]):
                            raise Exception("Unable to find configuration file {}".format(conf["extension_conf"]))
                        json_data = json.loads(file(conf["extension_conf"]).read())
            logger.info("Syncing tenant {}".format(tenant["name"]))
            logs += "Syncing {}".format(tenant["name"])
            try:
                pip.set_creds_for_tenant(tenant["name"])
            except pip.Unauthorized:
                logger.warning("Cannot authenticate in tenant {}".format(tenant["name"]))
                logs += " KO (Cannot authenticate in tenant)\n"
                continue
            self.inter_extensions().add_tenant(
                name=tenant["name"],
                description=tenant["description"],
                enabled=tenant["enabled"],
                domain=tenant["domain"],
                uuid=tenant["uuid"]
            )
            try:
                self.new_intra_extension(tenant=tenant, json_data=json_data)
                logs += " OK\n"
            except pip.Forbidden:
                logger.warning("Cannot list users in tenant {}".format(tenant["name"]))
                logs += " KO (Cannot list users in tenant)\n"
                continue
        return logs

    def delete_tables(self):
        self.intra_extensions.delete_tables()
        self.inter_extensions.delete_tables()


pap = PAP()


def get_pap():
    return pap