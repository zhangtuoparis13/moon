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

from moon_server import settings
import importlib


DATABASES = getattr(settings, "MOON_DATABASES")
if not 'intra-extensions' in DATABASES or not 'ENGINE' in DATABASES['intra-extensions']:
    raise(Exception("Unknown database engine {engine}".format(engine=DATABASES['intra-extensions']['ENGINE'])))

db_driver_name = DATABASES['intra-extensions']['ENGINE']
db_name = DATABASES['intra-extensions']['NAME']
db_driver = importlib.import_module(db_driver_name)


class IntraExtensionSyncer():
    def __init__(self):
        self.db = db_driver.DB(db_name, "intraextensions")

    def backup_intra_extension_to_db(self, data):
        self.db.set_to_db(data)

    def get_intra_extension_from_db(self, uuid):
        return self.db.get_from_db(uuid)

    def drop(self):
        return self.db.drop()


class IntraExtensionsSyncer():
    def __init__(self):
        self.db = db_driver.DB(db_name, "intraextensions")

    def get_intra_extensions_from_db(self):
        return self.db.get_from_db()

    def drop(self):
        return self.db.drop()


class InterExtensionSyncer():
    def __init__(self):
        self.db = db_driver.DB(db_name, "interextensions")

    def backup_inter_extension_to_db(self, data):
        self.db.set_to_db(data)

    def get_from_db(self, uuid=None):
        return self.db.get_from_db(uuid)

    def drop(self):
        return self.db.drop()