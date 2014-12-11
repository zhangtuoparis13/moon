# Copyright 2014 Orange
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import shelve
from moon_server import settings
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