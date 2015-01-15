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

from nova import wsgi
import json
from nova.openstack.common import log as logging
from oslo.config import cfg
from cStringIO import StringIO
#from nova.api.openstack.compute import servers
from nova import exception
from moon_pep import get_moon_client
CONF = cfg.CONF
CONF.import_opt('use_forwarded_for', 'nova.api.auth')
UNMANAGED_OBJECTS = ("", "token", )
# MANAGED_OBJECTS = ("server", "servers", )
MANAGED_OBJECTS = ("server", "servers", )

_ = str


class MoonException(exception.Forbidden):
    msg_fmt = _("User does not have authorization to do that action.")


class NovaMoon(wsgi.Middleware):

    def __init__(self, app, conf):
        super(NovaMoon, self).__init__(app)
        self.LOG = logging.getLogger(__name__)
        self.conf = conf
        self.app = app
        self.password = self.conf.get("moon_server_password")
        self.moon_server_ip = self.conf.get("moon_server_ip")
        self.moon_server_port = self.conf.get("moon_server_port", 8080)
        self.LOG.info('Starting moon middleware to {}'.format(self.moon_server_ip))
        self._moon_client = get_moon_client(
            self.moon_server_ip,
            self.moon_server_port,
            password=self.password)

    # def __call__(self, env, start_response):
    def process_request(self, request):
        # self.LOG.info(tools.get_action(env, self.LOG))
        # self.LOG.info(env)
        _action, _object, _object_type, _tenant_uuid = self._moon_client.get_action(request.environ)
        # self.LOG.warning("{} {} {} {}".format(_action, _object, _object_type, _tenant_uuid))
        # self.LOG.warning(str(request.environ))
        sub_action = "*"
        # if ret_object_type == "server":
        #     #Find the true tenant for this server
        #     ncreds = get_nova_creds()
        #     ncreds["project_id"] = tenant_name
        #     self.nclient = nova_client.Client("1.1", **ncreds)
        if "action" in request.environ["PATH_INFO"]:
            length = int(request.environ.get('CONTENT_LENGTH', '0'))
            if length > 0:
                try:
                    sub_action_object = request.environ['wsgi.input'].read(length)
                    sub_action = json.loads(sub_action_object).keys()[0]
                    body = StringIO(sub_action_object)
                    request.environ['wsgi.input'] = body
                    _action = sub_action
                except ValueError:
                    self.LOG.error("Error in decoding sub-action ({}-{})".format(_action, _object))
        self.LOG.info("{} {} {} {}".format(_action, _object, _object_type, _tenant_uuid))
        if _object_type == "server" and _object == "detail":
            _object = "servers"
        if _object_type == "servers":
            _object = "servers"
        if _object_type in MANAGED_OBJECTS:
            # self.LOG.info("{} {} {} {}".format(_action, _object, _object_type, _tenant_uuid))
            # self.LOG.info(request.environ)
            keystone_auth_context = request.environ.get("KEYSTONE_AUTH_CONTEXT", {})
            requested_tenant = self._moon_client.get_project(request.environ["PATH_INFO"])
            authz_request = {
                'service': "nova",
                'subject': request.environ.get("HTTP_X_USER_ID"),
                'object': _object,
                'object_type': _object_type,
                'action': _action,
                'requesting_tenant': keystone_auth_context.get('project_id', requested_tenant),
                'requested_tenant': requested_tenant
            }
            authz_response = self._moon_client.authz(authz_request)
            if authz_response and authz_response["authz"] == "NoExtension":
                self.LOG.info("No Extension for {}".format(_object))
            elif authz_response and ("authz" not in authz_response or authz_response["authz"] != "OK"):
                # self.LOG.error("You are not authorized to do that!")
                raise MoonException(message="You are not authorized to do that!")
        else:
            self.LOG.info("Will not get authz for "+_object_type)
        # authz = tools.get_moon_authz(
        #     host=self.moon_server_ip,
        #     port=self.moon_server_port,
        #     subject_uuid=env["HTTP_X_USER_ID"],
        #     object_uuid=ret_object.replace("_", ""),
        #     object_type=ret_object_type,
        #     action=ret_action,
        #     subject_tenant=env["HTTP_X_TENANT_ID"],
        #     object_tenant=ret_tenant_uuid,
        #     path=env["RAW_PATH_INFO"],
        #     password=self.password
        # )
        # self.LOG.info(str(authz))
        # return self.app(env, start_response)


def filter_factory(global_conf, **local_conf):
    """Returns a WSGI filter app for use with paste.deploy."""
    conf = global_conf.copy()
    conf.update(local_conf)

    def auth_filter(app):
        return NovaMoon(app, conf)
    return auth_filter

