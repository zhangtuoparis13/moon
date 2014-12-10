from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()


urlpatterns = patterns(
    'moon_server.mrm.views',
    url(r'authz', 'mrm_authz'),
)
