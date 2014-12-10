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
