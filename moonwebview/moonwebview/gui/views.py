#!/usr/bin/env python

# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from moonwebview.server import settings


@login_required()
def index(request):
    """
    Front interface of the application
    """
    wrapper = file(os.path.join(settings.STATIC_ROOT, 'index.html')).read()
    return HttpResponse(wrapper, content_type="text/html; charset=utf-8")
