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
"""
TODO: put the following code to the main file

CONF = config.CONF
config.configure()
CONF(default_config_files=['/../../moon.conf'])
"""


from oslo.config import cfg
from oslo import messaging


FILE_OPTIONS = {
    None: [
        cfg.IntOpt('admin_workers', default=1,
                   help='help xxx'),
        cfg.IntOpt('max_token_size', default=16384,
                   help='help xxx'),
        cfg.StrOpt('logging_exception_prefix', default='%(process)d TRACE %(name)s %(instance)s',
                   help='logging_exception_prefix'),
        cfg.StrOpt('logging_debug_format_suffix', default='%(funcName)s %(pathname)s:%(lineno)d',
                   help='logging_exception_prefix'),
        cfg.StrOpt('logging_default_format_string',
                   default='%(process)d %(levelname)s %(name)s [-] %(instance)s%(message)s',
                   help='logging_exception_prefix'),
        cfg.StrOpt('logging_context_format_string',
                   default='%(process)d %(levelname)s %(name)s [%(request_id)s %(user_identity)s] %(instance)s%(message)s',
                   help='logging_exception_prefix'),
        cfg.BoolOpt('debug', default=True,
                    help='debug'),
        cfg.StrOpt('admin_token', default='password',
                   help='admin_token'),
        cfg.StrOpt('admin_bind_host', default='0.0.0.0',
                   help='admin_bind_host'),
        cfg.StrOpt('admin_endpoint', default='0.0.0.0:%(admin_port)s/',
                   help='admin_bind_host'),
        cfg.StrOpt('public_endpoint', default='0.0.0.0:%(public_port)s/',
                   help='admin_bind_host'),
    ],
    'moon': [
        cfg.StrOpt('keystone_admin_endpoint_v3', default='http://0.0.0.0:%(admin_port)s/v3',
                   help='keystone_admin_endpoint_v3'),
        cfg.StrOpt('kesytone_admin_endpoint_v2', default='http://0.0.0.0:%(admin_port)s/v22',
                   help='Connection password between OpenStack hooks and the Moon platform'),
        cfg.StrOpt('cnx_password', default='P4ssw0rd',
                   help='Connection password between OpenStack hooks and the Moon platform'),
        cfg.BoolOpt('block_unknown_tenant', default=False,
                    help='Does Moon block tenant that are not connected to a security extension'),
        cfg.StrOpt('moon_tenant', default='admin',
                   help='moon_tenant'),
        cfg.StrOpt('keystone_admin', default='admin',
                   help='keystone_admin'),
        cfg.StrOpt('keystone_admin_password', default='nomoresecretenomoresecrete',
                   help='keystone_admin_password'),
    ]
}

CONF = cfg.CONF


def configure(conf=None):
    if conf is None:
        conf = CONF

    for section in FILE_OPTIONS:
        for option in FILE_OPTIONS[section]:
            if section:
                conf.register_opt(option, group=section)
            else:
                conf.register_opt(option)

