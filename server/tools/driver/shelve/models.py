import shelve
from moon import settings
import logging
from contextlib import closing
from datetime import datetime

logger = logging.getLogger('moon.tools.driver.shelve_driver')


def get_db_filename():
    DATABASES = getattr(settings, "DATABASES")
    if not 'log' in DATABASES or not 'ENGINE' in DATABASES['log']:
        raise(Exception("Unknown database engine {engine}".format(engine=DATABASES['log']['ENGINE'])))
    return DATABASES['log']['NAME']


def create_tables():
    s = shelve.open(get_db_filename())
    s["date"] = datetime.now()
    if "logs" not in s:
        s["logs"] = []
    s.close()


def read(limit=None):
    s = shelve.open(get_db_filename())
    logs = []
    if "logs" not in s:
        logs = []
    if limit:
        logs = s["logs"][-limit:]
    else:
        logs = s["logs"]
    s.close()
    return logs


def write(log=None):
    s = shelve.open(get_db_filename())
    s["date"] = datetime.now()
    d = s["logs"]
    d.append(log)
    s["logs"] = d
    s.close()