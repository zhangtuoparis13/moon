
DATABASES = {
    'user_db': {
        'ENGINE': 'moon.tools.driver.mysql',
        'NAME': "user_db",
        'USER': "moonuser",
        'PASSWORD': "P4ssw0rd",
        'HOST': "127.0.0.1",
        'PORT': "3306"
    },
    'intra-extensions': {
        'ENGINE': 'moon.tools.driver.mongodb',
        'NAME': "moon",
        'USER': "",
        'PASSWORD': "",
        'HOST': "127.0.0.1",
        'PORT': "27017"
    },
    'inter-extensions': {
        'ENGINE': 'moon.tools.driver.mongodb',
        'NAME': "moon",
        'USER': "",
        'PASSWORD': "",
        'HOST': "127.0.0.1",
        'PORT': "27017"
    },
    'tenant_db': {
        'ENGINE': 'moon.tools.driver.mongodb',
        'NAME': "/etc/moon/tenant.db",
        'USER': "",
        'PASSWORD': "",
        'HOST': "",
        'PORT': ""
    },
    'log': {
        'ENGINE': 'moon.tools.driver.shelve',
        'NAME': "/var/log/moon/log.db",
        'USER': "",
        'PASSWORD': "",
        'HOST': "",
        'PORT': ""
    }
}

DEFAULT_EXTENSION_TABLE = "/etc/moon/policy/intra_ext_example.json"

OPENSTACK_KEYSTONE_URL = "http://openstackserver:5000/v3"

OPENSTACK_API = "/etc/moon/api.json"

CNX_PASSWORD = "P4ssw0rd"

OS_USERNAME = "admin"
OS_PASSWORD = "set a password here"
OS_TENANT_NAME = "admin"
OS_AUTH_URL = "http://openstackserver:5000/v2.0/"
#OS_SERVICE_ENDPOINT = "http://openstackserver:35357/v3/"
#OS_SERVICE_TOKEN = "set a password here"
#OS_REGION_NAME = "regionOne"