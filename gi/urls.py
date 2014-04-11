from django.conf.urls import patterns, include, url
from openstack_auth.utils import patch_middleware_get_user

from gi import views
patch_middleware_get_user()

urlpatterns = patterns('gi.views',
    url(r'^$', views.index, name="index"),
    url(r'^users/', views.users, name="users"),
    url(r'^projects/', views.projects, name="users"),
    url(r'^roles/', views.roles, name="users"),
)
