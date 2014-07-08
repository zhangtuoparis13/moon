"""
TODO: write a documentation about driver installation
"""

from nova.openstack.common.middleware import base
from nova import wsgi
import webob.dec
import urllib2
import urllib
import re
import json
import uuid
import hashlib
from moon import settings
from nova.openstack.common import log as logging
from oslo.config import cfg
from moon import tools
from cStringIO import StringIO
# from novaclient import client as nova_client
CONF = cfg.CONF
CONF.import_opt('use_forwarded_for', 'nova.api.auth')


class NovaMoon(wsgi.Middleware):

    def __init__(self, app, conf):
        self.LOG = logging.getLogger(conf.get('log_name', __name__))
        self.conf = conf
        self.app = app
        self.password = self.conf.get("moon_server_password")
        self.moon_server_ip = self.conf.get("moon_server_ip")
        self.moon_server_port = self.conf.get("moon_server_port", 8080)
        self.LOG.info('Starting moon middleware to {}'.format(self.moon_server_ip))
        # self.LOG.info(dir(self.app))

    def __call__(self, env, start_response):
        # self.LOG.info(tools.get_action(env, self.LOG))
        # self.LOG.info(env)
        ret_action, ret_object, ret_object_type, ret_tenant_uuid = tools.get_action(env, self.LOG)
        sub_action = "*"
        # if ret_object_type == "server":
        #     #Find the true tenant for this server
        #     ncreds = get_nova_creds()
        #     ncreds["project_id"] = tenant_name
        #     self.nclient = nova_client.Client("1.1", **ncreds)

        if "action" in env["RAW_PATH_INFO"]:
            length = int(env.get('CONTENT_LENGTH', '0'))
            sub_action_object = env['wsgi.input'].read(length)
            sub_action = json.loads(sub_action_object).keys()[0]
            body = StringIO(sub_action_object)
            env['wsgi.input'] = body
        authz = tools.get_moon_authz(
            host=self.moon_server_ip,
            port=self.moon_server_port,
            subject_uuid=env["HTTP_X_USER_ID"],
            object_uuid=ret_object.replace("_", ""),
            object_type=ret_object_type,
            action=ret_action+"."+sub_action,
            subject_tenant=env["HTTP_X_TENANT_ID"],
            object_tenant=ret_tenant_uuid,
            path=env["RAW_PATH_INFO"],
            password=self.password
        )
        self.LOG.info(str(authz))
        return self.app(env, start_response)


def filter_factory(global_conf, **local_conf):
    """Returns a WSGI filter app for use with paste.deploy."""
    conf = global_conf.copy()
    conf.update(local_conf)

    def auth_filter(app):
        return NovaMoon(app, conf)
    return auth_filter

