from django.conf.urls import patterns, include, url

from django.contrib import admin
# import openstack_auth
from django.views.generic import TemplateView

from openstack_auth.utils import patch_middleware_get_user


patch_middleware_get_user()

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'moon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'', include('openstack_auth.urls'))
    url(r"^", include("gi.urls")),
    #url(r"^users/", include("gi.urls")),
    url(r"^auth/", include('openstack_auth.urls')),
    #url(r"^$", TemplateView.as_view(template_name="auth/blank.html"))
)
