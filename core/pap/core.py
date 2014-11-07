"""
"""
import os
import json
from moon.core.pdp import get_intra_extensions
from moon.core.pdp import get_inter_extensions
from moon.core.pdp import get_super_extension
from moon.core.pdp import get_tenant_intra_extension_mapping
from moon.core.pip import get_pip
from moon.tools.log import get_sys_logger
from moon.core.pdp import pdp_admin

sys_logger = get_sys_logger()


def translate_uuid(function):
    def wrapped(*args, **kwargs):
        if "user_id" in kwargs:
            try:
                user = get_pip().get_subjects("admin", kwargs["user_id"]).next()
                kwargs["user_id"] = user["name"]
            except StopIteration:
                pass
        else:
            try:
                user = get_pip().get_subjects("admin", args[1]).next()
                args[1] = user["name"]
            except StopIteration:
                pass
        result = function(*args, **kwargs)
        return result
    return wrapped


class PAP:

    def __init__(self):
        self.intra_extensions = get_intra_extensions()
        self.inter_extensions = get_inter_extensions()
        # self.tenants = get_inter_extensions().tenants
        self.super_extension = get_super_extension()
        self.tenant_intra_extension_mapping = get_tenant_intra_extension_mapping()
        self.policies = dict()
        self.__admin_uuid = None

    def set_policies(self, dirname):
        import glob
        for node in glob.glob(os.path.join(dirname, "*")):
            if os.path.isdir(os.path.join(node, "admin")) and \
               os.path.isdir(os.path.join(node, "admin")):
                append = False
                for json_file in ("assignment.json", "metadata.json", "configuration.json", "perimeter.json"):
                    if os.path.join(node, "admin", json_file) in glob.glob(os.path.join(node, "admin", "*")) and \
                       os.path.join(node, "authz", json_file) in glob.glob(os.path.join(node, "authz", "*")):
                        append = True
                    else:
                        append = False
                        break
                if append:
                    policy_name = os.path.basename(node.strip("/"))
                    self.policies[policy_name] = dict()
                    self.policies[policy_name]["dir"] = node
                    self.policies[policy_name]["admin"] = dict()
                    self.policies[policy_name]["authz"] = dict()
                    self.policies[policy_name]["admin"]["assignment"] = json.loads(
                        file(os.path.join(node, "admin", "assignment.json")).read())
                    self.policies[policy_name]["admin"]["metadata"] = json.loads(
                        file(os.path.join(node, "admin", "metadata.json")).read())
                    self.policies[policy_name]["admin"]["configuration"] = json.loads(
                        file(os.path.join(node, "admin", "configuration.json")).read())
                    self.policies[policy_name]["admin"]["perimeter"] = json.loads(
                        file(os.path.join(node, "admin", "perimeter.json")).read())
                    self.policies[policy_name]["authz"]["assignment"] = json.loads(
                        file(os.path.join(node, "admin", "assignment.json")).read())
                    self.policies[policy_name]["authz"]["metadata"] = json.loads(
                        file(os.path.join(node, "admin", "metadata.json")).read())
                    self.policies[policy_name]["authz"]["configuration"] = json.loads(
                        file(os.path.join(node, "admin", "configuration.json")).read())
                    self.policies[policy_name]["authz"]["perimeter"] = json.loads(
                        file(os.path.join(node, "admin", "perimeter.json")).read())

    def get_policies(self):
        return self.policies

    def set_admin_uuid(self, uuid):
        self.__admin_uuid = uuid

    ###########################################
    # Misc functions for Super-Extension
    ###########################################

    def get_tenants(self):
        pip = get_pip()
        return pip.get_tenants()

    @translate_uuid
    def get_intra_extensions(self, user_id, uuid=None):
        if self.super_extension.admin(user_id, "intra_extension", "list") == "OK":
            if not uuid:
                return self.intra_extensions.values()
            elif uuid and uuid in self.intra_extensions.keys():
                return self.intra_extensions[uuid]

    @translate_uuid
    def install_intra_extension_from_json(
            self,
            user_id,
            extension_setting_name=None,
            extension_setting_dir=None,
            name="Intra_Extension"):
        if self.super_extension.admin(user_id, "intra_extension", "create") == "OK":
            if extension_setting_name:
                extension_setting_dir = self.policies[extension_setting_name]["dir"]
            intra_ext_uuid = self.intra_extensions.install_intra_extension_from_json(extension_setting_dir, name=name)
            self.intra_extensions[intra_ext_uuid].intra_extension_admin.add_subject(self.__admin_uuid)
            self.intra_extensions[intra_ext_uuid].intra_extension_admin.add_subject_assignment(
                "role", self.__admin_uuid, "admin"
            )
            return intra_ext_uuid

    @translate_uuid
    def list_mappings(self, user_id):
        if self.super_extension.admin(user_id, "mapping", "list") == "OK":
            return self.tenant_intra_extension_mapping.list_mappings()

    @translate_uuid
    def create_mapping(self, user_id, tenant_uuid, intra_extension_uuid):
        if self.super_extension.admin(user_id, "mapping", "create") == "OK":
            return self.tenant_intra_extension_mapping.create_mapping(tenant_uuid, intra_extension_uuid)

    @translate_uuid
    def destroy_mapping(self, user_id, tenant_uuid, intra_extension_uuid):
        if self.super_extension.admin(user_id, "mapping", "destroy") == "OK":
            return self.tenant_intra_extension_mapping.destroy_mapping(tenant_uuid, intra_extension_uuid)

    @translate_uuid
    def delegate_privilege(self, user_id, delegator_id, genre, privilege):
        if self.super_extension.admin(user_id, genre, "delegate") == "OK":
            return self.super_extension.delegate(delegator_id, genre, privilege)

    @translate_uuid
    def delete_intra_extension(self, user_id, intra_extension_uuid):
        if self.super_extension.admin(user_id, "intra_extension", "destroy") == "OK":
            return self.intra_extensions.delete_intra_extension(intra_extension_uuid)

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
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subjects", "read") == "OK":
                k_subjects = get_pip().get_subjects()
                for sbj in k_subjects:
                    if sbj["uuid"] not in self.intra_extensions[extension_uuid].intra_extension_authz.get_subjects():
                        #Can abort because the user (user_uuid) may not have the rights to do that
                        if self.intra_extensions[extension_uuid].admin(user_uuid, "subjects", "write") == "OK":
                            self.intra_extensions[extension_uuid].intra_extension_authz.add_subject(sbj["uuid"])
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_subjects()
        return list()

    def add_subject(self, extension_uuid, user_uuid, subject):
        """Add a new subject (ie user)

        :param extension_uuid: intra_extension UUID
        :param user_uuid: user who request the action
        :param subject: subject to be added
        :return: subject UUID

        the subject must a dictionary:
        {
            "name": "username",
            'domain': "Default",
            'enabled': True,
            'project': "admin",
            'password': "password",
            'description': "user description"
        }
        """
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
        if extension_uuid in self.intra_extensions.values():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "objects", "read") == "OK":
                servers = get_pip().get_objects(tenant=self.intra_extensions[extension_uuid].get_tenant_uuid())
                for server in servers:
                    if server["uuid"] not in self.intra_extensions[extension_uuid].intra_extension_authz.get_objects():
                        #Can abort because the user (user_uuid) may not have the rights to do that
                        if self.intra_extensions[extension_uuid].admin(user_uuid, "objects", "write") == "OK":
                            self.intra_extensions[extension_uuid].intra_extension_authz.add_object(server["uuid"])
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_objects()
        return list()

    def add_object(self, extension_uuid, user_uuid, object):
        """Add a new virtual machine

        :param extension_uuid: intra_extension UUID
        :param user_uuid: user who request the action
        :param object: VM to be added
        :return: the VM UUID

        object must be a dictionary:
        {
            "name": "what ever you want",
            "image_name": "Cirros3.2",
            "flavor_name": "m1.tiny"
        }
        """
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "objects", "write") == "OK":
                tenant = self.intra_extensions[extension_uuid].get_tenant_uuid()
                if not tenant:
                    return
                object_id = get_pip().add_object(
                    name=object["name"],
                    image_name=object["image_name"],
                    flavor_name=object["flavor_name"],
                    tenant=tenant
                )
                if object_id:
                    self.intra_extensions[extension_uuid].intra_extension_authz.add_object(object_id)
                    return object_id

    def del_object(self, extension_uuid, user_uuid, object_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "objects", "write") == "OK":
                tenant = self.intra_extensions[extension_uuid].get_tenant_uuid()
                if not tenant:
                    return
                get_pip().del_object(object_id, tenant=tenant)
                self.intra_extensions[extension_uuid].intra_extension_authz.del_object(object_id)
                #TODO need to check if the subject is not in other tables like assignment

    def get_subject_categories(self, extension_uuid, user_uuid):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_categories", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_subject_categories()
        return list()

    def add_subject_category(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_categories", "write") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.add_subject_category(category_id)

    def del_subject_category(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_categories", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.del_subject_category(category_id)

    def get_object_categories(self, extension_uuid, user_uuid):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_categories", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_object_categories()
        return list()

    def add_object_category(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_categories", "write") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.add_object_category(category_id)

    def del_object_category(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_categories", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.del_object_category(category_id)

    def get_subject_category_values(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_category_values", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_subject_category_values(category_id)
        return list()

    def add_subject_category_value(self, extension_uuid, user_uuid, category_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_category_values", "write") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.add_subject_category_value(
                    category_id,
                    category_value)

    def del_subject_category_value(self, extension_uuid, user_uuid, category_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_category_values", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.del_subject_category_value(category_id, category_value)
                #TODO need to check if the value is not in other tables like assignment

    def get_object_category_values(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_category_values", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_object_category_values(category_id)
        return list()

    def add_object_category_value(self, extension_uuid, user_uuid, category_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_category_values", "write") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.add_object_category_value(
                    category_id,
                    category_value)

    def del_object_category_value(self, extension_uuid, user_uuid, category_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_category_values", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.del_object_category_value(category_id, category_value)
                #TODO need to check if the value is not in other tables like assignment

    def get_subject_assignments(self, extension_uuid, user_uuid, category_id):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_category_assignments", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_subject_assignments(category_id)
        return list()

    def add_subject_assignment(self, extension_uuid, user_uuid, category_id, subject_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "subject_category_assignments", "write") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.add_subject_assignment(
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
        return list()

    def add_object_assignment(self, extension_uuid, user_uuid, category_id, object_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_category_assignments", "write") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.add_object_assignment(
                    category_id, object_id, category_value
                )

    def del_object_assignment(self, extension_uuid, user_uuid, category_id, object_id, category_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "object_category_assignments", "write") == "OK":
                self.intra_extensions[extension_uuid].intra_extension_authz.del_object_assignment(
                    category_id, object_id, category_value
                )

    def get_meta_rules(self, extension_uuid, user_uuid):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "rules", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_meta_rules()
        return dict()

    def get_rules(self, extension_uuid, user_uuid):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "rules", "read") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.get_rules(full=True)
        return dict()

    def add_rule(self, extension_uuid, user_uuid, sub_cat_value, obj_cat_value):
        if extension_uuid in self.intra_extensions.keys():
            if self.intra_extensions[extension_uuid].admin(user_uuid, "rules", "write") == "OK":
                return self.intra_extensions[extension_uuid].intra_extension_authz.add_rule(
                    sub_cat_value,
                    obj_cat_value)

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

    @translate_uuid
    def get_installed_inter_extensions(self, user_id, extension_uuid):
        if self.super_extension.admin(user_id, "inter_extension", "list") == "OK":
            for inter_ext in self.inter_extensions.get_installed_inter_extensions().values():
                if extension_uuid and extension_uuid == inter_ext.get_uuid():
                    yield inter_ext
                elif not extension_uuid:
                    yield inter_ext

    @translate_uuid
    def create_collaboration(
            self,
            user_id,
            requesting_intra_extension_uuid,
            requested_intra_extension_uuid,
            genre,
            sub_list,
            obj_list,
            act):
        #TODO use pdp_admin
        if self.super_extension.admin(
                user_id,
                "inter_extension",
                "create") == "OK":
            result = self.inter_extensions.create_collaboration(
                requesting_intra_extension_uuid=requesting_intra_extension_uuid,
                requested_intra_extension_uuid=requested_intra_extension_uuid,
                genre=genre,
                sub_list=sub_list,
                obj_list=obj_list,
                act=act
            )
            return result
        return None, None

    @translate_uuid
    def destroy_collaboration(self, user_id, inter_extension_uuid, vent_uuid, genre):
        if self.super_extension.admin(user_id, "inter_extension", "destroy") == "OK":
            self.inter_extensions.destroy_collaboration(
                genre=genre,
                inter_extension_uuid=inter_extension_uuid,
                vent_uuid=vent_uuid)

    ###########################################
    # Misc functions for Intra/Inter-Extensions
    ###########################################

    def delete_tables(self):
        self.intra_extensions.delete_tables()
        self.inter_extensions.delete_tables()

pap = PAP()


def get_pap():
    return pap