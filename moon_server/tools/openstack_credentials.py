#!/usr/bin/env python

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


import os
from moon_server import settings


def get_keystone_creds(admin_token=False):
    d = dict()
    if 'OS_SERVICE_ENDPOINT' in os.environ.keys() or 'OS_USERNAME' in os.environ.keys():
        if admin_token:
            d['endpoint'] = os.environ['OS_SERVICE_ENDPOINT']
            d['token'] = os.environ['OS_SERVICE_TOKEN']
        else:
            d['username'] = os.environ['OS_USERNAME']
            d['password'] = os.environ['OS_PASSWORD']
            d['auth_url'] = os.environ['OS_AUTH_URL']
            d['tenant_name'] = os.environ['OS_TENANT_NAME']
    else:
        if admin_token:
            d['endpoint'] = getattr(settings, 'OS_SERVICE_ENDPOINT')
            d['token'] = getattr(settings, 'OS_SERVICE_TOKEN')
        else:
            d['username'] = getattr(settings, 'OS_USERNAME')
            d['password'] = getattr(settings, 'OS_PASSWORD')
            d['auth_url'] = getattr(settings, 'OS_AUTH_URL')
            d['tenant_name'] = getattr(settings, 'OS_TENANT_NAME')
    return d


def get_nova_creds(version="1.1", admin_token=False):
    d = dict()
    if 'OS_SERVICE_ENDPOINT' in os.environ.keys() or 'OS_USERNAME' in os.environ.keys():
        if admin_token:
            d['endpoint'] = os.environ['OS_SERVICE_ENDPOINT']
            d['token'] = os.environ['OS_SERVICE_TOKEN']
        else:
            d['username'] = os.environ['OS_USERNAME']
            if version == "1.1":
                d['api_key'] = os.environ['OS_PASSWORD']
            else:
                d['password'] = os.environ['OS_PASSWORD']
            d['auth_url'] = os.environ['OS_AUTH_URL']
            d['project_id'] = os.environ['OS_TENANT_NAME']
    else:
        if admin_token:
            d['endpoint'] = getattr(settings, 'OS_SERVICE_ENDPOINT')
            d['token'] = getattr(settings, 'OS_SERVICE_TOKEN')
        else:
            d['username'] = getattr(settings, 'OS_USERNAME')
            if version == "1.1":
                d['api_key'] = getattr(settings, 'OS_PASSWORD')
            else:
                d['password'] = getattr(settings, 'OS_PASSWORD')
            d['auth_url'] = getattr(settings, 'OS_AUTH_URL')
            d['project_id'] = getattr(settings, 'OS_TENANT_NAME')
    return d