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
            return self.collection.find()

    def drop(self):
        self.collection.drop()
