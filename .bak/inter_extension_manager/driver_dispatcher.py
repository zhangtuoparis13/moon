import logging
import json
from moon import settings
import importlib
from uuid import uuid4

logger = logging.getLogger(__name__)

DATABASES = getattr(settings, "DATABASES")
if not 'inter-extensions' in DATABASES or not 'ENGINE' in DATABASES['inter-extensions']:
    raise(Exception("Unknown database engine {engine}".format(engine=DATABASES['inter-extensions']['ENGINE'])))

drivername = DATABASES['inter-extensions']['ENGINE']
db_name = DATABASES['inter-extensions']['NAME']
driver = importlib.import_module(drivername)


class Dispatcher:

    def __init__(self):
        self.db = driver.DB(db_name=db_name, collection_name="interextensions")

    def add(self, attributes={}):
        return self.db.add(attributes=attributes)

    def list(self, object_type="tenant"):
        return self.db.get({"type": object_type})

    def get(self, attributes=None):
        return self.db.get(attributes=attributes)

    def delete(self, uuid=None):
        return self.db.delete(uuid=uuid)

    def drop(self):
        return self.db.drop()

    def add_tenant(self,
                   attributes=None,
                   name=None,
                   description=None,
                   enabled=None,
                   domain=None,
                   uuid=None):
        return self.db.add_tenant(
            attributes=attributes,
            name=name,
            description=description,
            enabled=enabled,
            domain=domain,
            uuid=uuid)

    def add_tenant_assignment(self,
                              attributes=None,
                              requesting=None,
                              requested=None,
                              type=None,
                              category=None,
                              uuid=None):
        return self.db.add_tenant_assignment(
            attributes=attributes,
            requesting=requesting,
            requested=requested,
            type=type,
            category=category,
            uuid=uuid)

    def delete_tables(self):
        return self.db.drop()


driver_dispatcher = Dispatcher()


def get_dispatcher():
    return driver_dispatcher