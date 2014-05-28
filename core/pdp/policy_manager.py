# from moon.core.pdp.core import tenant_registry as tr
from moon.policy_repository import policy_engine
from moon.tenant_repository.driver_dispatcher import Tenants
from moon.core.pdp import PDP
from moon import settings
import json
import logging

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

    def register_tenant(self, tenant_name=None, filename=None):
        """
        Register access control policy for the tenant tenant_name
        """
        # create policy plugin
        policy_plugin_pointer, attributes = policy_engine.load_policy_plugin(filename)
        # return policy plugin pointer
        pdp_i = PDP('', tenant_name, policy_plugin_pointer, attributes)
        self.pdps[tenant_name] = pdp_i

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
        auth = False
        if not subject_tenant or subject_tenant == "None":
            # subject_tenant is None when for example action is "token"
            auth = self.pdps["None"].authz(subject, action, object_name)
        elif subject_tenant == object_tenant:
            # intra tenant access control
            # check pdp_i
            auth = self.pdps[subject_tenant].authz(subject, action, object_name)
        else:
            # inter tenant access control
            # check tenant_tree
            # check pdp_i tenant1
            # check pdp_i tenant2
            logger.warning("Inter-tenant access control validation not developed ! (s:{}/o:{})".format(
                subject_tenant,
                object_tenant
            ))
            pass
        return auth




# def tenant_registry(tenant_name=None, filename=None):
#     """
#     Register access control policy for the tenant tenant_name
#     """
#     # create policy plugin
#     policy_plugin_pointer, attributes = policy_engine.load_policy_plugin(filename)
#     # return policy plugin pointer
#     tr('', tenant_name, policy_plugin_pointer, attributes)
