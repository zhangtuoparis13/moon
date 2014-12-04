from django.contrib import admin
from django.conf.urls import patterns, include, url
from openstack_auth.utils import patch_middleware_get_user
import moon_server.gui.urls_json
import moon_server.gui.urls_pip
# import gi.views
# print(gi.views)
admin.autodiscover()
patch_middleware_get_user()


urlpatterns = patterns(
    'gui.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^json/', include(moon_server.gui.urls_json)),
    url(r'^pip/', include(moon_server.gui.urls_pip)),
    url(r'^$', 'index'),
    url(r'^sync/$', 'sync'),
    url(r'^sync/(?P<uuid>\w{32})/$', 'sync'),
    url(r"^auth/", include('openstack_auth.urls')),
    # url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/$', 'intra_extension'),
    # url(r'^inter-extensions/(?P<uuid>[\w-]{32,36})/$', 'inter_extension'),
    url(r'^intra-extensions/', 'intra_extensions'),
    url(r'^inter-extensions/', 'inter_extensions'),
    url(r'^logs/', 'logs_repository'),
    # URL for the authorisation API for Keystone, Nova, ...
    url(r"^mrm/", include('mrm.urls')),
)
