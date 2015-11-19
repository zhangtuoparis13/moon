#!/usr/bin/env python

# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from django.conf.urls import url
from . import views

urlpatterns = [
   url(r'^(?P<url>[\w_/\-]+)$', views.passthru, name='passthru'),
]
