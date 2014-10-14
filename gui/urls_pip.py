from django.conf.urls import patterns, url

urlpatterns = patterns(
    'gui.views_pip',
    url(r'projects/$', 'projects'),
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

