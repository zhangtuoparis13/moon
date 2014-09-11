from pymongo import MongoClient


class DB:

    def __init__(self, db_name="moon", collection_name="extensions"):
        self.client = MongoClient()
        self.database = eval("self.client.{}".format(db_name))
        self.collection = eval("self.database.{}".format(collection_name))

    def sync(self, extension_data):
        _extensions = self.collection.find()
        _extension_data = self.collection.find_one({"_id": extension_data["_id"]})
        if _extension_data:
            _extensions.update({"_id": _extension_data["_id"]}, extension_data)
        else:
            self.collection.insert(extension_data)

    def get(self, attributes=dict()):
        """Return a list of extensions with attributes"""
        collections = tuple(self.collection.find(attributes))
        return collections

    def drop(self):
        self.collection.drop()
