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

from django.contrib import admin
from django.conf.urls import patterns, include, url
from openstack_auth.utils import patch_middleware_get_user
import moon_server.gui.urls_json
import moon_server.gui.urls_pip
import moon_server.mrm.urls
import openstack_auth.urls

admin.autodiscover()
patch_middleware_get_user()


urlpatterns = patterns(
    'moon_server.gui.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^json/', include(moon_server.gui.urls_json)),
    url(r'^pip/', include(moon_server.gui.urls_pip)),
    url(r'^$', 'index'),
    url(r"^auth/", include(openstack_auth.urls)),
    url(r'^logs/', 'logs_repository'),
    # URL for the authorisation API for Keystone, Nova, ...
    url(r"^mrm/", include(moon_server.mrm.urls)),
)
