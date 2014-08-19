
DATABASES = {
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

BLOCK_UNKNOWN_TENANT = False

SYNC_CONF_FILENAME = "/etc/moon/tenants.json"

UNMANAGED_OBJECTS = ("", "token", )

OS_USERNAME = "admin"
OS_PASSWORD = "P4ssw0rd"
OS_TENANT_NAME = "admin"
OS_AUTH_URL = "http://openstackserver:5000/v2.0/"
#OS_SERVICE_ENDPOINT = "http://openstackserver:35357/v3/"
#OS_SERVICE_TOKEN = "set a password here"
#OS_REGION_NAME = "regionOne"