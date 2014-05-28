from tenant_repository.models import Tenant
import shelve
from moon import settings
import logging
from contextlib import closing

logger = logging.getLogger('moon.tenant_repository.shelve_driver')

# dbfile = None
# dbhandler = None


def get_db_filename():
    DATABASES = getattr(settings, "DATABASES")
    if not 'tenant_db' in DATABASES or not 'ENGINE' in DATABASES['tenant_db']:
        raise(Exception("Unknown database engine {engine}".format(engine=DATABASES['tenant_db']['ENGINE'])))
    return DATABASES['tenant_db']['NAME']


# def open_db():
#     global dbfile, dbhandler
#     DATABASES = getattr(settings, "DATABASES")
#     if not 'tenant_db' in DATABASES or not 'ENGINE' in DATABASES['tenant_db']:
#         raise(Exception("Unknown database engine {engine}".format(engine=DATABASES['tenant_db']['ENGINE'])))
#
#     dbfile = DATABASES['tenant_db']['NAME']
#     dbhandler = shelve.open(dbfile)
#
#
# def get_dbhandler():
#     global dbhandler
#     if not dbhandler:
#         open_db()
#     return dbhandler


# class Tenant(models.Tenant):
#     """
#     Database Model for a Tenant / Project
#     """
#     __tablename__ = 'tenant'
#     uuid = str()
#     name = str()
#     domain = str()
#     description = str()
#     parent = str()
#     children = list()
#     enabled = bool()


def create_tables():
    s = shelve.open(get_db_filename())
    s.close()


def add_project_to_tenantdb(tenant=None):
    with closing(shelve.open(get_db_filename())) as dbhandler:
        logger.debug("Add tenant {}".format(tenant.name))
        # t = Tenant()
        # t.uuid = tenant.uuid
        # t.name = tenant.name
        # t.domain = tenant.domain_id
        # t.enabled = tenant.enabled
        # t.children = list()
        # t.parent = ""
        dbhandler[str(tenant.uuid)] = tenant
        dbhandler.sync()


def set_tenant(tenant):
    with closing(shelve.open(get_db_filename())) as dbhandler:
        dbhandler[tenant.uuid] = tenant
        dbhandler.sync()

# def save_to_db(tenant_uuid="", tenant_obj=None):
#     with closing(shelve.open(get_db_filename())) as dbhandler:
#         dbhandler[tenant_uuid] = tenant_obj
#         dbhandler.sync()


def get_tenant_by_name(name=""):
    with closing(shelve.open(get_db_filename())) as dbhandler:
        for tenant in dbhandler:
            if tenant.name == name:
                return tenant


def get_tenant_by_uuid(uuid=None):
    with closing(shelve.open(get_db_filename())) as dbhandler:
        if str(uuid) in dbhandler:
            # print("children of {} is {}".format(uuid, str(dbhandler[str(uuid)].children)))
            return dbhandler[str(uuid)]


def get_tenants():
    all_tenants = []
    with closing(shelve.open(get_db_filename())) as dbhandler:
        for uuid in dbhandler.keys():
            all_tenants.append(dbhandler[uuid])
    return all_tenants


def get_tenant(uuid=None):
    return get_tenant_by_uuid(uuid=uuid)


def set_tenant_relationship(tenant_up="", tenant_bottom=""):
    tenant_up_uuid = str(tenant_up)
    tenant_bottom_uuid = str(tenant_bottom)
    tenant_up_obj = None
    tenant_bottom_obj = None
    with closing(shelve.open(get_db_filename())) as dbhandler:
        if tenant_up_uuid not in dbhandler:
            tenant_up_obj = get_tenant_by_name(name=tenant_up_uuid)
        else:
            tenant_up_obj = dbhandler[tenant_up_uuid]
        if tenant_bottom_uuid not in dbhandler:
            tenant_bottom_obj = get_tenant_by_name(name=tenant_bottom_uuid)
        else:
            tenant_bottom_obj = dbhandler[tenant_bottom_uuid]
        __chidren = tenant_up_obj.children
        __chidren.append(tenant_bottom)
        tenant_up_obj.children = __chidren
        tenant_bottom_obj.parent = tenant_up
        dbhandler[tenant_up_uuid] = tenant_up_obj
        dbhandler[tenant_bottom_uuid] = tenant_bottom_obj
        dbhandler.sync()
        # save_to_db(tenant_uuid=tenant_up_uuid, tenant_obj=tenant_up_obj)
        # save_to_db(tenant_uuid=tenant_bottom_uuid, tenant_obj=tenant_bottom_obj)
    # with closing(shelve.open(get_db_filename())) as dbhandler:
    #     print(dbhandler)


def unset_tenant_relationship(tenant_up="", tenant_bottom=""):
    tenant_up_uuid = str(tenant_up)
    tenant_bottom_uuid = str(tenant_bottom)
    tenant_up_obj = None
    tenant_bottom_obj = None
    with closing(shelve.open(get_db_filename())) as dbhandler:
        if tenant_up_uuid not in dbhandler:
            tenant_up_obj = get_tenant_by_name(name=tenant_up_uuid)
        else:
            tenant_up_obj = dbhandler[tenant_up_uuid]
        if tenant_bottom_uuid not in dbhandler:
            tenant_bottom_obj = get_tenant_by_name(name=tenant_bottom_uuid)
        else:
            tenant_bottom_obj = dbhandler[tenant_bottom_uuid]
        __chidren = tenant_up_obj.children
        try:
            __chidren.remove(tenant_bottom_uuid)
            tenant_up_obj.children = __chidren
        except ValueError:
            #tenant_bottom_uuid not in __chidren
            pass
        if tenant_bottom_obj.parent == tenant_up:
            tenant_bottom_obj.parent = ""
        dbhandler[tenant_up_uuid] = tenant_up_obj
        dbhandler[tenant_bottom_uuid] = tenant_bottom_obj
        dbhandler.sync()