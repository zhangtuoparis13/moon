import uuid
import hashlib
import urllib
import urllib2
import logging
import json
import re

logger = logging.getLogger(__name__)

API = json.loads(file("/etc/moon/api.json").read())
API_dict = {}
for attr in API["attributes"]:
    if "server_id" in attr:
        API_dict[attr] = "(\w+)"
    elif "id" in attr:
        API_dict[attr] = "(\w){32}"
    else:
        API_dict[attr] = "(\w+)"


def get_moon_authz(
        host,
        port=8080,
        baseurl="mrm",
        subject_uuid="",
        object_uuid="",
        object_type="",
        action="",
        subject_tenant="",
        object_tenant="",
        path="",
        password=""
):
    """ Send a authorization request to the Moon service.

    :param host:
    :param port:
    :param baseurl:
    :param subject_uuid:
    :param object_uuid:
    :param object_type:
    :param action:
    :param subject_tenant:
    :param object_tenant:
    :param path:
    :param password:
    :return:
    """
    url = "http://{host}:{port}/{baseurl}/tenants".format(host=host, port=port, baseurl=baseurl)
    key = uuid.uuid4()
    crypt_key = hashlib.sha256()
    crypt_key.update(str(key))
    crypt_key.update(password)
    post_data = [
        ('Object', object_uuid),
        ('ObjectType', object_type),
        ('Subject', subject_uuid),
        ('Action', action),
        ('Subject_Tenant', subject_tenant),
        ('Object_Tenant', object_tenant),
        ('RAW_PATH_INFO', path),
        ('key', key)]
    # logger.info(url)
    try:
        # TODO: the connection must be secured!
        result = urllib2.urlopen(url, urllib.urlencode(post_data))
        content = json.loads(result.read())
        if "key" not in content or content["key"] != crypt_key.hexdigest():
            return {"auth": False, "message": "Connection problem with Moon authorisation framework"}
        # TODO: in production must raise an error if authz is false
        return content
    except urllib2.URLError as e:
        # TODO: in production must raise an error and don't allow connection
        logger.warning(e.message)
        logger.warning(e)


def get_action(env_req, logger=None):
    ret_action = ""
    ret_object = ""
    ret_object_type = ""
    ret_tenant_uuid = ""
    method = env_req['REQUEST_METHOD']
    logger.warning(env_req['RAW_PATH_INFO'])
    try:
        ret_tenant_uuid = env_req['RAW_PATH_INFO'].split("/")[2]
    except IndexError:
        pass
    url = env_req['RAW_PATH_INFO'].replace("-", "_")
    for action in API["data"]:
        if action['method'] == method and \
            re.match(action['name'].format(**API_dict), url):
            ret_action = action['action']
            ret_object_type = action['object']
            ret_object = url.split("/")[-1]
            if ret_object in ("action", ):
                # BAD
                ret_object = url.split("/")[-2]
                ret_object_type = "server"
            if len(ret_object_type) == 0:
                continue
            return ret_action, ret_object, ret_object_type, ret_tenant_uuid
    return ret_action, ret_object, ret_object_type, ret_tenant_uuid