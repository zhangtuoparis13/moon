from tenant_repository.models import Tenant
import shelve
from moon import settings
import logging
from contextlib import closing
import time

logger = logging.getLogger('moon.log_repository.shelve_driver')


def get_db_filename():
    DATABASES = getattr(settings, "DATABASES")
    if not 'tenant_db' in DATABASES or not 'ENGINE' in DATABASES['log']:
        raise(Exception("Unknown database engine {engine}".format(engine=DATABASES['log']['ENGINE'])))
    return DATABASES['log']['NAME']


def create_tables():
    s = shelve.open(get_db_filename())
    s["date"] = time.time()
    if "logs" not in s:
        s["logs"] = []
    s.close()


def read(limit=None):
    s = shelve.open(get_db_filename())
    if "logs" not in s:
        return []
    if limit:
        return s["logs"][-limit:]
    else:
        return s["logs"]


def write(log=None):
    s = shelve.open(get_db_filename())
    s["date"] = time.time()
    s["logs"].append(log)
    s.close()