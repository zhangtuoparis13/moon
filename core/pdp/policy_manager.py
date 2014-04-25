from moon.core.pdp.core import tenant_registry as tr
from moon.policy_repository import policy_engine


def tenant_registry(tenant_name=None, filename=None):
    """
    Register access control policy for the tenant tenant_name
    """
    # create policy plugin
    policy_plugin_pointer, attributes = policy_engine.load_policy_plugin(filename)
    # return policy plugin pointer
    tr('', tenant_name, policy_plugin_pointer, attributes)
