"""
Moon settings which include Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
# import mongoengine
import os

MOON_DATABASES = {
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


#########################################################
# Specific settings for Django
#########################################################

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (BASE_DIR, os.path.join(BASE_DIR, 'gui/templates'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<select id>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition
#
# INSTALLED_APPS = (
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
# )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'moon.gui.urls'

WSGI_APPLICATION = 'moon.gui.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# MONGODB_DATABASES = {
#     'default': {'name': 'moon'}
# }
# DJANGO_MONGOENGINE_OVERRIDE_ADMIN = True
#TODO: change MySQL to MongoDB

DATABASES = dict()
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    'NAME': "moon",
    'USER': "moonuser",
    'PASSWORD': "P4ssw0rd",
    'HOST': "",
    'PORT': ""
}

# SESSION_ENGINE = 'mongoengine.django.sessions'

# _MONGODB_USER = ''
# _MONGODB_PASSWD = ''
# _MONGODB_HOST = '127.0.0.1'
# _MONGODB_NAME = 'moon'
# _MONGODB_DATABASE_HOST = \
#     'mongodb://%s/%s' \
#     % (_MONGODB_HOST, _MONGODB_NAME)
# _MONGODB_DATABASE_HOST = \
#     'mongodb://%s:%s@%s/%s' \
#     % (_MONGODB_USER, _MONGODB_PASSWD, _MONGODB_HOST, _MONGODB_NAME)

# mongoengine.connect(_MONGODB_NAME, host=_MONGODB_DATABASE_HOST)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "moon/gui/static"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'openstack_auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    "moon.gui",
    "moon.mrm",
    #"repositery",,
    # 'mongoengine.django.debug_toolbar',
    # 'mongoengine.django.auth',
    # 'mongoengine.django.admin.sites',
    # 'mongoengine.django.admin',
)

# OPENSTACK_KEYSTONE_URL = getattr(moon_settings, "OPENSTACK_KEYSTONE_URL")

AUTHENTICATION_BACKENDS = (
    'openstack_auth.backend.KeystoneBackend',
    # 'mongoengine.django.auth.MongoEngineBackend',
)

#ROOT_URLCONF = 'openstack_auth.tests.urls'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = "/auth/login/"

OPENSTACK_API_VERSIONS = {
    "identity": 3
}

OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = False

OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'Default'

# NOTE(saschpe): The openstack_auth.user.Token object isn't JSON-serializable ATM
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
