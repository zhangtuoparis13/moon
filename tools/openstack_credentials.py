#!/usr/bin/env python
import os


def get_keystone_creds(admin_token=False):
    d = dict()
    if admin_token:
        d['endpoint'] = os.environ['OS_SERVICE_ENDPOINT']
        d['token'] = os.environ['OS_SERVICE_TOKEN']
    else:
        d['username'] = os.environ['OS_USERNAME']
        d['password'] = os.environ['OS_PASSWORD']
        d['auth_url'] = os.environ['OS_AUTH_URL']
        d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d


def get_nova_creds(version="1.1", admin_token=False):
    d = dict()
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
    return d