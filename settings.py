
DATABASES = {
    'user_db': {
        'ENGINE': 'moon.user_repository.mysql_driver',
        'NAME': "user_db",
        'USER': "moonuser",
        'PASSWORD': "P4ssw0rd",
        'HOST': "",
        'PORT': ""
    },
    'tenant_db': {
        'ENGINE': 'moon.tenant_repository.mysql_driver',
        'NAME': "tenant_db",
        'USER': "moonuser",
        'PASSWORD': "P4ssw0rd",
        'HOST': "",
        'PORT': ""
    }
}

#OPENSTACK_KEYSTONE_URL = "http://openstackserver:5000/v3"
OPENSTACK_KEYSTONE_URL = "http://p-trustedcloud3:5000/v3"

