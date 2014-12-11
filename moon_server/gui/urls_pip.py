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

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'gui.views_pip',
    url(r'projects/?$', 'projects'),
    url(r'projects/(?P<project_uuid>[\w-]{32,36})/?$', 'projects'),
    url(r'projects/(?P<project_uuid>[\w-]{32,36})/users/?$', 'users'),
    url(r'projects/(?P<project_uuid>[\w-]{32,36})/users/(?P<user_uuid>[\w-]{3,36})/?$', 'users'),
    url(r'projects/(?P<project_uuid>[\w-]{32,36})/objects/?$', 'objects'),
    url(r'projects/(?P<project_uuid>[\w-]{32,36})/objects/(?P<object_uuid>[\w-]{3,36})/?$', 'objects'),
    url(r'projects/(?P<project_uuid>[\w-]{32,36})/roles/?$', 'roles'),
    url(r'projects/(?P<project_uuid>[\w-]{32,36})/users/(?P<user_uuid>[\w-]{32,36})/roles/?$', 'roles'),
    url(r'projects/(?P<project_uuid>[\w-]{32,36})/groups/?$', 'groups'),
    url(r'projects/(?P<project_uuid>[\w-]{32,36})/users/(?P<user_uuid>[\w-]{32,36})/groups/?$', 'groups'),
    url(r'projects/(?P<project_uuid>[\w-]{32,36})/assignments/roles/?$', 'role_assignments'),
    url(r'projects/(?P<project_uuid>[\w-]{32,36})/assignments/groups/?$', 'group_assignments'),
    url(r'projects/(?P<project_uuid>[\w-]{32,36})/assignments/roles/(?P<user_uuid>[\w-]{32,36})/?$',
        'role_assignments'),
    url(r'projects/(?P<project_uuid>[\w-]{32,36})/assignments/groups/(?P<user_uuid>[\w-]{32,36})/?$',
        'group_assignments'),
    url(r'nova/images/?$', 'images'),
    url(r'nova/flavors/?$', 'flavors'),
)

