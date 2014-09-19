from django.conf.urls import patterns, url

urlpatterns = patterns(
    'gui.views_json',
    url(r'intra-extensions/$',
        'intra_extensions'),
    url(r'intra-extension/(?P<uuid>[\w-]{32,36})/$',
        'intra_extension'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/subjects/$',
        'subjects'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/objects/$',
        'objects'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/subject_categories/$',
        'subject_categories'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/object_categories/$',
        'object_categories'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/subject_category/(?P<name>[\w-]{32,36})/$',
        'subject_category'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/object_category/(?P<name>[\w-]{32,36})/$',
        'object_category'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/subject_category/$',
        'subject_category'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/object_category/$',
        'object_category'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/subject_category_values/$',
        'subject_category_values'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/object_category_values/$',
        'object_category_values'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/subject_category_value/(?P<cat>[\w-]+)/(?P<value>[\w-]+)/$',
        'subject_category_value'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/object_category_value/(?P<cat>[\w-]+)/(?P<value>[\w-]+)/$',
        'object_category_value'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/subject_category_value/$',
        'subject_category_value'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/object_category_value/$',
        'object_category_value'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/subject_assignments/$',
        'subject_assignments'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/object_assignments/$',
        'object_assignments'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/subject_assignment/(?P<uuid>[\w-]+)/$',
        'subject_assignment'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/object_assignment/(?P<uuid>[\w-]+)/$',
        'object_assignment'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/rules/$',
        'rules'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/rule/$',
        'rule'),
    url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/rule/(?P<uuid>[\w-]+)/$',
        'rule'),
)