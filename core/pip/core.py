"""
Policy information Point
Information gathering from the infrastructure
"""
from moon.info_repository import driver_dispatcher as dd
# from moon import settings
import logging

logger = logging.getLogger("moon.pip")


def update_request_attributes(
        subject=None,
        action=None,
        object_name=None,
        tenant=None,
        attributes=None):
    """
    Get a list of attribute values for user user_uuid in tenant tenant_uuid
    Return a list of attribute values for attribute_name
    Example for 'role': ( "admin", "user" )

    """
    attributes = dd.update_request_attributes(subject, action, object_name, tenant, attributes)
    return attributes