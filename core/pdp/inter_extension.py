from uuid import uuid4
try:
    from django.utils.safestring import mark_safe
except ImportError:
    mark_safe = str

from moon.core.pdp.extension import VirtualEntity
from moon.core.pdp.sync_db import InterExtensionSyncer


class InterExtension:
    def __init__(self, requesting_intra_extension, requested_intra_extension):
        self.__uuid = str(uuid4())
        self.requesting_intra_extension = requesting_intra_extension
        self.requested_intra_extension = requested_intra_extension
        self.__vEnts = list()
        self.__syncer = InterExtensionSyncer()

    def create_collaboration(self, type, subs, objs, act):
        _vEnt = VirtualEntity(type)
        if type == 'trust':
            self.requesting_intra_extension.create_requesting_collaboration('authz', subs, _vEnt, act)
            self.requested_intra_extension.create_requested_collaboration('authz', _vEnt, objs, act)
        elif type == 'coordinate':
            self.requesting_intra_extension.create_requesting_collaboration('admin', subs, _vEnt, act)
            self.requested_intra_extension.create_requested_collaboration('admin', _vEnt, objs, act)
        else:  # other relations like inheritance
            pass
        self.__vEnts.append(_vEnt)

    def authz(self, sub, obj, act):
        for _vEnt in self.__vEnts:
            if self.requesting_intra_extension(sub, _vEnt, act) and self.requested_intra_extension(_vEnt, obj, act):
                return True

    def get_uuid(self):
        return self.__uuid