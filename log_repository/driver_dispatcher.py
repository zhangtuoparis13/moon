from moon import settings
import importlib
from datetime import datetime


DATABASES = getattr(settings, "DATABASES")
if not 'log' in DATABASES or not 'ENGINE' in DATABASES['log']:
    raise(Exception("Unknown database engine {engine}".format(engine=DATABASES['log']['ENGINE'])))

drivername = DATABASES['log']['ENGINE']
driver = importlib.import_module(drivername)
driver.create_tables()


class Log:
    def __init__(self, date=None, value=None):
        if not date:
            self.date = datetime.now()
        else:
            self.date = date
        self.value = value


class Logs:
    def __init__(self):
        self.list = driver.read(limit=None)

    def read(self, limit=10):
        """Return [limit] line of logs
        """
        if limit:
            return self.list[-limit:]
        else:
            return self.list

    def write(self, line=""):
        log = Log(value=line)
        self.list.append(log)
        driver.write(log)

log_manager = Logs()


def get_log_manager():
    return log_manager