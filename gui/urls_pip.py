from django.conf.urls import patterns, url

urlpatterns = patterns(
    'gui.views_pip',
    url(r'tenants/$', 'tenants'),
    url(r'tenant/(?P<tenant_uuid>[\w-]{32,36})$', 'tenants'),
    url(r'subjects/(?P<tenant_uuid>[\w-]{32,36})$', 'subjects'),
    url(r'objects/(?P<tenant_uuid>[\w-]{32,36})$', 'objects'),
    url(r'roles/(?P<tenant_uuid>[\w-]{32,36})/(?P<user_uuid>[\w-]{32,36})$', 'roles'),
    url(r'groups/(?P<tenant_uuid>[\w-]{32,36})/(?P<user_uuid>[\w-]{32,36})$', 'groups'),
    url(r'assignments/roles/(?P<tenant_uuid>[\w-]{32,36})/(?P<user_uuid>[\w-]{32,36})$', 'role_assignments'),
    url(r'assignments/groups/(?P<tenant_uuid>[\w-]{32,36})/(?P<user_uuid>[\w-]{32,36})$', 'group_assignments'),
)

