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

from pymongo import MongoClient


class DB:

    def __init__(self, db_name="moon", collection_name="extensions"):
        self.client = MongoClient()
        self.database = eval("self.client.{}".format(db_name))
        self.collection = eval("self.database.{}".format(collection_name))

    def set_to_db(self, extension_data):
        _extensions = self.collection.find()
        _extension_data = self.collection.find_one({"_id": extension_data["_id"]})
        if _extension_data:
            _extensions.update({"_id": _extension_data["_id"]}, extension_data)
        else:
            self.collection.insert(extension_data)

    def get_from_db(self, uuid=None):
        if uuid:
            return self.collection.find_one({"_id": uuid})
        else:
            _records = self.collection.find()
            _record_dict = dict()
            for _r in _records:
                _record_dict[_r["_id"]] = _r
            return _record_dict

    def drop(self):
        self.collection.drop()
