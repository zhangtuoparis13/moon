from django.conf.urls import patterns, url

urlpatterns = patterns(
    'gui.views_json',
    url(r'intra-extensions/?$',
        'intra_extensions'),
    # url(r'intra-extension/?$',
    #     'intra_extension'),
    url(r'intra-extensions/(?P<uuid>[\w-]{32,36})/?$',
        'intra_extensions'),
    url(r'intra-extensions/(?P<uuid>[\w-]{32,36})/tenant/?$',
        'tenant'),
    url(r'intra-extensions/policies/?$',
        'policies'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/subjects/?$',
        'subjects'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/objects/?$',
        'objects'),
    # url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/subjects/?$',
    #     'subject'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/subjects/(?P<subject_id>[\w\-\_]{3,36})/?$',
        'subjects'),
    # url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/objects/?$',
    #     'object'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/objects/(?P<object_id>[\w\-\_]{3,36})/?$',
        'objects'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/subject_categories/?$',
        'subject_categories'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/object_categories/?$',
        'object_categories'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/subject_categories/(?P<category_id>[\w\-\_]{3,36})/?$',
        'subject_categories'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/object_categories/(?P<category_id>[\w\-\_]{3,36})/?$',
        'object_categories'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/subject_categories/?$',
        'subject_categories'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/object_categories/?$',
        'object_categories'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/subject_category_values/?$',
        'subject_category_values'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/object_category_values/?$',
        'object_category_values'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/subject_category_values/(?P<category_id>[\w\-\_]+)/(?P<value>[\w\-\_]{3,36})/?$',
        'subject_category_values'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/object_category_values/(?P<category_id>[\w\-\_]+)/(?P<value>[\w\-\_]{3,36})/?$',
        'object_category_values'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/subject_category_values/?$',
        'subject_category_values'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/object_category_values/?$',
        'object_category_values'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/subject_assignments/?$',
        'subject_assignments'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/object_assignments/?$',
        'object_assignments'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/subject_assignments/?$',
        'subject_assignments'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/object_assignments/?$',
        'object_assignments'),
    url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/rules/?$',
        'rules'),
    # url(r'^intra-extensions/(?P<uuid>[\w-]{32,36})/rules/?$',
    #     'rules'),
    # url(r'^intra-extension/(?P<uuid>[\w-]{32,36})/rule/(?P<rule_id>[\w\_\-]{3,36})/?$',
    #     'rule'),
    url(r'inter-extensions/?$',
        'inter_extensions'),
    # url(r'inter-extension/?$',
    #     'inter_extension'),
    url(r'inter-extensions/(?P<uuid>[\w-]{32,36})/?$',
        'inter_extensions'),
    url(r'super-extensions/?$',
        'super_extensions'),
    url(r'super-extensions/tenants/(?P<tenant_uuid>[\w-]{32,36})/intra_extensions/(?P<intra_extension_uuid>[\w-]{32,36})/?$',
        'super_extensions'),
    url(r'super-extensions/tenants/(?P<tenant_uuid>[\w-]{32,36})/intra_extensions/(?P<intra_extension_uuid>[\w-]{32,36})/?$',
        'super_extensions'),
)