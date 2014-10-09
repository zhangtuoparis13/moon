"""
"""
import os
import json
from moon import settings
from moon.core.pdp import get_intra_extensions
from moon.core.pdp import get_inter_extensions
from moon.core.pdp import get_super_extension
from moon.core.pdp import get_tenant_intra_extension_mapping
from moon.core.pip import get_pip
from moon.tools.log import get_sys_logger


sys_logger = get_sys_logger()


class PAP:

    def __init__(self):
        self.intra_extensions = get_intra_extensions()
        self.inter_extensions = get_inter_extensions()
        # self.tenants = get_inter_extensions().tenants
        self.super_extension = get_super_extension()
        self.tenant_intra_extension_mapping = get_tenant_intra_extension_mapping()

    ###########################################
    # Misc functions for Super-Extension
    ###########################################

    def get_tenants(self):
        pip = get_pip()
        return pip.get_tenants()

    def get_intra_extensions(self, uuid=None):
        if not uuid:
            return self.intra_extensions.values()
        elif uuid and uuid in self.intra_extensions.keys():
            return self.intra_extensions[uuid]

    def list_mappings(self, user_id):
        if self.super_extension.admin(user_id, "mapping", "list") == "OK":
            return self.tenant_intra_extension_mapping.list_mappings()

    def create_mapping(self, user_id, tenant_uuid, intra_extension_uuid):
        if self.super_extension.admin(user_id, "mapping", "create") == "OK":
            return self.tenant_intra_extension_mapping.create_mapping(tenant_uuid, intra_extension_uuid)

    def destroy_mapping(self, user_id, tenant_uuid, intra_extension_uuid):
        if self.super_extension.admin(user_id, "mapping", "destroy") == "OK":
            return self.tenant_intra_extension_mapping.destroy_mapping(tenant_uuid, intra_extension_uuid)

    def delegate_privilege(self, user_id, delegator_id, genre, privilege):
        if self.super_extension.admin(user_id, genre, "delegate") == "OK":
            return self.super_extension.delegate(delegator_id, genre, privilege)


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
        #TODO: sync with PIP
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subjects", "read") == "OK":
                k_subjects = get_pip().get_subjects()
                for sbj in k_subjects:
                    if sbj["uuid"] not in self.intra_extensions[extension_uuid].intra_extension_authz.get_subjects():
                        #Can abort because the user (user_uuid) may not have the rights to do that
                        if self.intra_extensions[extension_uuid].admin(user_uuid, "subjects", "write") == "OK":
                            self.intra_extensions[extension_uuid].intra_extension_authz.add_subject(sbj["uuid"])
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_subjects()

    def add_subject(self, extension_uuid, user_uuid, subject):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subjects", "write") == "OK":
                subject_id = get_pip().add_subject(subject)
                self.intra_extensions[extension_uuid].intra_extension_authz.add_subject(subject_id)
                return subject_id

    def del_subject(self, extension_uuid, user_uuid, subject_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subjects", "write") == "OK":
                get_pip().del_subject(subject_id)
                self.intra_extensions[extension_uuid].intra_extension_authz.del_subject(subject_id)
                #TODO need to check if the subject is not in other tables like assignment

    def get_objects(self, extension_uuid, user_uuid):
        #TODO: sync with PIP
        if extension_uuid in self.intra_extensions.values():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "objects", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_objects()

    def add_object(self, extension_uuid, user_uuid, object_id):
        #TODO: add VM in Nova with PIP and sync afterwards
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "objects", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.add_object(object_id)

    def del_object(self, extension_uuid, user_uuid, object_id):
        #TODO: del VM in Nova with PIP and sync afterwards
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "objects", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.del_object(object_id)
                #TODO need to check if the subject is not in other tables like assignment

    def get_subject_categories(self, extension_uuid, user_uuid):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_categories", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_subject_categories()

    def add_subject_category(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_categories", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.add_subject_category(category_id)

    def del_subject_category(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_categories", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.del_subject_category(category_id)

    def get_object_categories(self, extension_uuid, user_uuid):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_categories", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_object_categories()

    def add_object_category(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_categories", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.add_object_category(category_id)

    def del_object_category(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_categories", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.del_object_category(category_id)

    def get_subject_category_values(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_category_values", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_subject_category_values(category_id)

    def add_subject_category_value(self, extension_uuid, user_uuid, category_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_category_values", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.add_subject_category_value(category_id, category_value)

    def del_subject_category_value(self, extension_uuid, user_uuid, category_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_category_values", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.del_subject_category_value(category_id, category_value)
                #TODO need to check if the value is not in other tables like assignment

    def get_object_category_values(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_category_values", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_object_category_values(category_id)

    def add_object_category_value(self, extension_uuid, user_uuid, category_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_category_values", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.add_object_category_value(category_id, category_value)

    def del_object_category_value(self, extension_uuid, user_uuid, category_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_category_values", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.del_object_category_value(category_id, category_value)
                #TODO need to check if the value is not in other tables like assignment

    def get_subject_assignments(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_category_assignments", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_subject_assignments(category_id)

    def add_subject_assignment(self, extension_uuid, user_uuid, category_id, subject_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_category_assignments", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.add_subject_assignment(
                    category_id, subject_id, category_value
                )

    def del_subject_assignment(self, extension_uuid, user_uuid, category_id, subject_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_category_assignments", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.del_subject_assignment(
                    category_id, subject_id, category_value
                )

    def get_object_assignments(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_category_assignments", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_object_assignments(category_id)

    def add_object_assignment(self, extension_uuid, user_uuid, category_id, object_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_category_assignments", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.add_object_assignment(
                    category_id, object_id, category_value
                )

    def del_object_assignment(self, extension_uuid, user_uuid, category_id, object_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_category_assignments", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.del_object_assignment(
                    category_id, object_id, category_value
                )

    def get_rules(self, extension_uuid, user_uuid):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "rules", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_rules()

    def add_rule(self, extension_uuid, user_uuid, sub_cat_value, obj_cat_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "rules", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.add_rule(sub_cat_value, obj_cat_value)

    def del_rule(self, extension_uuid, user_uuid, sub_cat_value, obj_cat_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "rules", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.del_rule(sub_cat_value, obj_cat_value)

    ########################################
    # Specific functions for Intra-Extension
    ########################################

    def add_from_json(self, json_directory):
        return get_intra_extensions().install_intra_extension_from_json(json_directory)

    def add_from_db(self):
        get_intra_extensions().install_intra_extension_from_db()

    #########################################
    # Specific functions for Inter Extensions
    #########################################

    def get_installed_inter_extensions(self, extension_uuid, user_uuid):
        if extension_uuid in self.inter_extensions.get_installed_inter_extensions():
            if self.inter_extensions[extension_uuid].admin(user_uuid, "inter_extension", "read") == "OK":
                for inter_ext in self.inter_extensions.get_installed_inter_extensions().values():
                    if extension_uuid and extension_uuid == inter_ext.get_uuid():
                        yield inter_ext
                    elif not extension_uuid:
                        yield inter_ext

    def create_collaboration(
            self,
            user_uuid,
            requesting_intra_extension_uuid,
            requested_intra_extension_uuid,
            genre,
            sub_list,
            obj_list,
            act):
        if self.inter_extensions.admin(user_uuid, "collaboration", "create") == "OK":
        # if self.inter_extensions.admin(
        #         requesting_intra_extension_uuid=requesting_intra_extension_uuid,
        #         requested_intra_extension_uuid=requested_intra_extension_uuid,
        #         sub=user_uuid,
        #         obj="inter_extension",
        #         act="write") == "OK":
            return self.inter_extensions.create_collaboration(
                requesting_intra_extension_uuid=requesting_intra_extension_uuid,
                requested_intra_extension_uuid=requested_intra_extension_uuid,
                genre=genre,
                sub_list=sub_list,
                obj_list=obj_list,
                act=act
            )
        return None, None

    def destroy_collaboration(self, user_uuid, inter_extension_uuid, vent_uuid):
        if self.inter_extensions.admin(user_uuid, "collaboration", "destroy") == "OK":
        # if self.inter_extensions.admin(user_uuid, "inter_extension", "write") == "OK":
            self.inter_extensions.destroy_collaboration(
                inter_extension_uuid=inter_extension_uuid,
                vent_uuid=vent_uuid)

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
            sys_logger.info("Syncing tenant {}".format(tenant["name"]))
            logs += "Syncing {}".format(tenant["name"])
            try:
                pip.set_creds_for_tenant(tenant["name"])
            except pip.Unauthorized:
                sys_logger.warning("Cannot authenticate in tenant {}".format(tenant["name"]))
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
                sys_logger.warning("Cannot list users in tenant {}".format(tenant["name"]))
                logs += " KO (Cannot list users in tenant)\n"
                continue
        return logs

    def delete_tables(self):
        self.intra_extensions.delete_tables()
        self.inter_extensions.delete_tables()

pap = PAP()


def get_pap():
    return pap