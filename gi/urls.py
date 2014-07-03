from django.contrib import admin
from django.conf.urls import patterns, include, url
from openstack_auth.utils import patch_middleware_get_user
# import gi.views
# print(gi.views)
admin.autodiscover()
patch_middleware_get_user()


urlpatterns = patterns(
    'gi.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index'),
    url(r'^sync/$', 'sync'),
    url(r'^sync/(?P<id>\w{32})/$', 'sync'),
    url(r"^auth/", include('openstack_auth.urls')),
    url(r'^intra-extensions/(?P<id>\w{32})/$', 'intra_extension'),
    url(r'^intra-extensions/', 'intra_extensions'),
    url(r'^inter-extensions/(?P<id>\w{32})/$', 'inter_extension'),
    url(r'^inter-extensions/', 'inter_extensions'),
    url(r'^tenants/$', 'get_tenants'),
    # url(r'^users/(?P<id>\w{32})/$', 'user'),
    # url(r'^users/', 'users'),
    # url(r'^projects/', 'projects'),
    # url(r'^roles/', 'roles'),
    # url(r'^userdb/', 'userdb'),
    # url(r'^policies/', 'policy_repository'),
    # URL that send JSON objects
    url(r'^tenant/(?P<id>\w{32})/$', 'get_tenant'),
    url(r'^tenant/(?P<id>\w{32})/subjects', 'get_subjects'),
    url(r'^tenant/(?P<id>\w{32})/objects', 'get_objects'),
    url(r'^logs/', 'logs_repository'),
    # URL for the authorisation API for Keystone, Nova, ...
    url(r"^mrm/", include('mrm.urls')),
)
