import logging
import json
from uuid import uuid4
from moon import settings
import importlib

logger = logging.getLogger(__name__)

DATABASES = getattr(settings, "DATABASES")
if not 'intra-extensions' in DATABASES or not 'ENGINE' in DATABASES['intra-extensions']:
    raise(Exception("Unknown database engine {engine}".format(engine=DATABASES['intra-extensions']['ENGINE'])))

drivername = DATABASES['intra-extensions']['ENGINE']
db_name = DATABASES['intra-extensions']['NAME']
driver = importlib.import_module(drivername)


class Dispatcher:

    def __init__(self):
        self.db = driver.DB(name=db_name, collection_name="intraextensions")

    def new_extension(self,
                      uuid=None,
                      name=None,
                      subjects=None,
                      objects=None,
                      metadata=None,
                      rules=None,
                      profiles=None,
                      description=None,
                      tenant=None,
                      model=None,
                      protocol=None
                      ):
        return self.db.new_extension(
            uuid=uuid,
            name=name,
            subjects=subjects,
            objects=objects,
            metadata=metadata,
            rules=rules,
            profiles=profiles,
            description=description,
            tenant=tenant,
            model=model,
            protocol=protocol)

    def list(self, type="extension"):
        return self.db.list(type=type)

    def get(self, attributes=None):
        return self.db.get(attributes=attributes)

    def delete(self, uuid):
        return self.db.delete(uuid=uuid)

    def delete_tables(self):
        return self.db.drop()

    def drop(self):
        return self.db.drop()


driver_dispatcher = Dispatcher()


def get_dispatcher():
    return driver_dispatcher