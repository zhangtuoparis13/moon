"""
Moon settings which include Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os

MOON_DATABASES = {
    'intra-extensions': {
        'ENGINE': 'moon_server.tools.driver.mongodb',
        'NAME': "moon",
        'USER': "",
        'PASSWORD': "",
        'HOST': "127.0.0.1",
        'PORT': "27017"
    },
    'inter-extensions': {
        'ENGINE': 'moon_server.tools.driver.mongodb',
        'NAME': "moon",
        'USER': "",
        'PASSWORD': "",
        'HOST': "127.0.0.1",
        'PORT': "27017"
    },
    'log': {
        'ENGINE': 'moon_server.tools.driver.shelve',
        'NAME': "/var/log/moon/log.db",
        'USER': "",
        'PASSWORD': "",
        'HOST': "",
        'PORT': ""
    }
}

OPENSTACK_KEYSTONE_URL = "http://openstackserver:5000/v3"

CNX_PASSWORD = "P4ssw0rd"

BLOCK_UNKNOWN_TENANT = False

UNMANAGED_OBJECTS = ("", "token", )

OS_USERNAME = "admin"
OS_PASSWORD = "P@ssw0rd"
OS_TENANT_NAME = "admin"
OS_AUTH_URL = "http://openstackserver:5000/v2.0/"


#########################################################
# Specific settings for Django
#########################################################

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (BASE_DIR, os.path.join(BASE_DIR, 'gui/templates'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<select id>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'moon_server.gui.urls'

WSGI_APPLICATION = 'moon_server.gui.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = dict()
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': "moon",
    'USER': "moonuser",
    'PASSWORD': "nomoresecrete",
    'HOST': "",
    'PORT': ""
}

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
    os.path.join(BASE_DIR, "moon_server/gui/static"),
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
    "moon_server.gui",
    "moon_server.mrm",
)

AUTHENTICATION_BACKENDS = (
    'openstack_auth.backend.KeystoneBackend',
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = "/auth/login/"

OPENSTACK_API_VERSIONS = {
    "identity": 3
}

OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = False

OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'Default'

# NOTE(saschpe): The openstack_auth.user.Token object isn't JSON-serializable ATM
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

APPEND_SLASH = False
