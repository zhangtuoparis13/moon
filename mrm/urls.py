from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()


urlpatterns = patterns(
    'mrm.views',
    # url(r'tenants', 'tenants'),
)
