from moon import settings
import importlib


DATABASES = getattr(settings, "DATABASES")
if not 'intra-extensions' in DATABASES or not 'ENGINE' in DATABASES['intra-extensions']:
    raise(Exception("Unknown database engine {engine}".format(engine=DATABASES['intra-extensions']['ENGINE'])))

db_driver_name = DATABASES['intra-extensions']['ENGINE']
db_name = DATABASES['intra-extensions']['NAME']
db_driver = importlib.import_module(db_driver_name)


class Intra_Extension_Syncer():

    def __init__(self):
        self.db = db_driver.DB(db_name, "intraextensions")

    def sync(self, data):
        self.db.sync(data)

    def drop(self):
        return self.db.drop()

