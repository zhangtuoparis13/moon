"""
TODO: write a documentation about driver installation
"""

from keystone.common import wsgi
from keystone import identity
from keystone.openstack.common import log as logging
# from keystone import config
# from keystone.common import extension
from keystone.common import dependency
import urllib2
import urllib
import re
import json

logger = logging.getLogger(__name__)

# TODO: set a configuration file
MOON_SERVER_IP = {
    "HOST": "192.168.119.166",
    "PORT": "8080",
    "BASEURL": "mrm"
}

API = json.loads(file("/etc/moon/api.json").read())
API_dict = {}
for attr in  API["attributes"]:
    if "id" in attr:
        API_dict[attr] = "(\w){32}"
    else:
        API_dict[attr] = "(\w+)"

# actions = (
#     {'url': '/tokens', 'action': 'authenticate', 'object': 'tokens', 'method': 'POST'},
#     {'url': '/tokens/revoked', 'action': 'revocation_list', 'object': 'tokens', 'method': 'GET'},
#     {'url': '/tokens/{token_id}', 'action': 'validate_token', 'object': 'token', 'method': 'GET'},
#     {'url': '/tokens/{token_id}', 'action': 'validate_token_head', 'object': 'token', 'method': 'HEAD'},
#     {'url': '/tokens/{token_id}', 'action': 'delete_token', 'object': 'token', 'method': 'DELETE'},
#     {'url': '/tokens/{token_id}/endpoints', 'action': 'endpoints', 'object': 'endpoints', 'method': 'GET'},
#     {'url': '/certificates/ca', 'action': 'ca_cert', 'object': '', 'method': 'GET'},
#     {'url': '/certificates/signing', 'action': 'signing_cert', 'object': 'certificates', 'method': 'GET'},
#     {'url': '/extensions', 'action': 'get_extensions_info', 'object': 'certificates', 'method': 'GET'},
#     {'url': '/extensions/{extension_alias}', 'action': 'get_extension_info', 'object': 'extension', 'method': 'GET'},
#     {'url': '/auth/tokens', 'action': 'authenticate_for_token', 'object': 'token', 'method': 'POST'},
#     {'url': '/auth/tokens', 'action': 'check_token', 'object': 'token', 'method': 'HEAD'},
#     {'url': '/auth/tokens', 'action': 'revoke_token', 'object': 'token', 'method': 'DELETE'},
#     {'url': '/auth/tokens', 'action': 'validate_token', 'object': 'token', 'method': 'GET'},
#     {'url': '/auth/tokens/OS-PKI/revoked', 'action': 'revocation_list', 'object': 'revocation_list', 'method': 'GET'},
#     {'url': '/tenants', 'action': 'get_projects_for_token', 'object': 'tenants', 'method': 'GET'},
#     {'url': '/tenants', 'action': 'get_all_projects', 'object': 'tenants', 'method': 'GET'},
#     {'url': '/tenants/{tenant_id}', 'action': 'get_project', 'object': 'tenant', 'method': 'GET'},
#     {'url': '/tenants/{tenant_id}/users/{user_id}/roles', 'action': 'get_user_roles', 'object': 'roles', 'method': 'GET'},
#     {'url': '/users/{user_id}/roles', 'action': 'get_user_roles', 'object': 'roles', 'method': 'GET'},
#     {'url': '/users/{user_id}/projects', 'action': 'list_user_projects', 'object': 'tenants', 'method': 'GET'},
#     {'url': '/projects/{project_id}/users/{user_id}/roles/{role_id}', 'action': 'create_grant', 'object': 'role', 'method': 'PUT'},
#     {'url': '/projects/{project_id}/groups/{group_id}/roles/{role_id}', 'action': 'create_grant', 'object': 'role', 'method': 'PUT'},
#     {'url': '/projects/{project_id}/users/{user_id}/roles/{role_id}', 'action': 'check_grant', 'object': 'role', 'method': 'HEAD'},
#     {'url': '/projects/{project_id}/groups/{group_id}/roles/{role_id}', 'action': 'check_grant', 'object': 'role', 'method': 'HEAD'},
#     {'url': '/projects/{project_id}/users/{user_id}/roles', 'action': 'list_grants', 'object': 'roles', 'method': 'GET'},
#     {'url': '/projects/{project_id}/groups/{group_id}/roles', 'action': 'list_grants', 'object': 'roles', 'method': 'GET'},
#     {'url': '/projects/{project_id}/users/{user_id}/roles/{role_id}', 'action': 'revoke_grant', 'object': 'role', 'method': 'DELETE'},
#     {'url': '/projects/{project_id}/groups/{group_id}/roles/{role_id}', 'action': 'revoke_grant', 'object': 'role', 'method': 'DELETE'},
#     {'url': '/domains/{domain_id}/users/{user_id}/roles/{role_id}', 'action': 'create_grant', 'object': 'role', 'method': 'PUT'},
#     {'url': '/domains/{domain_id}/groups/{group_id}/roles/{role_id}', 'action': 'create_grant', 'object': 'role', 'method': 'PUT'},
#     {'url': '/domains/{domain_id}/users/{user_id}/roles/{role_id}', 'action': 'check_grant', 'object': 'role', 'method': 'HEAD'},
#     {'url': '/domains/{domain_id}/groups/{group_id}/roles/{role_id}', 'action': 'check_grant', 'object': 'role', 'method': 'HEAD'},
#     {'url': '/domains/{domain_id}/users/{user_id}/roles', 'action': 'list_grants', 'object': 'roles', 'method': 'GET'},
#     {'url': '/domains/{domain_id}/groups/{group_id}/roles', 'action': 'list_grants', 'object': 'roles', 'method': 'GET'},
#     {'url': '/domains/{domain_id}/users/{user_id}/roles/{role_id}', 'action': 'revoke_grant', 'object': 'role', 'method': 'DELETE'},
#     {'url': '/domains/{domain_id}/groups/{group_id}/roles/{role_id}', 'action': 'revoke_grant', 'object': 'role', 'method': 'DELETE'},
#     {'url': '/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects', 'action': 'create_grant', 'object': 'role', 'method': 'PUT'},
#     {'url': '/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects', 'action': 'create_grant', 'object': 'role', 'method': 'PUT'},
#     {'url': '/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects', 'action': 'check_grant', 'object': 'role', 'method': 'HEAD'},
#     {'url': '/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects', 'action': 'check_grant', 'object': 'role', 'method': 'HEAD'},
#     {'url': '/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/inherited_to_projects', 'action': 'list_grants', 'object': 'role', 'method': 'GET'},
#     {'url': '/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/inherited_to_projects', 'action': 'list_grants', 'object': 'role', 'method': 'GET'},
#     {'url': '/OS-INHERIT/domains/{domain_id}/users/{user_id}/roles/{role_id}/inherited_to_projects', 'action': 'revoke_grant', 'object': 'role', 'method': 'DELETE'},
#     {'url': '/OS-INHERIT/domains/{domain_id}/groups/{group_id}/roles/{role_id}/inherited_to_projects', 'action': 'revoke_grant', 'object': 'role', 'method': 'DELETE'},
#     {'url': '/users/{user_id}/password', 'action': 'change_password', 'object': 'password', 'method': 'POST'},
#     {'url': '/users', 'action': 'list', 'object': 'users', 'method': 'GET'},
#     {'url': '/groups/{group_id}/users', 'action': 'list_users_in_group', 'object': 'users', 'method': 'GET'},
#     {'url': '/groups/{group_id}/users/{user_id}', 'action': 'add_user_to_group', 'object': 'user', 'method': 'PUT'},
#     {'url': '/groups/{group_id}/users/{user_id}', 'action': 'check_user_in_group', 'object': 'user', 'method': 'HEAD'},
#     {'url': '/groups/{group_id}/users/{user_id}', 'action': 'remove_user_from_group', 'object': 'user', 'method': 'DELETE'},
#     {'url': '/users/{user_id}/groups', 'action': 'list_groups_for_user', 'object': 'groups', 'method': 'GET'},
#     {'url': '/users/{user_id}', 'action': "get_user", 'object': 'user', 'method': "GET"},
#     {'url': '/OS-KSADM/roles', 'action': 'os-ksadm', 'object': 'roles', 'method': 'GET'},
# )


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
    method = env_req['REQUEST_METHOD']
    url = env_req['RAW_PATH_INFO'].replace("-", "_")
    for action in API["data"]:
        if action['method'] == method and \
            re.match(action['name'].format(**API_dict), url):
            ret_action = action['action']
            ret_object = action['object']
    return ret_action, ret_object


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
            logger.warning(request.environ['RAW_PATH_INFO'])
        post_data = [
            ('Object', action[1]),
            ('Subject', u),
            ('Action', action[0]),
            ('Subject_Tenant', KEYSTONE_AUTH_CONTEXT.get('project_id')),
            ('Object_Tenant', self.__get_project(request.environ["PATH_INFO"])),
            ('RAW_PATH_INFO', request.environ["RAW_PATH_INFO"].replace("-", "_"))]
        # TODO: connection is too long when the server is down
        #       especially when we create the DB for the first time
        try:
            result = urllib2.urlopen(url, urllib.urlencode(post_data))
            content = result.read()
            logger.info(str(content))
        except urllib2.URLError as e:
            logger.warning(e.message)
            logger.warning(e)

    def __get_project(self, path):
        try:
            if "/tenants" in path or "/projects" in path:
                return path.split('/')[2]
        except IndexError:
            return