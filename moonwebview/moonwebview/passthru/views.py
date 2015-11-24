#!/usr/bin/env python

# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from moonwebview.server import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import httplib
import json
import re


def __get_url(host, port, url, post_data=None, delete_data=None, method="GET", authtoken=None):
    if post_data:
        method = "POST"
    if delete_data:
        method = "DELETE"
    #print("\033[32m{} {}\033[m".format(method, url))
    conn = httplib.HTTPConnection(host, port)
    #print("Host: {}:{}".format(host, port))
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    if authtoken:
        headers["X-Auth-Token"] = authtoken
    if post_data:
        method = "POST"
        headers["Content-type"] = "application/json"
        # post_data = json.dumps(post_data)
        conn.request(method, url, post_data, headers=headers)
    elif delete_data:
        method = "DELETE"
        conn.request(method, url, json.dumps(delete_data), headers=headers)
    else:
        conn.request(method, url, headers=headers)
    resp = conn.getresponse()
    content = resp.read()
    conn.close()
    try:
        return json.loads(content)
    except ValueError:
        return {"error": content}


@login_required()
@csrf_exempt
def passthru(request, url=None):
    """
    Front interface of the application
    """
    # TODO: set an applicative FW to limit the use of the API
    from django.contrib.auth import get_user as xxx_get_user
    user = xxx_get_user(request)
    method = request.method
    endpoint = request.session["region_endpoint"]
    host, port = re.findall("(\d+\.\d+\.\d+\.\d+):(\d+)", endpoint)[0]
    post_data = None
    delete_data = None
    if method == "POST":
        post_data = request.body
    elif method == "DELETE":
        delete_data = request.body
    response = __get_url(
        host=host,
        port=int(port),
        url="/" + url,
        post_data=post_data,
        delete_data=delete_data,
        method=method,
        authtoken=user.token.id)
    return JsonResponse(response)
