# Copyright 2014 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from keystone.common import wsgi
from keystone import identity
from keystone import exception
from keystone.common import dependency
from moon_pep import get_moon_client
from keystone.models import token_model
import logging

UNMANAGED_OBJECTS = ("", "tokens", "token", "container", )
MANAGED_OBJECTS = list()

logger = logging.getLogger(__name__)


class UserController(identity.controllers.UserV3):
    #[u'tenantId', u'enabled', u'id', u'name', u'email']

    def get_user_id(self, context):
        user_id_from_token = None
        token_id = context.get('token_id')
        if token_id:
            response = self.token_provider_api.validate_token(token_id)
            token_ref = token_model.KeystoneToken(token_id=token_id, token_data=response)
            user_id_from_token = token_ref['user']['id']
        return user_id_from_token

    def get_user_name(self, context):
        user_id_from_token = None
        token_id = context.get('token_id')
        if token_id:
            response = self.token_provider_api.validate_token(token_id)
            token_ref = token_model.KeystoneToken(token_id=token_id, token_data=response)
            user_id_from_token = token_ref['user']['name']
        return user_id_from_token

    def get_user_project(self, context):
        user_tenant_from_token = None
        token_id = context.get('token_id')
        if token_id:
            response = self.token_provider_api.validate_token(token_id)
            token_ref = token_model.KeystoneToken(token_id=token_id, token_data=response)
            user_tenant_from_token = token_ref['user']['tenantId']
        return user_tenant_from_token


@dependency.requires('assignment_api', 'identity_api')
class KeystoneMoon(wsgi.Middleware):

    def __init__(self, app, conf):
        super(KeystoneMoon, self).__init__(app)
        self.conf = conf
        _moon_server_ip = self.conf.get("moon_server_ip")
        _moon_server_port = self.conf.get("moon_server_port", 8080)
        self._moon_server_password = self.conf.get("moon_server_password")
        self._moon_client = get_moon_client(_moon_server_ip, _moon_server_port)
        self._moon_client.set_server(_moon_server_ip, _moon_server_port,
                                     password=self._moon_server_password)

    def process_request(self, request):
        """
        authz_response2 = {
            'authz': "OK"/"KO",
            'message': "xxooxxoo"
        }
        """
        wsgi_context = request.environ.get(wsgi.CONTEXT_ENV, {})
        keystone_auth_context = request.environ.get("KEYSTONE_AUTH_CONTEXT", {})
        user_controller = UserController()
        _user_id = user_controller.get_user_id(wsgi_context)
        _action, _object, _object_type, _tenant_uuid = self._moon_client.get_action(request.environ)

        if _object_type in MANAGED_OBJECTS:
            authz_request = {
                'service': "keystone",
                'subject': _user_id,
                'object': _object,
                'object_type': _object_type,
                'action': _action,
                'requesting_tenant': keystone_auth_context.get('project_id', "NoTenant"),
                'requested_tenant': self._moon_client.get_project(request.environ["PATH_INFO"])
            }
            # logger.warning("authz_request={}".format(authz_request))
            authz_response = self._moon_client.authz(authz_request)
            # logger.warning(authz_response)
            if not authz_response or "authz" not in authz_response or authz_response["authz"] != "OK":
                raise exception.Unauthorized(message="You are not authorized to do that!")
                # logger.error("authz_response = ".format(authz_response))


def filter_factory(global_conf, **local_conf):
    """Returns a WSGI filter app for use with paste.deploy."""
    conf = global_conf.copy()
    conf.update(local_conf)

    def auth_filter(app):
        return KeystoneMoon(app, conf)
    return auth_filter