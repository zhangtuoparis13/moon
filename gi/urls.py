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
    url(r'^sync/', 'sync'),
    url(r'^intra-extensions/(?P<id>\w{32})/$', 'intra_extension'),
    url(r'^intra-extensions/', 'intra_extensions'),
    url(r'^inter-extensions/(?P<id>\w{32})/$', 'inter_extension'),
    url(r'^inter-extensions/', 'inter_extensions'),
    # url(r'^users/(?P<id>\w{32})/$', 'user'),
    # url(r'^users/', 'users'),
    # url(r'^projects/(?P<id>\w{32})/$', 'project'),
    # url(r'^projects/', 'projects'),
    # url(r'^roles/', 'roles'),
    # url(r'^userdb/', 'userdb'),
    # url(r'^policies/', 'policy_repository'),
    url(r'^tenant/(?P<id>\w{32})/subjects', 'get_subjects'),
    url(r'^tenant/(?P<id>\w{32})/objects', 'get_objects'),
    url(r'^logs/', 'logs_repository'),
    url(r"^auth/", include('openstack_auth.urls')),
    url(r"^mrm/", include('mrm.urls')),
)
