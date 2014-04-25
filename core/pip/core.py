"""
Policy information Point
Information gathering from the infrastructure
"""
from moon.user_repository import driver_dispatcher as dd
from moon import settings
import logging

logger = logging.getLogger("moon.pip")


def get_user_attributes(
        user_uuid=None,
        tenant_uuid=None,
        attribute_name=None):
    """
    Get a list of attribute values for user user_uuid in tenant tenant_uuid
    Return a list of attribute values for attribute_name
    Example for 'role': ( "admin", "user" )

    """
    result = ()
    user = dd.get_user(uuid=user_uuid)
    return result