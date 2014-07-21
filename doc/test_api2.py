def enforce(param, mode="r"):
    def enforce_decorated(function):
        def wrapped(*args, **kwargs):
            interface = locals().get("args")[0]
            print("\t\033[31menforce\033[m raw_extension={}".format(getattr(interface, "_PublicAdminInterface__extension")))
            raw_extension = getattr(interface, "_PublicAdminInterface__extension")
            print("\tsubjects={}".format(raw_extension.get_subjects()))
            try:
                interface.adminAuthz()
            except:
                pass
            result = function(*args, **kwargs)
            return result
        return wrapped
    return enforce_decorated


class Extension(object):

    def __init__(self, *args, **kwargs):
        print("Init of Extension")
        self.__uuid = "azerty"
        self.__subjects = ["admin", "test"]

    def get_uuid(self):
        return self.__uuid

    def get_subjects(self, uuid=""):
        return self.__subjects

    def add_subjects(self, name):
        self.__subjects.append(name)

    def del_subjects(self, uuid):
        raise NotImplemented

    def set_subjects(self, uuid, name=""):
        raise NotImplemented


class PublicAuthzInterface:

    def __init__(self, extension=None):
        self.__extension = extension
        print ("Init of PublicAuthzInterface with uuid=" + self.__extension.get_uuid())
        self.__all__ = (self.authz, )

    def authz(self, request):
        return "\033[32mauthz\033[m with {}".format(self.__extension.get_subjects())


class PublicAdminInterface:

    def __init__(self, extension=None):
        self.__extension = extension
        print ("Init of PublicAdminInterface with uuid=" + self.__extension.get_uuid())
        self.__adminSubjects = []
        self.__all__ = (self.get_subjects, self.add_subject, self.adminAuthz)

    @enforce("perimeter.subjects")
    def get_subjects(self, uuid="", name=""):
        return self.__extension.get_subjects()

    @enforce("perimeter.subjects", "w")
    def add_subject(self, name, description="", domain="Default", enabled=True, project=None, mail=""):
        self.__extension.add_subjects(name)

    def adminAuthz(self, admin_object_name, action, user):
        raise NotImplemented

extension = Extension()
__PublicAuthzInterface = PublicAuthzInterface(extension)
__PublicAdminInterface = PublicAdminInterface(extension)

### Tests

print("----------------------------")
print("__PublicAuthzInterface.authz()={}".format(__PublicAuthzInterface.authz(None)))
print("----------------------------")
print("__PublicAdminInterface.get_subjects()={}".format(__PublicAdminInterface.get_subjects()))
print("---------------------------- Add a subject")
__PublicAdminInterface.add_subject("demo")
print("----------------------------")
print("__PublicAdminInterface.get_subjects()={}".format(__PublicAdminInterface.get_subjects()))
print("----------------------------")
print("__PublicAuthzInterface.authz()={}".format(__PublicAuthzInterface.authz(None)))
print("----------------------------")

### Examples

def get_subjects():
    return __PublicAdminInterface.get_subjects()


def authz(request):
    return __PublicAuthzInterface.authz(request)