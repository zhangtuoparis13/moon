"""
Policy Decision Point
"""
import pdp_i


def authz(user, project):
    """
    Inter-tenant access control validation
    """
    if user in project:
        # check pdp_i
        pass
    else:
        # check tenant_tree
        # check pdp_i tenant1
        # check pdp_i tenant2
        pass


def get_pdp(name=None):
    pdp_i.get_pdp(name)

