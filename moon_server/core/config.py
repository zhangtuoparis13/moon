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

from oslo.config import cfg
from oslo import messaging

FILE_OPTIONS = {
    'openstack': [
        cfg.StrOpt('OPENSTACK_KEYSTONE_URL', default='http://openstackserver:5000/v3',
                   help='URL of the OpenStack server'),
        cfg.StrOpt('OS_USERNAME', default='admin',
                   help='Name of the OpenStack administrator'),
        cfg.StrOpt('OS_PASSWORD', default='nomoresecrete',
                   help='Password of the OpenStack administrator'),
        cfg.StrOpt('OS_TENANT_NAME', default='admin',
                   help='Tenant name of the OpenStack administrator'),
        cfg.StrOpt('OS_AUTH_URL', default='http://openstackserver:5000/v3',
                   help='URL of the OpenStack server'),
    ],
    'moon': [
        cfg.StrOpt('CNX_PASSWORD', default='nomoresecrete',
                   help='Connection password between OpenStack hooks and the Moon platform'),
        cfg.BoolOpt('BLOCK_UNKNOWN_TENANT', default=False,
                    help='Does Moon block tenant that are not connected to a security extension'),

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

