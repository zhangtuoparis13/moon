from django.contrib import admin
from django.conf.urls import patterns, include, url
from openstack_auth.utils import patch_middleware_get_user
# import gi.views
# print(gi.views)
admin.autodiscover()
patch_middleware_get_user()


urlpatterns = patterns(
    'gui.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index'),
    url(r'^sync/$', 'sync'),
    url(r'^sync/(?P<uuid>\w{32})/$', 'sync'),
    url(r"^auth/", include('openstack_auth.urls')),
    url(r'^intra-extensions/(?P<uuid>\w{32})/$', 'intra_extension'),
    url(r'^intra-extensions/(?P<uuid>\w{32})/type/(?P<type>\w+)/$', 'intra_extension_attributes'),  # return JSON
    url(r'^inter-extensions/(?P<uuid>\w{32})/$', 'inter_extension'),
    url(r'^intra-extensions/', 'intra_extensions'),
    url(r'^inter-extensions/', 'inter_extensions'),
    url(r'^tenants/$', 'tenants'),
    # url(r'^authz/$', 'authz'),
    url(r'^roles/$', 'roles'),
    # url(r'^users/(?P<id>\w{32})/$', 'user'),
    # url(r'^users/', 'users'),
    # url(r'^projects/', 'projects'),
    # url(r'^userdb/', 'userdb'),
    # url(r'^policies/', 'policy_repository'),
    # URL that send JSON objects
    url(r'^tenant/(?P<uuid>\w{32})/$', 'get_tenants'),  # return JSON
    url(r'^tenant/(?P<uuid>\w{32})/subjects', 'get_subjects'),  # return JSON
    url(r'^tenant/(?P<uuid>\w{32})/objects', 'get_objects'),  # return JSON
    url(r'^logs/', 'logs_repository'),
    url(r'^roles/(?P<uuid>\w{32})/$', 'roles'),
    # URL for the authorisation API for Keystone, Nova, ...
    url(r"^mrm/", include('mrm.urls')),
)
