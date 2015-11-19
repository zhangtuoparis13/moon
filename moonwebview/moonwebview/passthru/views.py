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
from django.contrib.auth import get_user as xxx_get_user



#@login_required(login_url='/auth/login/')
@login_required()
def index(request):
    """
    Front interface of the application
    """
    # return render(request, "static/index.html")
    print(get_user_model())
    print(dir(xxx_get_user(request)))
    print(request)
    return HttpResponse("MOON -user={}- Will send a request to {}/".format(
        xxx_get_user(request), settings.OPENSTACK_KEYSTONE_URL))


@login_required()
def passthru(request, url=None):
    """
    Front interface of the application
    """
    # TODO: set an applicative FW to limit the use of the API
    # return render(request, "static/index.html")
    from django.contrib.auth import get_user as xxx_get_user
    print(dict(request.session))
    user = xxx_get_user(request)
    print(user.token)
    # return HttpResponse("MOON -user={}- Will send a request to {}/{}".format(
    #     get_user(request), settings.OPENSTACK_KEYSTONE_URL, url))
    return JsonResponse({'foo': url})
