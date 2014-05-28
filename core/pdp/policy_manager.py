# from moon.core.pdp.core import tenant_registry as tr
from moon.policy_repository import policy_engine
from moon.tenant_repository.driver_dispatcher import Tenants
from moon.core.pdp import PDP
from moon import settings
from moon.core.pap.core import PAP
import json
import logging
import re

logger = logging.getLogger(__name__)


class Manager:

    def __init__(self):
        self.tenants = Tenants(kclient=None)
        # pdps: list of tenant name and corresponding pdp_i
        # example:
        #   {
        #       'tenant1': pdp1,
        #       'tenant2': pdp2,
        #   }
        self.pdps = {}
        self.init_pdps()

    def init_pdps(self):
        filename = getattr(settings, "POLICY_PLUGIN_TABLE")
        try:
            tables = json.loads(open(filename).read())
        except IOError:
            raise Exception("[{}] Unable to read file {}".format(__name__, filename))
        for key in tables.keys():
            self.register_tenant(key, tables[key])

    # def tenant_registry(self, tenant_uuid, tenant_name, policy_plugin_pointer, attributes):
    #     pdp_i = PDP(tenant_uuid, tenant_name, policy_plugin_pointer, attributes)
    #     self.pdps[tenant_name] = pdp_i

    def is_child(self, tenant_parent=None, tenant_child=None):
        """Return True if tenant_child is a child of tenant_parent.
        """
        for children_uuid in tenant_parent.children:
            if tenant_child.uuid == children_uuid:
                return True
            tenant = self.tenants.get_tenant(uuid=children_uuid)
            return self.is_child(tenant_parent=tenant_child, tenant_child=tenant)
        return False

    def register_tenant(self, tenant_name=None, filename=None):
        """
        Register access control policy for the tenant tenant_name
        """
        # create policy plugin
        policy_plugin_pointer, attributes = policy_engine.load_policy_plugin(filename)
        # return policy plugin pointer
        pdp_i = PDP('', tenant_name, policy_plugin_pointer, attributes)
        self.pdps[tenant_name] = pdp_i

    def __check_policy(self, subject, action, object_name, tenant_name=""):
        auth = False
        tenant_name = tenant_name.replace("*", ".*")
        policy_found = False
        for key in self.pdps.keys():
            if re.match(key, tenant_name):
                auth = self.pdps[key].authz(subject, action, object_name)
                policy_found = True
                break
        if not policy_found:
            logger.warning("No policy found for tenant {}".format(tenant_name))
        return auth

    def authz(self,
            subject=None,
            action=None,
            object_name=None,
            subject_tenant=None,
            object_tenant=None):
        """
        Intra/Inter-tenant access control validation
        Parameters:
            subject: user who ask for resources
            action:  manipulation on resources
            object_name:  resources name
            subject_tenant: tenant name of the subject
            object_tenant: tenant name of the resources
        Return: boolean
        """
        tenant_name = "None"
        auth = False
        object_tenant = self.tenants.get_tenant(uuid=object_tenant)
        object_tenant_name = "Unknown"
        if not subject_tenant or subject_tenant == "None":
            if subject:
                pap = PAP(kclient=None)
                user = pap.users.get_user(uuid=subject)
                if user:
                    subject_tenant = self.tenants.get_tenant(uuid=user.project)
                    if not subject_tenant:
                        subject_tenant = self.tenants.get_tenant(name=user.project)
        if not object_tenant:
            object_tenant = self.tenants.get_tenant(name=object_tenant)
        try:
            object_tenant_name = object_tenant.name
        except AttributeError:
            pass
        subject_tenant_name = "Unknown"
        subject_tenant = self.tenants.get_tenant(uuid=subject_tenant)
        if not subject_tenant:
            subject_tenant = self.tenants.get_tenant(name=subject_tenant)
        try:
            subject_tenant_name = subject_tenant.name
        except AttributeError:
            pass
        if not subject_tenant or subject_tenant == "None":
            # subject_tenant is None when for example action is "get" and object is "token" ie authentication
            auth = self.pdps["None"].authz(subject, action, object_name)
        elif subject_tenant == object_tenant:
            # intra tenant access control
            # check pdp_i
            auth = self.__check_policy(subject, action, object_name, subject_tenant_name)
            tenant_name = subject_tenant_name
        else:
            # inter tenant access control
            # check tenant_tree
            child = False
            child = self.is_child(tenant_parent=subject_tenant, tenant_child=object_tenant)
            # check pdp_i tenant1
            auth_subject = self.__check_policy(subject, action, object_name, subject_tenant_name)
            # check pdp_i tenant2
            auth_object = self.__check_policy(subject, action, object_name, object_tenant_name)
            if child:
                auth = auth_subject or auth_object
                tenant_name = subject_tenant_name + "->" + object_tenant_name
            else:
                auth = auth_object
                tenant_name = object_tenant_name
        return auth, tenant_name




# def tenant_registry(tenant_name=None, filename=None):
#     """
#     Register access control policy for the tenant tenant_name
#     """
#     # create policy plugin
#     policy_plugin_pointer, attributes = policy_engine.load_policy_plugin(filename)
#     # return policy plugin pointer
#     tr('', tenant_name, policy_plugin_pointer, attributes)
