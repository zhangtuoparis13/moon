"""
TODO: write a documentation about driver installation
"""

from keystone.common import wsgi
from keystone import identity
from keystone.openstack.common import log as logging
from keystone import config
from keystone.common import extension
from keystone.common import dependency
import urllib2
import urllib

logger = logging.getLogger(__name__)

MOON_SERVER_IP = {
    "HOST": "192.168.119.154",
    "PORT": "8080",
    "BASEURL": "mrm"
}


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
        post_data = [('object', request.environ["PATH_INFO"]),
                     ('user', u)]
        try:
            result = urllib2.urlopen(url, urllib.urlencode(post_data))
            content = result.read()
            logger.info(str(content))
        except Exception as e:
            logger.warning(e.message)
            logger.warning(e)
