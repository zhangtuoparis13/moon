#!/usr/bin/env python
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