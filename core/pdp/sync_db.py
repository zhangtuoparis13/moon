from moon import settings
import importlib


DATABASES = getattr(settings, "DATABASES")
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

    def set_to_db(self, data):
        self.db.set_to_db(data)

    def get_from_db(self, uuid=None):
        return self.db.get_from_db(uuid)

    def drop(self):
        return self.db.drop()