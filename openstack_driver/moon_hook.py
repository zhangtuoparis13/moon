"""
TODO: write a documentation about driver installation
"""

from keystone.common import wsgi
from keystone import identity
from keystone.openstack.common import log as logging
# from keystone import config
# from keystone.common import extension
from keystone import exception
from keystone.common import dependency
import urllib2
import urllib
import re
import json
import uuid
import hashlib

logger = logging.getLogger(__name__)

# TODO: set a configuration file
MOON_SERVER_IP = {
    "HOST": "192.168.119.166",
    "PORT": "8080",
    "BASEURL": "mrm"
}

PASSWORD = "P4ssw0rd"
IMPORT = False

API = json.loads(file("/etc/moon/api.json").read())
API_dict = {}
for attr in API["attributes"]:
    if "id" in attr:
        API_dict[attr] = "(\w){32}"
    else:
        API_dict[attr] = "(\w+)"


class UserController(identity.controllers.UserV3):
    #[u'tenantId', u'enabled', u'id', u'name', u'email']

    def get_user_id(self, context):
        user_id_from_token = None
        token_id = context.get('token_id')
        if token_id:
            token_ref = self.token_api.get_token(token_id)
            user_id_from_token = token_ref['user']['id']
        return user_id_from_token

    def get_user_name(self, context):
        user_id_from_token = None
        token_id = context.get('token_id')
        if token_id:
            token_ref = self.token_api.get_token(token_id)
            user_id_from_token = token_ref['user']['name']
        return user_id_from_token

    def get_user_project(self, context):
        user_tenant_from_token = None
        token_id = context.get('token_id')
        if token_id:
            token_ref = self.token_api.get_token(token_id)
            logger.debug("token_ref['user'].keys() = {}".format(str(token_ref['user'].keys())))
            user_tenant_from_token = token_ref['user']['tenantId']
        return user_tenant_from_token


def get_action(env_req):
    ret_action = ""
    ret_object = ""
    ret_object_type = ""
    method = env_req['REQUEST_METHOD']
    url = env_req['RAW_PATH_INFO'].replace("-", "_")
    for action in API["data"]:
        if action['method'] == method and \
            re.match(action['name'].format(**API_dict), url):
            ret_action = action['action']
            ret_object_type = action['object']
            ret_object = url.split("/")[-1]
            if len(ret_object) != 32:
                ret_object = ""
    return ret_action, ret_object, ret_object_type


@dependency.requires('assignment_api', 'identity_api')
class Moon(wsgi.Middleware):

    def process_request(self, request):
        AUTH_TOKEN_HEADER = 'X-Auth-Token'
        CONTEXT_ENV = wsgi.CONTEXT_ENV
        # token = request.headers.get(AUTH_TOKEN_HEADER)
        context = request.environ.get(CONTEXT_ENV, {})
        KEYSTONE_AUTH_CONTEXT = request.environ.get("KEYSTONE_AUTH_CONTEXT", {})
        #  example: 'project_id': u'2310b664a9ee430ea69d70c5e7c9662a',
        #           'user_id': u'9d325471d9bc4144bfb9206873d61c74',
        #           'roles': [u'admin']
        user = UserController()
        u = user.get_user_id(context)
        url = "http://{HOST}:{PORT}/{BASEURL}/tenants".format(**MOON_SERVER_IP)
        action = get_action(request.environ)
        if len(action[0]) == 0:
            logger.warning("Action not found! " + str(request.environ))
        key = uuid.uuid4()
        crypt_key = hashlib.sha256()
        crypt_key.update(str(key))
        crypt_key.update(PASSWORD)
        post_data = [
            ('Object', action[1]),
            ('ObjectType', action[2]),
            ('Subject', u),
            ('Action', action[0]),
            ('Subject_Tenant', KEYSTONE_AUTH_CONTEXT.get('project_id')),
            ('Object_Tenant', self.__get_project(request.environ["PATH_INFO"])),
            ('RAW_PATH_INFO', request.environ["RAW_PATH_INFO"].replace("-", "_")),
            ('key', key)]
        # TODO: connection is too long when the server is down
        #       especially when we create the DB for the first time
        if not IMPORT:
            try:
                # TODO: the connection must be secured!
                result = urllib2.urlopen(url, urllib.urlencode(post_data))
                content = json.loads(result.read())
                if "key" not in content or content["key"] != crypt_key.hexdigest():
                    raise exception.Unauthorized(message="Connection problem with Moon authorisation framework")
                # TODO: in production must raise an error if authz is false
                if "auth" not in content or content["auth"] != True:
                    logger.error("You are not authorized to do that!")
                    # raise exception.Unauthorized(message="You are not authorized to do that!")
            except urllib2.URLError as e:
                # TODO: in production must raise an error and don't allow connection
                logger.warning(e.message)
                logger.warning(e)
        else:
            logger.warning("Moon is disabled by configuration.")

    def __get_project(self, path):
        try:
            if "/tenants" in path or "/projects" in path:
                return path.split('/')[2]
        except IndexError:
            return