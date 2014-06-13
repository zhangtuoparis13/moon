from django.contrib import admin
from django.conf.urls import patterns, include, url
from openstack_auth.utils import patch_middleware_get_user

admin.autodiscover()
patch_middleware_get_user()


urlpatterns = patterns('gi.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index'),
    url(r'^intra-extensions/(?P<id>\w{32})/$', 'intra_extension'),
    url(r'^intra-extensions/', 'intra_extensions'),
    # url(r'^users/(?P<id>\w{32})/$', 'user'),
    # url(r'^users/', 'users'),
    # url(r'^projects/(?P<id>\w{32})/$', 'project'),
    # url(r'^projects/', 'projects'),
    # url(r'^roles/', 'roles'),
    # url(r'^userdb/', 'userdb'),
    # url(r'^policies/', 'policy_repository'),
    url(r'^logs/', 'logs_repository'),
    url(r"^auth/", include('openstack_auth.urls')),
    url(r"^mrm/", include('mrm.urls')),
)
