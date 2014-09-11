from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'gui.views_json',
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/subjects/$', 'get_subjects'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/objects/$', 'get_objects'),
    url(r'^tenant/(?P<uuid>\w{32})/$', 'get_tenants'),
    url(r'intra-extensions/(?P<uuid>[\w-]{32,36})/$', 'intra_extension'),
    url(r'intra-extensions/', 'intra_extensions'),
)